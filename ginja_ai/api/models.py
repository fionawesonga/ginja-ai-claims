from sqlalchemy import Column, String, Date, Numeric, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base

class Member(Base):
    __tablename__ = "Member"

    member_id = Column(String(50), primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    eligibility_status = Column(String(20), nullable=False, default='active')
    enrollment_date = Column(Date, nullable=False)

    claims = relationship("Claim", back_populates="member", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Member(member_id={self.member_id}, name={self.first_name} {self.last_name})>"


class ProcedureCost(Base):
    __tablename__ = "ProcedureCost"

    procedure_code = Column(String(50), primary_key=True, index=True)
    procedure_name = Column(String(100), nullable=False)
    average_cost = Column(Numeric(12, 2), nullable=False)

    claims = relationship("Claim", back_populates="procedure", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProcedureCost(procedure_code={self.procedure_code})>"


class Claim(Base):
    __tablename__ = "Claim"

    claim_id = Column(String(50), primary_key=True, index=True)
    member_id = Column(String(50), ForeignKey("Member.member_id"), nullable=False, index=True)
    provider_id = Column(String(50), nullable=False)
    diagnosis_code = Column(String(50), nullable=False)
    procedure_code = Column(String(50), ForeignKey("ProcedureCost.procedure_code"), nullable=False, index=True)
    claim_amount = Column(Numeric(12, 2), nullable=False)
    claim_date = Column(Date, nullable=False)

    member = relationship("Member", back_populates="claims")
    procedure = relationship("ProcedureCost", back_populates="claims")
    validation = relationship("ClaimValidation", back_populates="claim", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Claim(claim_id={self.claim_id})>"


class ClaimValidation(Base):
    __tablename__ = "ClaimValidation"

    validation_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    claim_id = Column(String(50), ForeignKey("Claim.claim_id"), nullable=False, unique=True, index=True)
    eligibility_check = Column(Boolean, nullable=False)
    benefit_limit_ok = Column(Boolean, nullable=False)
    fraud_flag = Column(Boolean, nullable=False)
    approved_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    claim = relationship("Claim", back_populates="validation")

    def __repr__(self):
        return f"<ClaimValidation(claim_id={self.claim_id}, status={self.status})>"
