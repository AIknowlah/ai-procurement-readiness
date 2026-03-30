"""
============================================================================
AI Procurement Readiness Tool - LangGraph Workflow
============================================================================
Version: 1.0
Date: 2026-03-30
Purpose: Complete assessment workflow using LangGraph state machine

LEARNING NOTE:
This file connects all the nodes (workers) into a workflow (assembly line).

WORKFLOW FLOW:
START → Load Questions → Question Loop (90x) → HITL Review → Store → END

The "Question Loop" repeats:
  Present Question → Collect Answer → (repeat until all 90 done)

After 90 questions, we calculate scores, get human approval, and store.
============================================================================
"""

from langgraph.graph import StateGraph, END
from assessment_state import AssessmentState, create_initial_state
from assessment_nodes import (
    load_questions_node,
    present_question_node,
    collect_answer_node,
    calculate_scores_node,
    hitl_review_node,
    store_results_node,
    completion_node
)


def should_continue_questions(state: AssessmentState) -> str:
    """
    Decide whether to continue asking questions or move to review.
    
    Args:
        state: Current assessment state
        
    Returns:
        "present_question" if more questions remain
        "calculate_scores" if all questions answered
        
    LEARNING NOTE:
    This is a "routing function" - it decides which node to go to next.
    LangGraph calls this after each question to decide: loop or exit?
    """
    # Check if we've answered all questions
    if state['current_question_index'] >= len(state['questions']):
        print(f"\n[ROUTER] All {len(state['questions'])} questions answered! Moving to scoring...")
        return "calculate_scores"
    else:
        remaining = len(state['questions']) - state['current_question_index']
        print(f"\n[ROUTER] {remaining} questions remaining. Continuing...")
        return "present_question"


def create_assessment_workflow() -> StateGraph:
    """
    Create the complete LangGraph workflow for AI procurement assessment.
    
    Returns:
        Compiled StateGraph ready to execute
        
    WORKFLOW STRUCTURE:
    
    START
      ↓
    load_questions ────────────────┐
      ↓                             │
    present_question ←──────────────┘
      ↓                             │
    collect_answer ─────────────────┤
      ↓                             │
    (routing: more questions?) ─────┘
      ↓
    calculate_scores
      ↓
    hitl_review
      ↓
    store_results
      ↓
    completion
      ↓
    END
    
    GOVERNANCE NOTE:
    The workflow ensures:
    1. All questions are asked in order
    2. All answers are collected and scored
    3. Human review happens before storage
    4. Results are permanently stored in BigQuery
    """
    
    # Create the graph
    workflow = StateGraph(AssessmentState)
    
    # ========================================================================
    # ADD NODES (the workers)
    # ========================================================================
    
    workflow.add_node("load_questions", load_questions_node)
    workflow.add_node("present_question", present_question_node)
    workflow.add_node("collect_answer", collect_answer_node)
    workflow.add_node("calculate_scores", calculate_scores_node)
    workflow.add_node("hitl_review", hitl_review_node)
    workflow.add_node("store_results", store_results_node)
    workflow.add_node("completion", completion_node)
    
    # ========================================================================
    # ADD EDGES (the connections between workers)
    # ========================================================================
    
    # Start by loading questions
    workflow.set_entry_point("load_questions")
    
    # After loading questions, present first question
    workflow.add_edge("load_questions", "present_question")
    
    # After presenting question, collect answer
    workflow.add_edge("present_question", "collect_answer")
    
    # After collecting answer, decide: more questions or done?
    # This is CONDITIONAL ROUTING - the workflow branches based on state
    workflow.add_conditional_edges(
        "collect_answer",
        should_continue_questions,
        {
            "present_question": "present_question",  # Loop back for next question
            "calculate_scores": "calculate_scores"   # All done, move to scoring
        }
    )
    
    # After calculating scores, go to HITL review
    workflow.add_edge("calculate_scores", "hitl_review")
    
    # After HITL approval, store results
    workflow.add_edge("hitl_review", "store_results")
    
    # After storing, mark as complete
    workflow.add_edge("store_results", "completion")
    
    # After completion, end the workflow
    workflow.add_edge("completion", END)
    
    # ========================================================================
    # COMPILE THE GRAPH
    # ========================================================================
    
    compiled_workflow = workflow.compile()
    
    return compiled_workflow


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_assessment(
    assessment_id: str,
    vendor_name: str,
    assessor_id: str,
    system_name: str = None,
    system_description: str = None,
    assessor_agency: str = None,
    procurement_stage: str = None,
    estimated_contract_value: float = None,
    notes: str = None
):
    """
    Run a complete assessment workflow.
    
    Args:
        assessment_id: Unique identifier (e.g., "ASM-2026-001")
        vendor_name: Name of vendor being assessed
        assessor_id: Government officer ID
        system_name: AI system name (optional)
        system_description: What the system does (optional)
        assessor_agency: Officer's agency (optional)
        procurement_stage: Procurement stage (optional)
        estimated_contract_value: Contract value in SGD (optional)
        notes: Additional notes (optional)
        
    Returns:
        Final state after workflow completion
        
    Example:
        >>> final_state = run_assessment(
        ...     assessment_id="ASM-2026-001",
        ...     vendor_name="Example AI Corp",
        ...     assessor_id="officer_chan_123",
        ...     assessor_agency="GovTech Singapore"
        ... )
        >>> print(final_state['total_readiness_score'])
        0.85
    """
    
    print("\n" + "=" * 60)
    print("AI PROCUREMENT READINESS ASSESSMENT - STARTING")
    print("=" * 60)
    
    # Create initial state
    initial_state = create_initial_state(
        assessment_id=assessment_id,
        vendor_name=vendor_name,
        assessor_id=assessor_id,
        system_name=system_name,
        system_description=system_description,
        assessor_agency=assessor_agency,
        procurement_stage=procurement_stage,
        estimated_contract_value=estimated_contract_value,
        notes=notes
    )
    
    # Create workflow
    workflow = create_assessment_workflow()
    
    # Run the workflow
    print("\n[WORKFLOW] Starting execution...")
    final_state = workflow.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("WORKFLOW EXECUTION COMPLETE")
    print("=" * 60)
    
    return final_state


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Run a test assessment
    final_state = run_assessment(
        assessment_id="ASM-2026-WORKFLOW-TEST",
        vendor_name="Test AI Vendor",
        system_name="AI Document Classifier",
        system_description="Automated document classification system for government records",
        assessor_id="officer_test_123",
        assessor_agency="Test Government Agency",
        procurement_stage="evaluation",
        estimated_contract_value=250000.00,
        notes="Phase 4 workflow test - simulated responses"
    )
    
    # Display results
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Assessment ID: {final_state['assessment_id']}")
    print(f"Vendor: {final_state['vendor_name']}")
    print(f"Questions Answered: {len(final_state['responses'])}")
    print(f"Total Readiness: {final_state['total_readiness_score']:.0%}")
    print(f"Status: {final_state['assessment_status']}")
    print(f"Workflow Stage: {final_state['workflow_stage']}")
    print(f"\nPrinciple Scores:")
    for principle, score in final_state['principle_scores'].items():
        print(f"  {principle}: {score:.0%}")
    print("=" * 60)
