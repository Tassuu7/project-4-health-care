"""
Unit Tests for HL7 / FHIR R4 Interoperability Conversion
"""

from datetime import date
from app.models.patient import Patient
from app.core.constants import Gender, BloodGroup
from app.services.fhir_service import FhirConverterService


def test_fhir_patient_resource_conversion():
    """Test serialization of internal Patient model into standard FHIR R4 Resource."""
    patient = Patient(
        id=42,
        mrn="MRN-2026-0042",
        first_name="Eleanor",
        last_name="Rigby",
        date_of_birth=date(1972, 8, 14),
        gender=Gender.FEMALE,
        blood_group=BloodGroup.O_POSITIVE,
        phone_number="(555) 018-2948",
        email="eleanor@example.com"
    )
    fhir_res = FhirConverterService.patient_to_fhir_resource(patient)
    assert fhir_res["resourceType"] == "Patient"
    assert fhir_res["id"] == "aegis-42"
    assert fhir_res["identifier"][0]["value"] == "MRN-2026-0042"
    assert fhir_res["name"][0]["family"] == "Rigby"
    assert fhir_res["name"][0]["given"] == ["Eleanor"]
