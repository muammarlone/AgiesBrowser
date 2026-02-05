from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.database import Base

class DeliverableRequest(Base):
    __tablename__ = "deliverable_requests"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    methodology = Column(String)  # Scrum, SAFe, Banking
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # JSON payload for flexibility (diagram types, specific requirements)
    parameters = Column(JSON, default={})
    
    # Relationship to outbox
    outbox_items = relationship("DeliverableOutbox", back_populates="request")

class DeliverableOutbox(Base):
    __tablename__ = "deliverable_outbox"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("deliverable_requests.id"))
    file_path = Column(String)
    file_type = Column(String)  # pptx, png, svg
    generated_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="ready")  # ready, approved, delivered
    
    request = relationship("DeliverableRequest", back_populates="outbox_items")

class DeliverableAuditLog(Base):
    """
    Graph-Native Audit Log (Adjacency List Pattern).
    Enables O(1) traversal of causality chains.
    """
    __tablename__ = "deliverable_audit_log"

    id = Column(Integer, primary_key=True, index=True)
    
    # Graph Edge Definition
    source_node = Column(String, index=True)  # e.g., "User:123"
    target_node = Column(String, index=True)  # e.g., "Request:456"
    predicate = Column(String, index=True)    # e.g., "INITIATED", "APPROVED_BY"
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    properties = Column(JSON) # Edge attributes
