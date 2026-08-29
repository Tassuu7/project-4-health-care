"""
Unit Tests for E-Prescription Safety and Drug-Drug Interaction Checker
"""

import pytest
from app.services.drug_interaction import DrugInteractionEngine


def test_drug_interaction_detection():
    """Test detection of critical contraindicated drug pairs (Warfarin + Aspirin)."""
    interaction = DrugInteractionEngine.check_interaction("WARFARIN", "ASPIRIN")
    assert interaction is not None
    assert interaction["severity"] == "CRITICAL"

    # Test reverse order
    interaction_rev = DrugInteractionEngine.check_interaction("Aspirin", "Warfarin")
    assert interaction_rev is not None
    assert interaction_rev["severity"] == "CRITICAL"


def test_safe_drug_pair():
    """Test non-interacting medications."""
    interaction = DrugInteractionEngine.check_interaction("PARACETAMOL", "AMOXICILLIN")
    assert interaction is None
