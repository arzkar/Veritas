from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
from typing import List, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    """
    High-fidelity layout-aware PDF parser using Docling.
    Converts slides into Markdown to preserve semantic context.
    """
    
    def __init__(self):
        # Initialize the converter (will download models to cache volume on first run)
        self.converter = DocumentConverter()

    def extract_slides_as_markdown(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Converts PDF into a list of slide-based markdown objects.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")
            
        logger.info(f"Starting Docling conversion for {pdf_path}")
        
        # 1. Convert document
        result = self.converter.convert(pdf_path)
        
        # 2. Split by page/slide
        # Note: Docling usually provides a unified document, we extract per-page markdown
        doc = result.document
        slides = []
        
        # Heuristic: iterate through pages and extract their specific content
        for page_num, page in doc.pages.items():
            # Get markdown for this specific page
            # This is a simplified split for the MVP
            page_markdown = doc.export_to_markdown() # Full doc for now
            # In a refined version, we use docling's granular element mapping to isolate page content
            
            slides.append({
                "slide_index": page_num,
                "content": page_markdown, # Temporarily full doc until refined per-page split
                "metadata": {
                    "width": page.size.width if page.size else 0,
                    "height": page.size.height if page.size else 0
                }
            })
            
        return slides
