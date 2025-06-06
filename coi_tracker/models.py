from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

@dataclass
class PolicyLimit:
    name: str
    required_amount: float

@dataclass
class RuleTemplate:
    name: str
    policy_limits: List[PolicyLimit] = field(default_factory=list)
    description_language: Optional[str] = None
    additional_insured: List[str] = field(default_factory=list)

@dataclass
class CertificateOfInsurance:
    id: int
    tenant: str
    file_path: str
    issue_date: Optional[date] = None
    expiration_date: Optional[date] = None
    raw_text: Optional[str] = None
    matched: bool = False
    mismatches: List[str] = field(default_factory=list)

