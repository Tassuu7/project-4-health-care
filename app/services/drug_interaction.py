"""
AegisCare Enterprise Patient Management System - Drug-Drug Interaction Safety Engine
Cross-checks prescribed medications against known clinical contraindications and drug pairs.
"""

from typing import Dict, List, Optional, Tuple

# Contraindicated & High-Severity Drug Interaction Matrix
KNOWN_INTERACTIONS: Dict[Tuple[str, str], Dict[str, str]] = {
    ("WARFARIN", "ASPIRIN"): {
        "severity": "CRITICAL",
        "description": "Concurrent use significantly increases risk of severe gastrointestinal hemorrhage."
    },
    ("WARFARIN", "IBUPROFEN"): {
        "severity": "HIGH",
        "description": "NSAIDs displace warfarin from albumin and inhibit platelet aggregation."
    },
    ("LISINOPRIL", "SPIRONOLACTONE"): {
        "severity": "HIGH",
        "description": "Concomitant ACE inhibitor and potassium-sparing diuretic causes severe hyperkalemia."
    },
    ("CIPROFLOXACIN", "THEOPHYLLINE"): {
        "severity": "CRITICAL",
        "description": "Ciprofloxacin inhibits theophylline clearance resulting in potential toxic seizures."
    },
    ("SIMVASTATIN", "CLARITHROMYCIN"): {
        "severity": "CRITICAL",
        "description": "Strong CYP3A4 inhibition increases statin toxicity and risk of rhabdomyolysis."
    },
    ("METFORMIN", "CONTRAST_MEDIA"): {
        "severity": "HIGH",
        "description": "Risk of severe lactic acidosis in renal impairment."
    },
    ("SERTRALINE", "TRAMADOL"): {
        "severity": "HIGH",
        "description": "Combination may precipitate potentially fatal Serotonin Syndrome."
    }
}


class DrugInteractionEngine:
    """Clinical safety engine for detecting harmful drug-drug conflicts."""

    @staticmethod
    def check_interaction(drug_a: str, drug_b: str) -> Optional[Dict[str, str]]:
        """Evaluate if two active drug substances exhibit severe interaction."""
        a = drug_a.strip().upper()
        b = drug_b.strip().upper()
        
        if (a, b) in KNOWN_INTERACTIONS:
            return KNOWN_INTERACTIONS[(a, b)]
        if (b, a) in KNOWN_INTERACTIONS:
            return KNOWN_INTERACTIONS[(b, a)]
        return None

    @classmethod
    def check_prescription_safety(cls, medication_names: List[str]) -> List[Dict[str, str]]:
        """Cross-check all pairs within a prescribed medication list."""
        conflicts = []
        n = len(medication_names)
        for i in range(n):
            for j in range(i + 1, n):
                interaction = cls.check_interaction(medication_names[i], medication_names[j])
                if interaction:
                    conflicts.append({
                        "drug_1": medication_names[i],
                        "drug_2": medication_names[j],
                        "severity": interaction["severity"],
                        "description": interaction["description"]
                    })
        return conflicts
