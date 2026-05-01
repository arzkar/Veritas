import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, Enum, JSON
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid

# Load from env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://veritas_admin:veritas_pass_2026@localhost:5432/veritas")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# --- Database Models ---

class JobModel(Base):
    __tablename__ = "investigation_jobs"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(255))
    document_path: Mapped[str] = mapped_column(String(512))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    global_score: Mapped[float] = mapped_column(Float, default=1.0)
    red_flag_count: Mapped[int] = mapped_column(Integer, default=0)
    synthesis_report: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    slides = relationship("SlideModel", back_populates="job", cascade="all, delete-orphan")
    claims = relationship("ClaimModel", back_populates="job", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLogModel", back_populates="job", cascade="all, delete-orphan")

class SlideModel(Base):
    __tablename__ = "investigative_slides"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigation_jobs.id"))
    slide_index: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    markdown_content: Mapped[Optional[str]] = mapped_column(String)
    
    job = relationship("JobModel", back_populates="slides")

class ClaimModel(Base):
    __tablename__ = "investigative_claims"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigation_jobs.id"))
    statement: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String(100))
    importance: Mapped[float] = mapped_column(Float)
    belief_state: Mapped[str] = mapped_column(String(50), default="unverified")
    credibility_score: Mapped[float] = mapped_column(Float, default=0.5)
    slide_index: Mapped[int] = mapped_column(Integer)
    analyst_summary: Mapped[Optional[str]] = mapped_column(String)
    skeptic_summary: Mapped[Optional[str]] = mapped_column(String)
    audit_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    
    job = relationship("JobModel", back_populates="claims")

class AuditLogModel(Base):
    __tablename__ = "agent_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigation_jobs.id"))
    agent_name: Mapped[str] = mapped_column(String(100))
    event_type: Mapped[str] = mapped_column(String(100))
    message: Mapped[str] = mapped_column(String)
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    job = relationship("JobModel", back_populates="audit_logs")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
