"""
Unit Tests for Emergency Severity Index (ESI) Triage Decision Engine
"""

import pytest
from app.core.constants import TriageLevel
from app.schemas.triage import TriageInput
from app.services.triage_engine import TriageEngine


def test_esi_level_1_resuscitation():
    """Test immediate life-threat resuscitation triage scoring (ESI 1)."""
    intake = TriageInput(
        patient_id=1,
        chief_complaint="Unresponsive, cardiac arrest in progress",
        is_resuscitation_required=True
    )
    level, zone, _ = TriageEngine.calculate_esi_level(intake)
    assert level == TriageLevel.LEVEL_1_RESUSCITATION
    assert "RESUSCITATION" in zone


def test_esi_level_2_high_risk_and_danger_vitals():
    """Test severe pain / danger vitals triage scoring (ESI 2)."""
    intake = TriageInput(
        patient_id=1,
        chief_complaint="Severe crushing substernal chest pain",
        pain_score=9,
        heart_rate=135,
        oxygen_saturation=90.0,
        is_high_risk_situation=True
    )
    level, zone, _ = TriageEngine.calculate_esi_level(intake)
    assert level == TriageLevel.LEVEL_2_EMERGENT


def test_esi_level_3_and_4():
    """Test resource-based triage scoring (ESI 3 and 4)."""
    # 2 resources with normal vitals -> Level 3
    intake_3 = TriageInput(
        patient_id=1,
        chief_complaint="Right lower quadrant abdominal pain",
        pain_score=5,
        heart_rate=80,
        oxygen_saturation=99.0,
        estimated_resource_count=2
    )
    level_3, _, _ = TriageEngine.calculate_esi_level(intake_3)
    assert level_3 == TriageLevel.LEVEL_3_URGENT

    # 1 resource -> Level 4
    intake_4 = TriageInput(
        patient_id=1,
        chief_complaint="Ankle sprain after walking down stairs",
        pain_score=3,
        estimated_resource_count=1
    )
    level_4, _, _ = TriageEngine.calculate_esi_level(intake_4)
    assert level_4 == TriageLevel.LEVEL_4_LESS_URGENT
