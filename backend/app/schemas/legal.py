from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LegalAgreement(BaseModel):
    """法的・倫理的ポジショニングの同意確認"""
    privacy_policy_agreed: bool
    terms_of_service_agreed: bool
    safety_guidelines_agreed: bool
    agreement_date: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class LegalAgreementResponse(BaseModel):
    """法的・倫理的ポジショニングの同意確認レスポンス"""
    message: str
    agreement_id: Optional[str] = None
    agreement_date: datetime 