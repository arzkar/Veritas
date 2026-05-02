from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import uuid
import os
import logging
import json
import shutil
from datetime import datetime
from dotenv import load_dotenv

from app.core.database import async_session, JobModel, SlideModel, ClaimModel, AuditLogModel, init_db
from sqlalchemy import select, delete, update
from app.services.ingestion import IngestionManager
from app.orchestration.graph import VeritasGraph

# --- Environment & Logging ---
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(root_dir, ".env")
app_dotenv_path = os.path.join(root_dir, "app", ".env")

load_dotenv(dotenv_path=dotenv_path)
load_dotenv(dotenv_path=app_dotenv_path)

if os.getenv("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Veritas-Diligence"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- WebSocket Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, job_id: str, websocket: WebSocket):
        await websocket.accept()
        if job_id not in self.active_connections:
            self.active_connections[job_id] = []
        self.active_connections[job_id].append(websocket)

    def disconnect(self, job_id: str, websocket: WebSocket):
        if job_id in self.active_connections:
            self.active_connections[job_id].remove(websocket)

    async def broadcast(self, job_id: str, message: dict):
        if job_id in self.active_connections:
            for connection in self.active_connections[job_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"WS Broadcast failed: {e}")

# --- App Initialization ---
app = FastAPI(title="Veritas API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ingestion_manager = IngestionManager()
investigation_graph = VeritasGraph().compile()
manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("Database initialized.")

# --- Background Task ---
async def start_investigation(job_id: str, pdf_path: str):
    try:
        # 1. Extraction Progress Bridge
        async def on_extraction_progress(current, total):
            await manager.broadcast(job_id, {
                "type": "progress", 
                "data": {"current": current, "total": total, "phase": "extraction"}
            })

        # Process PDF (Checkpoints slides and claims in DB)
        await ingestion_manager.process_pdf(
            job_id, 
            pdf_path, 
            progress_callback=on_extraction_progress
        )
        
        # 2. Orchestration Bridge
        async with async_session() as session:
            result = await session.execute(select(JobModel).where(JobModel.id == uuid.UUID(job_id)))
            job = result.scalar_one()
            
            await manager.broadcast(job_id, {"type": "status", "data": "investigating"})
            
            # TODO: Convert DB state to GraphState and invoke investigation_graph
            # For MVP, we mark complete after ingestion to test persistence
            job.status = "completed"
            await session.commit()
            await manager.broadcast(job_id, {"type": "status", "data": "completed"})
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        async with async_session() as session:
            await session.execute(
                update(JobModel).where(JobModel.id == uuid.UUID(job_id)).values(status="failed")
            )
            await session.commit()
            await manager.broadcast(job_id, {"type": "status", "data": "failed"})

# --- Endpoints ---

@app.get("/jobs")
async def list_jobs():
    async with async_session() as session:
        result = await session.execute(select(JobModel).order_by(JobModel.created_at.desc()))
        db_jobs = result.scalars().all()
        return [
            {
                "job_id": str(job.id),
                "company": job.company_name,
                "status": job.status,
                "created_at": job.created_at.isoformat(),
                "document_id": job.document_path
            }
            for job in db_jobs
        ]

@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    async with async_session() as session:
        job_uuid = uuid.UUID(job_id)
        result = await session.execute(select(JobModel).where(JobModel.id == job_uuid))
        job = result.scalar_one_or_none()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        if os.path.exists(os.path.dirname(job.document_path)):
            shutil.rmtree(os.path.dirname(job.document_path))
            
        await session.execute(delete(JobModel).where(JobModel.id == job_uuid))
        await session.commit()
        return {"status": "deleted", "job_id": job_id}

@app.post("/upload", status_code=202)
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    company_name: str = None
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    job_id = str(uuid.uuid4())
    upload_dir = f"data/uploads/{job_id}"
    os.makedirs(upload_dir, exist_ok=True)
    temp_path = os.path.join(upload_dir, file.filename)
    
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    async with async_session() as session:
        new_job = JobModel(
            id=uuid.UUID(job_id),
            company_name=company_name or file.filename.replace(".pdf", ""),
            document_path=temp_path,
            status="pending"
        )
        session.add(new_job)
        await session.commit()
    
    background_tasks.add_task(start_investigation, job_id, temp_path)
    return {"job_id": job_id, "status": "uploaded"}

@app.get("/report/{job_id}")
async def get_report(job_id: str):
    async with async_session() as session:
        job_uuid = uuid.UUID(job_id)
        result = await session.execute(select(JobModel).where(JobModel.id == job_uuid))
        job = result.scalar_one_or_none()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        claims_res = await session.execute(select(ClaimModel).where(ClaimModel.job_id == job_uuid))
        logs_res = await session.execute(select(AuditLogModel).where(AuditLogModel.job_id == job_uuid).order_by(AuditLogModel.timestamp.asc()))
        
        return {
            "status": job.status,
            "company": job.company_name,
            "report": {
                "global_credibility_score": job.global_score,
                "red_flag_count": job.red_flag_count,
                "claims": {str(c.id): {
                    "id": str(c.id),
                    "statement": c.statement,
                    "category": c.category,
                    "importance": c.importance,
                    "belief": c.belief_state,
                    "credibility_score": c.credibility_score,
                    "primary_slide": c.slide_index,
                    "analyst_summary": c.analyst_summary,
                    "skeptic_summary": c.skeptic_summary
                } for c in claims_res.scalars().all()},
                "audit_logs": [{
                    "id": str(l.id),
                    "timestamp": l.timestamp.isoformat(),
                    "agent_name": l.agent_name,
                    "event_type": l.event_type,
                    "message": l.message,
                    "metadata": l.metadata_json
                } for l in logs_res.scalars().all()]
            }
        }

@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await manager.connect(job_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(job_id, websocket)
