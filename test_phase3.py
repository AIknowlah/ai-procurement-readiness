"""
Simple Phase 3 test - Insert one assessment into BigQuery
"""

from datetime import datetime
from bigquery_storage import AssessmentStorage

# Prepare a minimal test assessment
test_assessment = {
    "assessment_id": "ASM-TEST-001",
    "vendor_name": "Test Vendor Corp",
    "system_name": "Test AI System",
    "system_description": "Test system for Phase 3 verification",
    
    "assessment_date": datetime.now().isoformat(),
    "assessor_id": "test_officer_001",
    "assessor_agency": "Test Agency",
    "assessment_status": "draft",
    
    # Simple scores for all 11 principles (all at 80% for testing)
    "principle_scores": {
        "P1_Transparency": 0.80,
        "P2_Explainability": 0.85,
        "P3_Reproducibility": 0.75,
        "P4_Safety": 0.90,
        "P5_Security": 0.88,
        "P6_Robustness": 0.82,
        "P7_Fairness": 0.86,
        "P8_DataGovernance": 0.79,
        "P9_Accountability": 0.83,
        "P10_HumanAgency": 0.87,
        "P11_InclusiveGrowth": 0.91
    },
    "total_readiness_score": 0.84,
    
    # Minimal response data
    "responses": [
        {
            "question_id": "Q001",
            "principle_number": 1,
            "principle_name": "Transparency",
            "answer": "Have",
            "score": 1.0
        }
    ],
    
    "evidence_files": None,
    "created_at": datetime.now().isoformat(),
    "last_modified_at": datetime.now().isoformat(),
    "procurement_stage": "evaluation",
    "estimated_contract_value": 100000.00,
    "notes": "Phase 3 test assessment"
}

# Insert into BigQuery
print("=" * 60)
print("PHASE 3 TEST - INSERTING ASSESSMENT")
print("=" * 60)

storage = AssessmentStorage(dataset_id="procurement_assessments")

try:
    assessment_id = storage.insert_assessment(test_assessment)
    print(f"\nSUCCESS! Assessment {assessment_id} inserted into BigQuery")
    print(f"   Vendor: {test_assessment['vendor_name']}")
    print(f"   Total Readiness: {test_assessment['total_readiness_score']:.0%}")
    
except Exception as e:
    print(f"\nERROR: {e}")

print("=" * 60)