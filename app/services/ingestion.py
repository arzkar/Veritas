from app.services.pdf_parser import PDFParser
from app.retrieval.vector_store import VectorStoreService
from app.agents.extractor import ExtractorAgent
from app.core.database import async_session, JobModel, SlideModel, ClaimModel
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import Dict, Any, List, Callable, Optional
import logging
import uuid

logger = logging.getLogger(__name__)

class IngestionManager:
    """
    Coordinates the ingestion process with persistent checkpointing (Saga Pattern).
    Supports resumption from individual slides.
    """
    
    def __init__(self):
        self.parser = PDFParser()
        self.vector_service = VectorStoreService()
        self.extractor = ExtractorAgent()

    async def process_pdf(self, job_id: str, pdf_path: str, progress_callback: Optional[Callable] = None):
        """
        Runs the full ingestion pipeline with DB persistence and resumption logic.
        """
        async with async_session() as session:
            # 1. Fetch Job
            result = await session.execute(select(JobModel).where(JobModel.id == uuid.UUID(job_id)))
            job = result.scalar_one_or_none()
            if not job:
                raise ValueError(f"Job {job_id} not found in database.")

            try:
                # 2. Extract Slides (Initial metadata pass)
                # Note: In a production version, we'd checkpoint this metadata too
                slides_metadata = self.parser.extract_slides_as_markdown(pdf_path)
                total_slides = len(slides_metadata)
                
                job.status = "ingesting"
                await session.commit()

                # 3. Slide-by-Slide Processing (The Saga Loop)
                for i, slide_data in enumerate(slides_metadata):
                    slide_idx = i + 1
                    
                    # Check if slide already processed
                    slide_result = await session.execute(
                        select(SlideModel).where(
                            SlideModel.job_id == job.id, 
                            SlideModel.slide_index == slide_idx,
                            SlideModel.status == "processed"
                        )
                    )
                    existing_slide = slide_result.scalar_one_or_none()
                    
                    if existing_slide:
                        logger.info(f"Slide {slide_idx} already processed. Skipping.")
                        if progress_callback:
                            await progress_callback(slide_idx, total_slides)
                        continue

                    # Process Slide
                    if progress_callback:
                        await progress_callback(slide_idx, total_slides)
                    
                    # Create or update slide record
                    new_slide = SlideModel(
                        job_id=job.id,
                        slide_index=slide_idx,
                        markdown_content=slide_data["content"],
                        status="processed"
                    )
                    session.add(new_slide)
                    
                    # Checkpoint progress
                    job.current_slide_index = slide_idx
                    await session.commit()
                    logger.info(f"Persisted Slide {slide_idx}/{total_slides} for job {job_id}")

                # 4. Claim Extraction (Batch from Markdown)
                job.status = "extracting_claims"
                await session.commit()
                
                # Fetch all slides for this job
                slides_result = await session.execute(
                    select(SlideModel).where(SlideModel.job_id == job.id).order_by(SlideModel.slide_index)
                )
                all_slides = slides_result.scalars().all()
                
                for slide in all_slides:
                    if not slide.markdown_content: continue
                    
                    logger.info(f"Extracting claims from slide {slide.slide_index}")
                    claims = await self.extractor.extract_claims(slide.markdown_content, slide.slide_index)
                    
                    for c in claims:
                        db_claim = ClaimModel(
                            id=uuid.UUID(c.id),
                            job_id=job.id,
                            statement=c.statement,
                            category=c.category,
                            importance=c.importance,
                            slide_index=slide.slide_index,
                            belief_state="unverified",
                            credibility_score=0.5
                        )
                        session.add(db_claim)
                
                # 5. Finalize Ingestion Phase
                job.status = "investigating"
                await session.commit()
                
                return job
                
            except Exception as e:
                job.status = "failed"
                await session.commit()
                logger.error(f"Ingestion failed for job {job_id}: {str(e)}")
                raise
