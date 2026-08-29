"""
AegisCare Enterprise Patient Management System - HL7 / FHIR R4 Interoperability Converter
Exports internal patient records into standard HL7 FHIR Release 4 JSON resource bundles.
"""

from typing import Any, Dict
from app.models.clinical import MedicalRecord, VitalSign
from app.models.patient import Patient


class FhirConverterService:
    """Serializes clinical entities into standardized FHIR R4 resource definitions."""

    @staticmethod
    def patient_to_fhir_resource(patient: Patient) -> Dict[str, Any]:
        """Convert internal Patient model into FHIR R4 Patient Resource."""
        return {
            "resourceType": "Patient",
            "id": f"aegis-{patient.id}",
            "identifier": [
                {
                    "use": "usual",
                    "type": {
                        "coding": [
                            {"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "MR", "display": "Medical Record Number"}
                        ]
                    },
                    "system": "urn:oid:2.16.840.1.113883.4.1",
                    "value": patient.mrn
                }
            ],
            "active": True,
            "name": [
                {
                    "use": "official",
                    "family": patient.last_name,
                    "given": [patient.first_name]
                }
            ],
            "telecom": [
                {"system": "phone", "value": patient.phone_number, "use": "mobile"},
                {"system": "email", "value": patient.email or "none@aegiscare.local", "use": "home"}
            ],
            "gender": patient.gender.value.lower() if hasattr(patient.gender, "value") else "unknown",
            "birthDate": patient.date_of_birth.strftime("%Y-%m-%d") if patient.date_of_birth else None,
            "address": [
                {
                    "use": "home",
                    "line": [patient.address_street or "Main St"],
                    "city": patient.address_city or "Metropolis",
                    "state": patient.address_state or "CA",
                    "postalCode": patient.address_postal_code or "90001",
                    "country": patient.address_country or "USA"
                }
            ]
        }

    @staticmethod
    def vitals_to_fhir_observation(vital: VitalSign) -> Dict[str, Any]:
        """Convert vital sign entry into FHIR R4 Observation Resource."""
        return {
            "resourceType": "Observation",
            "id": f"obs-vital-{vital.id}",
            "status": "final",
            "category": [
                {
                    "coding": [
                        {"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs", "display": "Vital Signs"}
                    ]
                }
            ],
            "code": {
                "coding": [
                    {"system": "http://loinc.org", "code": "85354-9", "display": "Blood pressure panel with all children optional"}
                ]
            },
            "subject": {"reference": f"Patient/aegis-{vital.patient_id}"},
            "effectiveDateTime": vital.recorded_at.isoformat() if vital.recorded_at else None,
            "component": [
                {
                    "code": {"coding": [{"system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure"}]},
                    "valueQuantity": {"value": vital.systolic_bp, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"}
                },
                {
                    "code": {"coding": [{"system": "http://loinc.org", "code": "8462-4", "display": "Diastolic blood pressure"}]},
                    "valueQuantity": {"value": vital.diastolic_bp, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"}
                },
                {
                    "code": {"coding": [{"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"}]},
                    "valueQuantity": {"value": vital.heart_rate, "unit": "beats/minute", "system": "http://unitsofmeasure.org", "code": "/min"}
                },
                {
                    "code": {"coding": [{"system": "http://loinc.org", "code": "2708-6", "display": "Oxygen saturation in Arterial blood"}]},
                    "valueQuantity": {"value": vital.oxygen_saturation, "unit": "%", "system": "http://unitsofmeasure.org", "code": "%"}
                }
            ]
        }
