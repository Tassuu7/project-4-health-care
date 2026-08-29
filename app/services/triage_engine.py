"""
AegisCare Enterprise Patient Management System - Clinical Triage Decision Engine
Implements the Emergency Severity Index (ESI) 5-level clinical acuity algorithm.
"""

from typing import Dict, Tuple
from app.core.constants import TriageLevel
from app.schemas.triage import TriageInput


class TriageEngine:
    """Clinical decision support system calculating emergency triage scores (ESI Level 1-5)."""

    @staticmethod
    def evaluate_vital_signs_danger(
        heart_rate: int = None,
        systolic_bp: int = None,
        respiratory_rate: int = None,
        oxygen_saturation: float = None
    ) -> bool:
        """Check if physiological vital signs exceed critical danger thresholds."""
        if oxygen_saturation and oxygen_saturation < 92.0:
            return True
        if heart_rate and (heart_rate > 130 or heart_rate < 40):
            return True
        if respiratory_rate and (respiratory_rate > 30 or respiratory_rate < 8):
            return True
        if systolic_bp and (systolic_bp > 200 or systolic_bp < 80):
            return True
        return False

    @classmethod
    def calculate_esi_level(cls, intake: TriageInput) -> Tuple[TriageLevel, str, str]:
        """
        Evaluate ESI Triage Level according to standard ESI Version 4 algorithm:
        - Decision Point A: Is patient dying / requires immediate life-saving resuscitation? -> Level 1
        - Decision Point B: Is this a high-risk situation, confused/lethargic, or severe pain? -> Level 2
        - Decision Point C: How many resources are needed?
          * 0 resources -> Level 5
          * 1 resource -> Level 4
          * 2+ resources -> Level 3 (Check danger vital signs; if abnormal, upgrade to Level 2)
        """
        # Step A: Resuscitation check
        if intake.is_resuscitation_required:
            return (
                TriageLevel.LEVEL_1_RESUSCITATION,
                "RED_RESUSCITATION_BAY",
                "Immediate life threat identified. Patient requires immediate resuscitation."
            )

        # Step B: High risk / acute distress check
        is_danger_vitals = cls.evaluate_vital_signs_danger(
            heart_rate=intake.heart_rate,
            systolic_bp=intake.systolic_bp,
            respiratory_rate=intake.respiratory_rate,
            oxygen_saturation=intake.oxygen_saturation
        )

        if intake.is_high_risk_situation or intake.pain_score >= 8:
            return (
                TriageLevel.LEVEL_2_EMERGENT,
                "ORANGE_ACUTE_CARE",
                "High-risk situation or severe acute pain score. Time-sensitive evaluation required."
            )

        # Step C: Resource estimation
        resources = intake.estimated_resource_count
        if resources == 0:
            return (
                TriageLevel.LEVEL_5_NON_URGENT,
                "BLUE_FAST_TRACK",
                "Non-urgent presentation. Routine assessment and prescription refill."
            )
        elif resources == 1:
            return (
                TriageLevel.LEVEL_4_LESS_URGENT,
                "GREEN_FAST_TRACK",
                "Less urgent presentation requiring single diagnostic modality."
            )
        else: # 2 or more resources
            if is_danger_vitals:
                return (
                    TriageLevel.LEVEL_2_EMERGENT,
                    "ORANGE_ACUTE_CARE",
                    "Vital sign danger zone detected. Upgraded from Level 3 to Level 2."
                )
            return (
                TriageLevel.LEVEL_3_URGENT,
                "YELLOW_URGENT_CARE",
                "Urgent condition requiring complex diagnostics and laboratory testing."
            )
