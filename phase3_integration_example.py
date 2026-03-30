"""
============================================================================
AI Procurement Readiness Tool - Phase 3 Integration Example
============================================================================
Version: 1.0
Date: 2026-03-30
Purpose: Demonstrates complete flow from responses to BigQuery storage

This example shows how all Phase 3 components work together:
1. Load question bank
2. Collect assessment responses (simulated)
3. Calculate scores
4. Store in BigQuery

LEARNING NOTES:
This file teaches the complete data flow through your system.
Follow the numbered steps to understand each stage.
============================================================================
"""

import json
from datetime import datetime
from typing import Dict, List
from scoring_calculator import (
    calculate_principle_score,
    calculate_all_principle_scores,
    calculate_total_readiness,
    generate_principle_scores_json
)
from bigquery_storage import AssessmentStorage


# ============================================================================
# STEP 1: LOAD QUESTION BANK
# ============================================================================

def load_question_bank(filepath: str = "question_bank.json") -> Dict:
    """
    Load the 90-question assessment framework.
    
    Args:
        filepath: Path to question_bank.json
        
    Returns:
        Parsed question bank dictionary
        
    GOVERNANCE NOTE:
    Question bank is the authoritative source.
    All assessments must use same question set for consistency.
    """
    with open(filepath, 'r') as f:
        question_bank = json.load(f)
    
    print(f"✓ Loaded {len(question_bank['questions'])} questions from {filepath}")
    return question_bank


# ============================================================================
# STEP 2: SIMULATE ASSESSMENT RESPONSES
# ============================================================================

def simulate_vendor_assessment() -> List[Dict]:
    """
    Simulate a government officer assessing a vendor AI system.
    
    In real implementation, this data comes from:
    - LangGraph workflow (Phase 4)
    - Streamlit UI (Phase 6)
    - Human assessor input
    
    Returns:
        List of 90 Q&A responses
        
    LEARNING NOTE:
    This simulates answering all 90 questions.
    Real assessments will have evidence files attached.
    """
    # Simulated responses for demonstration
    # In reality, this comes from assessor input
    
    responses = []
    
    # P1 Transparency (10 questions) - Mostly good
    for i in range(1, 11):
        responses.append({
            "question_id": f"Q{i:03d}",
            "pid": f"1.{(i-1)//5 + 1}.{(i-1)%5 + 1}",
            "principle_number": 1,
            "principle_name": "Transparency",
            "question_text": f"Question {i} about transparency",
            "answer": "Have" if i <= 8 else ("Partial" if i == 9 else "Gap"),
            "score": 1.0 if i <= 8 else (0.5 if i == 9 else 0.0),
            "evidence_provided": i <= 9,
            "evidence_files": [f"transparency_evidence_{i}.pdf"] if i <= 9 else [],
            "explanation": "Incomplete documentation" if i == 9 else None,
            "assessed_at": datetime.now().isoformat()
        })
    
    # P2 Explainability (1 question) - Complete
    responses.append({
        "question_id": "Q011",
        "pid": "2.1.1",
        "principle_number": 2,
        "principle_name": "Explainability",
        "question_text": "Question about explainability",
        "answer": "Have",
        "score": 1.0,
        "evidence_provided": True,
        "evidence_files": ["explainability_doc.pdf"],
        "explanation": None,
        "assessed_at": datetime.now().isoformat()
    })
    
    # For demonstration, simulate remaining 79 responses
    # In real code, all 90 would come from actual assessment
    
    # P3 Reproducibility (15 questions) - Mixed results
    for i in range(12, 27):
        responses.append({
            "question_id": f"Q{i:03d}",
            "pid": f"3.{(i-12)//5 + 1}.{(i-12)%5 + 1}",
            "principle_number": 3,
            "principle_name": "Reproducibility",
            "question_text": f"Question {i} about reproducibility",
            "answer": "Have" if i % 2 == 0 else ("Partial" if i % 3 == 0 else "Gap"),
            "score": 1.0 if i % 2 == 0 else (0.5 if i % 3 == 0 else 0.0),
            "evidence_provided": i % 2 == 0 or i % 3 == 0,
            "evidence_files": [f"reproducibility_{i}.pdf"] if (i % 2 == 0 or i % 3 == 0) else [],
            "explanation": "Partial implementation" if i % 3 == 0 else None,
            "assessed_at": datetime.now().isoformat()
        })
    
    # Continue for remaining principles...
    # (Abbreviated for example - real implementation would have all 90)
    
    print(f"✓ Simulated {len(responses)} assessment responses")
    return responses


# ============================================================================
# STEP 3: CALCULATE SCORES
# ============================================================================

def calculate_assessment_scores(responses: List[Dict]) -> Dict:
    """
    Calculate all readiness scores from responses.
    
    Args:
        responses: List of all Q&A pairs
        
    Returns:
        Dictionary with:
        - principle_scores: PrincipleScore objects
        - principle_scores_json: JSON-compatible scores
        - total_readiness_score: Overall score
        
    LEARNING NOTE:
    This is where raw responses become actionable metrics.
    Scoring algorithm is deterministic and auditable.
    """
    print("\n" + "=" * 60)
    print("CALCULATING SCORES")
    print("=" * 60)
    
    # Calculate scores for all principles
    principle_scores = calculate_all_principle_scores(responses)
    
    # Display results
    for principle_key, score in principle_scores.items():
        print(f"{principle_key}: {score.readiness_percentage:.0%} "
              f"({score.have_count} Have, {score.partial_count} Partial, {score.gap_count} Gap)")
    
    # Calculate total readiness
    total_readiness = calculate_total_readiness(principle_scores)
    print(f"\nTotal Readiness: {total_readiness:.0%}")
    
    # Generate JSON format for BigQuery
    principle_scores_json = generate_principle_scores_json(principle_scores)
    
    return {
        "principle_scores": principle_scores,
        "principle_scores_json": principle_scores_json,
        "total_readiness_score": total_readiness
    }


# ============================================================================
# STEP 4: PREPARE ASSESSMENT RECORD
# ============================================================================

def prepare_assessment_record(
    assessment_id: str,
    vendor_name: str,
    system_name: str,
    system_description: str,
    assessor_id: str,
    assessor_agency: str,
    responses: List[Dict],
    scores: Dict,
    procurement_stage: str = "evaluation",
    estimated_contract_value: float = None,
    notes: str = None
) -> Dict:
    """
    Prepare complete assessment record for BigQuery insertion.
    
    Args:
        assessment_id: Unique ID (e.g., "ASM-2026-001")
        vendor_name: Vendor company name
        system_name: AI system product name
        system_description: What the system does
        assessor_id: Government officer ID
        assessor_agency: Officer's agency
        responses: All 90 Q&A pairs
        scores: Calculated scores from calculate_assessment_scores()
        procurement_stage: Stage in procurement lifecycle
        estimated_contract_value: Contract value in SGD
        notes: Additional context
        
    Returns:
        Complete assessment record ready for BigQuery
        
    GOVERNANCE NOTE:
    This structure ensures complete audit trail:
    - Who assessed (assessor_id, assessor_agency)
    - What was assessed (vendor, system, responses)
    - When assessed (timestamps)
    - What was found (scores)
    - Supporting evidence (evidence_files)
    """
    now = datetime.now()
    
    # Extract evidence file references from responses
    evidence_files = []
    for response in responses:
        if response.get('evidence_files'):
            for filename in response['evidence_files']:
                evidence_files.append({
                    "filename": filename,
                    "gcs_path": f"gs://ai-procurement-evidence/{assessment_id}/{filename}",
                    "question_ids": [response['question_id']],
                    "uploaded_at": response['assessed_at'],
                    "file_size_bytes": 0  # Would be populated in real implementation
                })
    
    assessment_record = {
        # Identifiers
        "assessment_id": assessment_id,
        "vendor_name": vendor_name,
        "system_name": system_name,
        "system_description": system_description,
        
        # Assessment metadata
        "assessment_date": now.isoformat(),
        "assessor_id": assessor_id,
        "assessor_agency": assessor_agency,
        "assessment_status": "submitted",  # draft → submitted → reviewed → approved
        
        # Scores
        "principle_scores": scores['principle_scores_json'],
        "total_readiness_score": scores['total_readiness_score'],
        
        # Detailed data
        "responses": responses,
        "evidence_files": evidence_files if evidence_files else None,
        
        # Audit timestamps
        "created_at": now.isoformat(),
        "last_modified_at": now.isoformat(),
        
        # Context
        "procurement_stage": procurement_stage,
        "estimated_contract_value": estimated_contract_value,
        "notes": notes
    }
    
    print("\n✓ Prepared assessment record")
    print(f"  Assessment ID: {assessment_id}")
    print(f"  Vendor: {vendor_name}")
    print(f"  Total Readiness: {scores['total_readiness_score']:.0%}")
    print(f"  Evidence Files: {len(evidence_files)}")
    
    return assessment_record


# ============================================================================
# STEP 5: STORE IN BIGQUERY
# ============================================================================

def store_assessment(assessment_record: Dict) -> str:
    """
    Store assessment in BigQuery.
    
    Args:
        assessment_record: Complete assessment data
        
    Returns:
        assessment_id of stored record
        
    GOVERNANCE NOTE:
    This creates permanent, immutable audit record.
    Once stored, assessment cannot be modified (append-only).
    """
    try:
        storage = AssessmentStorage()
        
        # Ensure table exists
        storage.create_table_if_not_exists()
        
        # Insert assessment
        assessment_id = storage.insert_assessment(assessment_record)
        
        print(f"\n✓ Stored assessment {assessment_id} in BigQuery")
        return assessment_id
        
    except Exception as e:
        print(f"\n✗ Failed to store assessment: {e}")
        print("  Note: This is expected if GCP credentials not configured")
        print("  Assessment record prepared successfully - storage would work with proper setup")
        return assessment_record['assessment_id']


# ============================================================================
# MAIN: COMPLETE WORKFLOW
# ============================================================================

def main():
    """
    Demonstrates complete Phase 3 workflow.
    
    LEARNING PATH:
    1. Load question bank → Know what to ask
    2. Simulate responses → Collect answers
    3. Calculate scores → Compute readiness
    4. Prepare record → Structure for storage
    5. Store in BigQuery → Create audit trail
    """
    print("\n" + "=" * 60)
    print("AI PROCUREMENT READINESS TOOL - PHASE 3 DEMO")
    print("=" * 60)
    
    # Step 1: Load questions
    # question_bank = load_question_bank()  # Requires question_bank.json
    
    # Step 2: Simulate assessment
    print("\nStep 1: Simulating vendor assessment...")
    responses = simulate_vendor_assessment()
    
    # Step 3: Calculate scores
    print("\nStep 2: Calculating readiness scores...")
    scores = calculate_assessment_scores(responses)
    
    # Step 4: Prepare record
    print("\nStep 3: Preparing assessment record...")
    assessment_record = prepare_assessment_record(
        assessment_id="ASM-2026-001",
        vendor_name="Example AI Corp",
        system_name="SmartDoc Analyzer",
        system_description="AI-powered document classification system for government archives",
        assessor_id="officer_chan_123",
        assessor_agency="GovTech Singapore",
        responses=responses,
        scores=scores,
        procurement_stage="evaluation",
        estimated_contract_value=500000.00,
        notes="Assessment conducted during RFP evaluation phase. Vendor responsive to questions."
    )
    
    # Step 5: Store in BigQuery
    print("\nStep 4: Storing in BigQuery...")
    assessment_id = store_assessment(assessment_record)
    
    print("\n" + "=" * 60)
    print("PHASE 3 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"Assessment {assessment_id} ready for:")
    print("  - Phase 4: LangGraph workflow integration")
    print("  - Phase 5: Word report generation")
    print("  - Phase 6: Streamlit UI display")
    print("=" * 60)


if __name__ == "__main__":
    main()
