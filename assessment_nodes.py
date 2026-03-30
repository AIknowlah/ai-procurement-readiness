"""
============================================================================
AI Procurement Readiness Tool - LangGraph Nodes
============================================================================
Version: 1.0
Date: 2026-03-30
Purpose: Individual nodes that make up the assessment workflow

LEARNING NOTE:
Each node is a Python function that:
1. Takes the current state as input
2. Does some work (load data, ask question, calculate score)
3. Returns updated state

Nodes are the "workers" in your workflow.
============================================================================
"""

import json
from typing import Dict
from datetime import datetime
from assessment_state import AssessmentState
from scoring_calculator import (
    calculate_all_principle_scores,
    calculate_total_readiness,
    generate_principle_scores_json
)
from bigquery_storage import AssessmentStorage


# ============================================================================
# NODE 1: LOAD QUESTIONS
# ============================================================================

def load_questions_node(state: AssessmentState) -> AssessmentState:
    """
    Load all 90 questions from question_bank.json.
    
    Args:
        state: Current assessment state
        
    Returns:
        Updated state with questions loaded
        
    WHAT THIS NODE DOES:
    1. Opens question_bank.json
    2. Loads all 90 questions
    3. Stores them in state['questions']
    4. Updates workflow_stage to 'loading_questions'
    
    GOVERNANCE NOTE:
    Questions come from official AI Verify framework.
    Using same question bank ensures consistency across all assessments.
    """
    print(f"\n[LOAD QUESTIONS] Loading question bank...")
    
    try:
        # Load question bank from file
        with open('question_bank.json', 'r') as f:
            question_bank = json.load(f)
        
        questions = question_bank.get('questions', [])
        
        print(f"[LOAD QUESTIONS] Loaded {len(questions)} questions")
        
        # Update state
        state['questions'] = questions
        state['workflow_stage'] = 'loading_questions'
        
        return state
        
    except Exception as e:
        print(f"[LOAD QUESTIONS] ERROR: {e}")
        state['workflow_stage'] = 'error'
        state['error_message'] = f"Failed to load questions: {e}"
        return state


# ============================================================================
# NODE 2: PRESENT QUESTION
# ============================================================================

def present_question_node(state: AssessmentState) -> AssessmentState:
    """
    Present the current question to the assessor.
    
    Args:
        state: Current assessment state
        
    Returns:
        Updated state with current_question set
        
    WHAT THIS NODE DOES:
    1. Gets current question index
    2. Retrieves that question from state['questions']
    3. Sets state['current_question']
    4. Displays question to assessor (in real UI, this would be on screen)
    
    LEARNING NOTE:
    In Phase 6 (Streamlit), this node would render the question in the UI.
    For now, we just print it and simulate the answer.
    """
    idx = state['current_question_index']
    
    # Check if we've finished all questions
    if idx >= len(state['questions']):
        print(f"\n[PRESENT QUESTION] All {len(state['questions'])} questions answered!")
        state['workflow_stage'] = 'hitl_review'
        state['current_question'] = None
        return state
    
    # Get current question
    question = state['questions'][idx]
    state['current_question'] = question
    state['workflow_stage'] = 'presenting_question'
    
    # Display question (in real UI, this would be rendered on screen)
    print(f"\n{'='*60}")
    print(f"QUESTION {idx + 1} of {len(state['questions'])}")
    print(f"{'='*60}")
    print(f"Principle: {question['principle_name']} (P{question['principle_number']})")
    print(f"Question ID: {question['question_id']}")
    print(f"PID: {question['pid']}")
    print(f"\n{question['question_text']}")
    print(f"\nAnswer Options: Have (1.0) | Partial (0.5) | Gap (0.0)")
    print(f"{'='*60}")
    
    return state


# ============================================================================
# NODE 3: COLLECT ANSWER (SIMULATED)
# ============================================================================

def collect_answer_node(state: AssessmentState) -> AssessmentState:
    """
    Collect answer from assessor for current question.
    
    Args:
        state: Current assessment state
        
    Returns:
        Updated state with answer recorded
        
    WHAT THIS NODE DOES:
    1. Wait for assessor to provide answer
    2. Collect evidence files (if any)
    3. Record the response
    4. Add to state['responses']
    5. Move to next question
    
    LEARNING NOTE:
    For Phase 4, we SIMULATE the answer (random/fixed responses).
    In Phase 6 (Streamlit), this would get real input from the UI form.
    
    GOVERNANCE NOTE:
    Every answer is timestamped and linked to evidence.
    This creates complete audit trail.
    """
    question = state['current_question']
    
    if question is None:
        print("[COLLECT ANSWER] ERROR: No current question!")
        state['workflow_stage'] = 'error'
        state['error_message'] = "No current question to answer"
        return state
    
    # SIMULATION: In real implementation, this would come from UI
    # For now, we'll simulate "Have" for most questions
    idx = state['current_question_index']
    
    # Simulate varied responses for demonstration
    if idx % 5 == 0:
        answer = "Partial"
        explanation = "Implementation is incomplete - some components missing"
        evidence_files = [f"partial_evidence_{question['question_id']}.pdf"]
    elif idx % 7 == 0:
        answer = "Gap"
        explanation = None
        evidence_files = []
    else:
        answer = "Have"
        explanation = None
        evidence_files = [f"evidence_{question['question_id']}.pdf"]
    
    # Map answer to score
    score_map = {"Have": 1.0, "Partial": 0.5, "Gap": 0.0}
    score = score_map[answer]
    
    print(f"\n[COLLECT ANSWER] Answer: {answer} (Score: {score})")
    if evidence_files:
        print(f"[COLLECT ANSWER] Evidence: {', '.join(evidence_files)}")
    if explanation:
        print(f"[COLLECT ANSWER] Explanation: {explanation}")
    
    # Create response record
    response = {
        "question_id": question['question_id'],
        "pid": question['pid'],
        "principle_number": question['principle_number'],
        "principle_name": question['principle_name'],
        "question_text": question['question_text'],
        "answer": answer,
        "score": score,
        "evidence_provided": len(evidence_files) > 0,
        "evidence_files": evidence_files,
        "explanation": explanation,
        "assessed_at": datetime.now().isoformat()
    }
    
    # Add to responses
    state['responses'].append(response)
    state['workflow_stage'] = 'collecting_answer'
    
    # Move to next question
    state['current_question_index'] += 1
    state['current_question'] = None
    state['current_answer'] = None
    state['current_evidence'] = None
    state['current_explanation'] = None
    
    return state


# ============================================================================
# NODE 4: CALCULATE SCORES
# ============================================================================

def calculate_scores_node(state: AssessmentState) -> AssessmentState:
    """
    Calculate readiness scores from all responses.
    
    Args:
        state: Current assessment state
        
    Returns:
        Updated state with scores calculated
        
    WHAT THIS NODE DOES:
    1. Takes all responses collected so far
    2. Groups them by principle
    3. Calculates score per principle
    4. Calculates total readiness score
    5. Stores in state
    
    GOVERNANCE NOTE:
    Scoring is deterministic and transparent.
    Formula: (Have + 0.5 × Partial) / Total
    Same inputs always produce same outputs.
    """
    print(f"\n[CALCULATE SCORES] Computing readiness scores...")
    
    if not state['responses']:
        print("[CALCULATE SCORES] No responses yet, skipping")
        return state
    
    try:
        # Calculate principle scores
        principle_scores = calculate_all_principle_scores(state['responses'])
        
        # Calculate total readiness
        total_readiness = calculate_total_readiness(principle_scores)
        
        # Convert to JSON format for storage
        principle_scores_json = generate_principle_scores_json(principle_scores)
        
        # Update state
        state['principle_scores'] = principle_scores_json
        state['total_readiness_score'] = total_readiness
        state['workflow_stage'] = 'calculating_score'
        
        print(f"[CALCULATE SCORES] Total Readiness: {total_readiness:.0%}")
        for principle, score in principle_scores_json.items():
            print(f"  {principle}: {score:.0%}")
        
        return state
        
    except Exception as e:
        print(f"[CALCULATE SCORES] ERROR: {e}")
        state['workflow_stage'] = 'error'
        state['error_message'] = f"Failed to calculate scores: {e}"
        return state


# ============================================================================
# NODE 5: HITL REVIEW (Human-in-the-Loop)
# ============================================================================

def hitl_review_node(state: AssessmentState) -> AssessmentState:
    """
    Human-in-the-loop review checkpoint.
    
    Args:
        state: Current assessment state
        
    Returns:
        Updated state with HITL approval status
        
    WHAT THIS NODE DOES:
    1. Displays assessment results to human reviewer
    2. Shows all scores and answers
    3. Waits for approval/rejection
    4. Records decision
    
    LEARNING NOTE:
    For Phase 4, we AUTO-APPROVE for testing.
    In Phase 6 (Streamlit), this would be a real review screen.
    
    GOVERNANCE NOTE:
    HITL gate ensures human oversight before finalizing assessment.
    Prevents automation errors from going undetected.
    """
    print(f"\n{'='*60}")
    print("HUMAN REVIEW CHECKPOINT")
    print(f"{'='*60}")
    print(f"Assessment ID: {state['assessment_id']}")
    print(f"Vendor: {state['vendor_name']}")
    print(f"Total Questions: {len(state['responses'])}")
    print(f"Total Readiness: {state['total_readiness_score']:.0%}")
    print(f"\nPrinciple Scores:")
    for principle, score in state['principle_scores'].items():
        print(f"  {principle}: {score:.0%}")
    print(f"{'='*60}")
    
    # SIMULATION: Auto-approve for Phase 4 testing
    # In real implementation, this would wait for human input
    print("\n[HITL REVIEW] AUTO-APPROVING for testing (Phase 6 will add real review)")
    
    state['hitl_approved'] = True
    state['workflow_stage'] = 'hitl_review'
    state['assessment_status'] = 'submitted'
    
    return state


# ============================================================================
# NODE 6: STORE RESULTS
# ============================================================================

def store_results_node(state: AssessmentState) -> AssessmentState:
    """
    Store completed assessment in BigQuery.
    
    Args:
        state: Current assessment state
        
    Returns:
        Updated state with storage confirmation
        
    WHAT THIS NODE DOES:
    1. Prepares assessment record for BigQuery
    2. Connects to BigQuery
    3. Inserts the record
    4. Confirms storage successful
    
    GOVERNANCE NOTE:
    This creates permanent, immutable audit record.
    Once stored, assessment cannot be modified (append-only).
    """
    print(f"\n[STORE RESULTS] Saving to BigQuery...")
    
    try:
        # Prepare assessment record
        assessment_record = {
            "assessment_id": state['assessment_id'],
            "vendor_name": state['vendor_name'],
            "system_name": state['system_name'],
            "system_description": state['system_description'],
            
            "assessment_date": datetime.now().isoformat(),
            "assessor_id": state['assessor_id'],
            "assessor_agency": state['assessor_agency'],
            "assessment_status": state['assessment_status'],
            
            "principle_scores": state['principle_scores'],
            "total_readiness_score": state['total_readiness_score'],
            
            "responses": state['responses'],
            "evidence_files": None,  # Would be populated with GCS paths in production
            
            "created_at": state['started_at'],
            "last_modified_at": datetime.now().isoformat(),
            
            "procurement_stage": state['procurement_stage'],
            "estimated_contract_value": state['estimated_contract_value'],
            "notes": state['notes']
        }
        
        # Store in BigQuery
        storage = AssessmentStorage(dataset_id="procurement_assessments")
        assessment_id = storage.insert_assessment(assessment_record)
        
        print(f"[STORE RESULTS] Successfully stored assessment: {assessment_id}")
        
        # Update state
        state['workflow_stage'] = 'storing_results'
        state['completed_at'] = datetime.now().isoformat()
        
        return state
        
    except Exception as e:
        print(f"[STORE RESULTS] ERROR: {e}")
        state['workflow_stage'] = 'error'
        state['error_message'] = f"Failed to store results: {e}"
        return state


# ============================================================================
# NODE 7: COMPLETION
# ============================================================================

def completion_node(state: AssessmentState) -> AssessmentState:
    """
    Final node - mark assessment as complete.
    
    Args:
        state: Current assessment state
        
    Returns:
        Final state
        
    WHAT THIS NODE DOES:
    1. Marks workflow as completed
    2. Displays summary
    3. Returns final state
    """
    print(f"\n{'='*60}")
    print("ASSESSMENT COMPLETE!")
    print(f"{'='*60}")
    print(f"Assessment ID: {state['assessment_id']}")
    print(f"Vendor: {state['vendor_name']}")
    print(f"Total Readiness: {state['total_readiness_score']:.0%}")
    print(f"Questions Answered: {len(state['responses'])}")
    print(f"Started: {state['started_at']}")
    print(f"Completed: {state['completed_at']}")
    print(f"{'='*60}")
    
    state['workflow_stage'] = 'completed'
    state['assessment_status'] = 'approved'
    
    return state


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    from assessment_state import create_initial_state
    
    print("=" * 60)
    print("TESTING INDIVIDUAL NODES")
    print("=" * 60)
    
    # Create initial state
    state = create_initial_state(
        assessment_id="ASM-TEST-NODES",
        vendor_name="Test Vendor Corp",
        assessor_id="test_officer",
        assessor_agency="Test Agency"
    )
    
    # Test Node 1: Load questions
    print("\n1. Testing load_questions_node...")
    # state = load_questions_node(state)  # Would need question_bank.json
    # print(f"   Questions loaded: {len(state['questions'])}")
    
    print("\nAll nodes defined successfully!")
    print("Next: Connect nodes in LangGraph workflow")
