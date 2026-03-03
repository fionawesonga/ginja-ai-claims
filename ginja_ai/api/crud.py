from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ginja_ai.api.models import Member, ProcedureCost, Claim, ClaimValidation
from ginja_ai.api.serializers import MemberCreate, ProcedureCostCreate, ClaimCreate, ClaimValidationCreate
from datetime import date

def get_member(db: Session, member_id: str):
    return db.query(Member).filter(Member.member_id == member_id).first()

def create_member(db: Session, member: MemberCreate):
    try:
        db_member = Member(
            member_id=member.member_id,
            first_name=member.first_name,
            last_name=member.last_name,
            eligibility_status=member.eligibility_status,
            enrollment_date=member.enrollment_date
        )
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return db_member
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_procedure(db: Session, procedure_code: str):
    return db.query(ProcedureCost).filter(ProcedureCost.procedure_code == procedure_code).first()

def create_procedure(db: Session, procedure: ProcedureCostCreate):
    try:
        db_procedure = ProcedureCost(
            procedure_code=procedure.procedure_code,
            procedure_name=procedure.procedure_name,
            average_cost=procedure.average_cost
        )
        db.add(db_procedure)
        db.commit()
        db.refresh(db_procedure)
        return db_procedure
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_claim(db: Session, claim_id: str):
    return db.query(Claim).filter(Claim.claim_id == claim_id).first()

def create_claim(db: Session, claim_id: str, claim: ClaimCreate):
    try:
        db_claim = Claim(
            claim_id=claim_id,
            member_id=claim.member_id,
            provider_id=claim.provider_id,
            diagnosis_code=claim.diagnosis_code,
            procedure_code=claim.procedure_code,
            claim_amount=claim.claim_amount,
            claim_date=date.today()
        )
        db.add(db_claim)
        db.commit()
        db.refresh(db_claim)
        return db_claim
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def create_claim_validation(db: Session, validation: ClaimValidationCreate):
    try:
        db_validation = ClaimValidation(
            claim_id=validation.claim_id,
            eligibility_check=validation.eligibility_check,
            benefit_limit_ok=validation.benefit_limit_ok,
            fraud_flag=validation.fraud_flag,
            approved_amount=validation.approved_amount,
            status=validation.status
        )
        db.add(db_validation)
        db.commit()
        db.refresh(db_validation)
        return db_validation
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_claim_validation(db: Session, claim_id: str):
    return db.query(ClaimValidation).filter(ClaimValidation.claim_id == claim_id).first()
