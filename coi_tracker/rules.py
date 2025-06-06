"""Rule configuration and checking logic."""
from dataclasses import dataclass, field
from typing import List

from .models import CertificateOfInsurance
from .llm import analyze_compliance


@dataclass
class RuleConfig:
    policy_limits: List[str] = field(default_factory=list)
    description_language: List[str] = field(default_factory=list)
    additional_insured: List[str] = field(default_factory=list)


class RuleEngine:
    def __init__(self, config: RuleConfig):
        self.config = config

    def evaluate(self, coi: CertificateOfInsurance) -> CertificateOfInsurance:
        text = coi.raw_text or ""
        rules_to_check = self.config.policy_limits + self.config.description_language + self.config.additional_insured
        missing = analyze_compliance(text, rules_to_check)
        coi.matched = not missing
        coi.mismatches = missing
        return coi
