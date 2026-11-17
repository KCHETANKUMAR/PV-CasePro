from datetime import datetime, date
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

class Base(DeclarativeBase): pass

class Case(Base):
    __tablename__ = "cases"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    report_type: Mapped[str] = mapped_column(String(20), default="Initial")
    received_date: Mapped[date | None] = mapped_column(Date)
    country: Mapped[str | None] = mapped_column(String(80))
    reporter_type: Mapped[str | None] = mapped_column(String(80))
    reporter_name: Mapped[str | None] = mapped_column(String(120))
    reporter_contact: Mapped[str | None] = mapped_column(String(200))
    patient_identifier: Mapped[str | None] = mapped_column(String(100))
    age_group: Mapped[str | None] = mapped_column(String(30))
    age: Mapped[str | None] = mapped_column(String(30))
    sex: Mapped[str | None] = mapped_column(String(30))
    product: Mapped[str | None] = mapped_column(String(150))
    strength: Mapped[str | None] = mapped_column(String(80))
    dose: Mapped[str | None] = mapped_column(String(80))
    route: Mapped[str | None] = mapped_column(String(80))
    frequency: Mapped[str | None] = mapped_column(String(80))
    indication: Mapped[str | None] = mapped_column(String(200))
    therapy_start: Mapped[date | None] = mapped_column(Date)
    therapy_stop: Mapped[date | None] = mapped_column(Date)
    event_verbatim: Mapped[str | None] = mapped_column(Text)
    training_term: Mapped[str | None] = mapped_column(String(100))
    terminology_rationale: Mapped[str | None] = mapped_column(Text)
    event_onset: Mapped[date | None] = mapped_column(Date)
    event_end: Mapped[date | None] = mapped_column(Date)
    outcome: Mapped[str | None] = mapped_column(String(80))
    medical_history: Mapped[str | None] = mapped_column(Text)
    concomitant_meds: Mapped[str | None] = mapped_column(Text)
    dechallenge: Mapped[str | None] = mapped_column(String(200))
    rechallenge: Mapped[str | None] = mapped_column(String(200))
    narrative_source: Mapped[str | None] = mapped_column(Text)
    reviewed_narrative: Mapped[str | None] = mapped_column(Text)
    comments: Mapped[str | None] = mapped_column(Text)
    seriousness: Mapped[str] = mapped_column(String(20), default="Unknown")
    serious_criteria: Mapped[str | None] = mapped_column(Text)
    seriousness_rationale: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(30), default="Unknown")
    causality: Mapped[str] = mapped_column(String(80), default="Not assessed")
    causality_rationale: Mapped[str | None] = mapped_column(Text)
    expectedness: Mapped[str] = mapped_column(String(80), default="Not assessed")
    reviewer_comments: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="New", index=True)
    qc_errors: Mapped[str | None] = mapped_column(Text)
    human_review_status: Mapped[str] = mapped_column(String(40), default="Not reviewed")
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    follow_ups: Mapped[list["FollowUp"]] = relationship(back_populates="case", cascade="all, delete-orphan")

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), unique=True)
    identifier: Mapped[str | None] = mapped_column(String(100))
    age_group: Mapped[str | None] = mapped_column(String(30))
    sex: Mapped[str | None] = mapped_column(String(30))

class Reporter(Base):
    __tablename__ = "reporters"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), unique=True)
    reporter_type: Mapped[str | None] = mapped_column(String(80))
    name: Mapped[str | None] = mapped_column(String(120))
    contact: Mapped[str | None] = mapped_column(String(200))

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), unique=True)
    name: Mapped[str | None] = mapped_column(String(150))
    strength: Mapped[str | None] = mapped_column(String(80))
    dose: Mapped[str | None] = mapped_column(String(80))
    route: Mapped[str | None] = mapped_column(String(80))
    indication: Mapped[str | None] = mapped_column(String(200))

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), unique=True)
    verbatim: Mapped[str | None] = mapped_column(Text)
    training_term: Mapped[str | None] = mapped_column(String(100))
    coding_rationale: Mapped[str | None] = mapped_column(Text)
    onset: Mapped[date | None] = mapped_column(Date)
    outcome: Mapped[str | None] = mapped_column(String(80))

class Assessment(Base):
    __tablename__ = "assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), unique=True)
    seriousness: Mapped[str] = mapped_column(String(20), default="Unknown")
    seriousness_criteria: Mapped[str | None] = mapped_column(Text)
    seriousness_rationale: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(30), default="Unknown")
    causality: Mapped[str] = mapped_column(String(80), default="Not assessed")
    expectedness: Mapped[str] = mapped_column(String(80), default="Not assessed")

class FollowUp(Base):
    __tablename__ = "follow_ups"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), index=True)
    missing_information: Mapped[str] = mapped_column(Text)
    questions: Mapped[str | None] = mapped_column(Text)
    date_sent: Mapped[date | None] = mapped_column(Date)
    response_date: Mapped[date | None] = mapped_column(Date)
    response_received: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="Open")
    comments: Mapped[str | None] = mapped_column(Text)
    case: Mapped[Case] = relationship(back_populates="follow_ups")

class ReferenceSafetyInformation(Base):
    __tablename__ = "reference_safety_information"
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(150), index=True)
    version: Mapped[str] = mapped_column(String(50))
    effective_date: Mapped[date | None] = mapped_column(Date)
    listed_events: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)

class QCReview(Base):
    __tablename__ = "qc_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), index=True)
    checklist: Mapped[str] = mapped_column(Text)
    reviewer: Mapped[str | None] = mapped_column(String(120))
    final_status: Mapped[str] = mapped_column(String(40), default="Not reviewed")
    comments: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[str] = mapped_column(String(30), index=True)
    action: Mapped[str] = mapped_column(String(80))
    previous_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[str] = mapped_column(String(120), default="Local user")
    comment: Mapped[str | None] = mapped_column(Text)

class TrainingAssessment(Base):
    __tablename__ = "training_assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    answers: Mapped[str] = mapped_column(Text)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
