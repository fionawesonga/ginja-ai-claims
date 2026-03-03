from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class MemberBase(BaseModel):
    first_name: str
    last_name: str
    eligibility_status: str
    enrollment_date: date

class MemberCreate(MemberBase):
    member_id: str

class MemberResponse(MemberBase):
    member_id: str
    class Config:
        from_attributes = True

class ProcedureCostBase(BaseModel):
    procedure_name: str
    average_cost: Decimal

class ProcedureCostCreate(ProcedureCostBase):
    procedure_code: str

class ProcedureCostResponse(ProcedureCostBase):
    procedure_code: str
    class Config:
        from_attributes = True

class ClaimCreate(BaseModel):
    member_id: str = Field(..., example="M123")
    provider_id: str = Field(..., example="H456")
    diagnosis_code: str = Field(..., example="D001")
    procedure_code: str = Field(..., example="P001")
    claim_amount: Decimal = Field(..., example=50000)

class ClaimResponse(BaseModel):
    claim_id: str
    member_id: str
    provider_id: str
    diagnosis_code: str
    procedure_code: str
    claim_amount: Decimal
    claim_date: date
    class Config:
        from_attributes = True

class ClaimValidationCreate(BaseModel):
    claim_id: str
    eligibility_check: bool
    benefit_limit_ok: bool
    fraud_flag: bool
    approved_amount: Decimal
    status: str

class ClaimValidationResponse(BaseModel):
    validation_id: int
    claim_id: str
    eligibility_check: bool
    benefit_limit_ok: bool
    fraud_flag: bool
    approved_amount: Decimal
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ClaimSubmitResponse(BaseModel):
    claim_id: str
    status: str
    fraud_flag: bool
    approved_amount: Decimal

class ClaimStatusResponse(BaseModel):
    claim_id: str
    member_id: str
    claim_amount: Decimal
    status: str
    fraud_flag: bool
    approved_amount: Decimal
    created_at: datetime
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
