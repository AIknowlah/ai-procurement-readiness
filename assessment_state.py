"""
============================================================================
AI Procurement Readiness Tool - Assessment State Structure
============================================================================
Version: 1.0
Date: 2026-03-30
Purpose: Define the state that flows through the LangGraph assessment workflow

LEARNING NOTE:
State is the "clipboard" that gets passed between nodes in the workflow.
Each node can READ from state and WRITE updates back to state.

GOVERNANCE SIGNIFICANCE:
State tracks complete audit trail: who, what, when, which questions answered.
This enables reproducibility and transparency.
============================================================================
"""

from typing import TypedDict, List, Dict, Optional, Literal
from datetime import datetime


class AssessmentState(TypedDict):
    """
    Complete state for an AI procurement assessment workflow.
    
    This state object flows through the entire LangGraph.
    Each node reads from it and writes updates back.
    
    WORKFLOW STAGES:
    1. Initialization: Load questions, set metadata
    2. Question Loop: Present Q, collect A, calculate score (repeat 90x)
    3. Review: HITL checkpoint
    4. Storage: Save to BigQuery
    5. Complete: Assessment finished
    
    ATTRIBUTES:
        Assessment Metadata:
            assessment_id: Unique identifier (e.g., "ASM-2026-001")
            vendor_name: Name of AI vendor being assessed
            system_name: Name of the AI system/product
            system_description: What the system does
            assessor_id: Government officer conducting assessment
            assessor_agency: Officer's agency
            assessment_status: Current status (draft/submitted/reviewed/approved)
            
        Question Management:
            questions: All 90 questions from question_bank.json
            current_question_index: Which question we're on (0-89)
            current_question: The question being asked right now
            
        Response Collection:
            responses: List of all Q&A pairs collected so far
            current_answer: Answer to current question
            current_evidence: Evidence files for current question
            
        Scoring:
            principle_scores: Readiness score per principle (P1-P11)
            total_readiness_score: Overall readiness (average of all principles)
            
        Workflow Control:
            workflow_stage: Where we are in the process
            hitl_approved: Whether human reviewer approved results
            error_message: Any errors encountered
            
        Timestamps:
            started_at: When assessment began
            completed_at: When assessment finished
    """
    
    # ========================================================================
    # ASSESSMENT METADATA
    # ========================================================================
    
    assessment_id: str
    """Unique assessment identifier (e.g., 'ASM-2026-001')"""
    
    vendor_name: str
    """Name of AI system vendor being assessed"""
    
    system_name: Optional[str]
    """Name of the AI system/product"""
    
    system_description: Optional[str]
    """Description of what the AI system does"""
    
    assessor_id: str
    """ID of government officer conducting assessment"""
    
    assessor_agency: Optional[str]
    """Government agency of the assessor"""
    
    assessment_status: Literal["draft", "in_progress", "review", "submitted", "approved"]
    """Current status of the assessment"""
    
    # ========================================================================
    # QUESTION MANAGEMENT
    # ========================================================================
    
    questions: List[Dict]
    """All 90 questions loaded from question_bank.json"""
    
    current_question_index: int
    """Index of current question (0-89)"""
    
    current_question: Optional[Dict]
    """The question currently being presented to assessor"""
    
    # ========================================================================
    # RESPONSE COLLECTION
    # ========================================================================
    
    responses: List[Dict]
    """
    All Q&A pairs collected so far.
    Each response contains:
    {
        "question_id": "Q001",
        "pid": "1.1.1",
        "principle_number": 1,
        "principle_name": "Transparency",
        "question_text": "Does the vendor...",
        "answer": "Have" | "Partial" | "Gap",
        "score": 1.0 | 0.5 | 0.0,
        "evidence_provided": True/False,
        "evidence_files": ["file1.pdf", "file2.pdf"],
        "explanation": "Optional explanation for Partial answers",
        "assessed_at": "2026-03-30T14:00:00Z"
    }
    """
    
    current_answer: Optional[str]
    """Answer to current question: 'Have', 'Partial', or 'Gap'"""
    
    current_evidence: Optional[List[str]]
    """Evidence files for current question"""
    
    current_explanation: Optional[str]
    """Explanation for Partial answers (required) or Gap (optional)"""
    
    # ========================================================================
    # SCORING
    # ========================================================================
    
    principle_scores: Dict[str, float]
    """
    Readiness score per principle.
    Example:
    {
        "P1_Transparency": 0.85,
        "P2_Explainability": 1.00,
        ...
        "P11_InclusiveGrowth": 0.90
    }
    """
    
    total_readiness_score: float
    """Overall readiness score (0.0 to 1.0) - average of all principle scores"""
    
    # ========================================================================
    # WORKFLOW CONTROL
    # ========================================================================
    
    workflow_stage: Literal[
        "initialized",
        "loading_questions",
        "presenting_question",
        "collecting_answer",
        "calculating_score",
        "hitl_review",
        "storing_results",
        "completed",
        "error"
    ]
    """Current stage in the workflow"""
    
    hitl_approved: bool
    """Whether human reviewer has approved the assessment results"""
    
    error_message: Optional[str]
    """Error message if something went wrong"""
    
    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    
    started_at: str
    """ISO 8601 timestamp when assessment began"""
    
    completed_at: Optional[str]
    """ISO 8601 timestamp when assessment finished"""
    
    # ========================================================================
    # ADDITIONAL CONTEXT
    # ========================================================================
    
    procurement_stage: Optional[str]
    """Stage of procurement: planning, evaluation, pre-award, post-award"""
    
    estimated_contract_value: Optional[float]
    """Estimated contract value in SGD"""
    
    notes: Optional[str]
    """Additional notes from assessor"""


def create_initial_state(
    assessment_id: str,
    vendor_name: str,
    assessor_id: str,
    system_name: Optional[str] = None,
    system_description: Optional[str] = None,
    assessor_agency: Optional[str] = None,
    procurement_stage: Optional[str] = None,
    estimated_contract_value: Optional[float] = None,
    notes: Optional[str] = None
) -> AssessmentState:
    """
    Create initial state for a new assessment.
    
    Args:
        assessment_id: Unique identifier for this assessment
        vendor_name: Name of vendor being assessed
        assessor_id: ID of government officer
        system_name: Name of AI system (optional)
        system_description: What the system does (optional)
        assessor_agency: Officer's agency (optional)
        procurement_stage: Stage in procurement (optional)
        estimated_contract_value: Contract value in SGD (optional)
        notes: Additional context (optional)
        
    Returns:
        AssessmentState initialized and ready for workflow
        
    Example:
        >>> state = create_initial_state(
        ...     assessment_id="ASM-2026-001",
        ...     vendor_name="Example AI Corp",
        ...     assessor_id="officer_chan_123",
        ...     assessor_agency="GovTech Singapore"
        ... )
        >>> state['workflow_stage']
        'initialized'
    """
    return AssessmentState(
        # Metadata
        assessment_id=assessment_id,
        vendor_name=vendor_name,
        system_name=system_name,
        system_description=system_description,
        assessor_id=assessor_id,
        assessor_agency=assessor_agency,
        assessment_status="draft",
        
        # Questions (to be loaded)
        questions=[],
        current_question_index=0,
        current_question=None,
        
        # Responses (to be collected)
        responses=[],
        current_answer=None,
        current_evidence=None,
        current_explanation=None,
        
        # Scores (to be calculated)
        principle_scores={},
        total_readiness_score=0.0,
        
        # Workflow control
        workflow_stage="initialized",
        hitl_approved=False,
        error_message=None,
        
        # Timestamps
        started_at=datetime.now().isoformat(),
        completed_at=None,
        
        # Additional context
        procurement_stage=procurement_stage,
        estimated_contract_value=estimated_contract_value,
        notes=notes
    )


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ASSESSMENT STATE STRUCTURE - EXAMPLE")
    print("=" * 60)
    
    # Create initial state
    state = create_initial_state(
        assessment_id="ASM-2026-001",
        vendor_name="Example AI Corp",
        assessor_id="officer_chan_123",
        system_name="SmartDoc Analyzer",
        system_description="AI document classification system",
        assessor_agency="GovTech Singapore",
        procurement_stage="evaluation",
        estimated_contract_value=500000.00
    )
    
    print("\nInitial State Created:")
    print(f"  Assessment ID: {state['assessment_id']}")
    print(f"  Vendor: {state['vendor_name']}")
    print(f"  System: {state['system_name']}")
    print(f"  Assessor: {state['assessor_id']}")
    print(f"  Agency: {state['assessor_agency']}")
    print(f"  Workflow Stage: {state['workflow_stage']}")
    print(f"  Status: {state['assessment_status']}")
    print(f"  Questions Loaded: {len(state['questions'])}")
    print(f"  Responses Collected: {len(state['responses'])}")
    print(f"  Started At: {state['started_at']}")
    
    print("\n" + "=" * 60)
    print("This state will flow through all LangGraph nodes!")
    print("=" * 60)
