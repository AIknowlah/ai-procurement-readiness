"""
============================================================================
AI Procurement Readiness Tool - Scoring Calculator
============================================================================
Version: 1.0
Date: 2026-03-30
Purpose: Calculate readiness scores from assessment responses

GOVERNANCE SIGNIFICANCE:
Scoring must be reproducible and auditable.
Same responses = same score every time.
No subjective interpretation.

Formula: Readiness = (Have + 0.5 × Partial) / Total Checks
============================================================================
"""

from dataclasses import dataclass
from typing import List, Dict
import json


@dataclass
class PrincipleScore:
    """
    Represents readiness score for one AI Verify principle.
    
    Attributes:
        principle_number: Principle ID (1-11)
        principle_name: Human-readable name (e.g., "Transparency")
        total_checks: Total number of process checks for this principle
        have_count: Number of "Have" responses (full compliance)
        partial_count: Number of "Partial" responses (incomplete)
        gap_count: Number of "Gap" responses (not implemented)
        readiness_percentage: Calculated readiness (0.0 to 1.0)
        
    GOVERNANCE NOTE:
    This dataclass enforces that counts add up correctly.
    If have + partial + gap ≠ total, validation fails.
    """
    principle_number: int
    principle_name: str
    total_checks: int
    have_count: int
    partial_count: int
    gap_count: int
    readiness_percentage: float
    
    def __post_init__(self):
        """Validate that response counts match total checks."""
        total_responses = self.have_count + self.partial_count + self.gap_count
        
        if total_responses != self.total_checks:
            raise ValueError(
                f"Response counts ({total_responses}) don't match total checks ({self.total_checks}) "
                f"for {self.principle_name}"
            )
        
        # Validate readiness is in valid range
        if not 0.0 <= self.readiness_percentage <= 1.0:
            raise ValueError(
                f"Readiness percentage {self.readiness_percentage} is out of range [0.0, 1.0]"
            )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "principle_number": self.principle_number,
            "principle_name": self.principle_name,
            "total_checks": self.total_checks,
            "have_count": self.have_count,
            "partial_count": self.partial_count,
            "gap_count": self.gap_count,
            "readiness_percentage": self.readiness_percentage
        }


def calculate_principle_score(responses: List[Dict]) -> PrincipleScore:
    """
    Calculate readiness score for a single principle.
    
    Args:
        responses: List of Q&A pairs for this principle
                  Each response must have: principle_number, principle_name, answer
                  
    Returns:
        PrincipleScore object with all metrics
        
    Raises:
        ValueError: If responses list is empty or contains mixed principles
        
    Example:
        >>> responses = [
        ...     {"principle_number": 1, "principle_name": "Transparency", "answer": "Have"},
        ...     {"principle_number": 1, "principle_name": "Transparency", "answer": "Have"},
        ...     {"principle_number": 1, "principle_name": "Transparency", "answer": "Partial"},
        ...     {"principle_number": 1, "principle_name": "Transparency", "answer": "Gap"},
        ... ]
        >>> score = calculate_principle_score(responses)
        >>> score.readiness_percentage
        0.62  # (2 + 0.5×1) / 4 = 0.625 rounded to 0.62
        
    GOVERNANCE NOTES:
    - Uses official AI Verify formula: (Have + 0.5 × Partial) / Total
    - Rounding to 2 decimal places for consistency
    - Validates all responses are from same principle
    """
    if not responses:
        raise ValueError("Cannot calculate score for empty responses list")
    
    # Validate all responses are from same principle
    principle_numbers = set(r['principle_number'] for r in responses)
    if len(principle_numbers) > 1:
        raise ValueError(f"Responses contain mixed principles: {principle_numbers}")
    
    principle_names = set(r['principle_name'] for r in responses)
    if len(principle_names) > 1:
        raise ValueError(f"Responses contain mixed principle names: {principle_names}")
    
    # Count response types
    have_count = sum(1 for r in responses if r['answer'] == 'Have')
    partial_count = sum(1 for r in responses if r['answer'] == 'Partial')
    gap_count = sum(1 for r in responses if r['answer'] == 'Gap')
    total_checks = len(responses)
    
    # Calculate readiness using AI Verify formula
    # Have = 1.0 points, Partial = 0.5 points, Gap = 0.0 points
    readiness = (have_count + 0.5 * partial_count) / total_checks if total_checks > 0 else 0.0
    
    # Round to 2 decimal places for consistency
    readiness = round(readiness, 2)
    
    return PrincipleScore(
        principle_number=responses[0]['principle_number'],
        principle_name=responses[0]['principle_name'],
        total_checks=total_checks,
        have_count=have_count,
        partial_count=partial_count,
        gap_count=gap_count,
        readiness_percentage=readiness
    )


def calculate_all_principle_scores(all_responses: List[Dict]) -> Dict[str, PrincipleScore]:
    """
    Calculate scores for all 11 principles from complete assessment.
    
    Args:
        all_responses: List of all 90 Q&A pairs from assessment
        
    Returns:
        Dictionary mapping principle keys to PrincipleScore objects
        Example: {"P1_Transparency": PrincipleScore(...), "P2_Explainability": ...}
        
    Raises:
        ValueError: If responses don't cover all 11 principles
        
    GOVERNANCE NOTES:
    - Validates that all 11 principles are present
    - Groups responses by principle automatically
    - Returns structured results for audit trail
    """
    # Group responses by principle
    responses_by_principle = {}
    
    for response in all_responses:
        principle_num = response['principle_number']
        principle_name = response['principle_name']
        
        # Create principle key (e.g., "P1_Transparency")
        principle_key = f"P{principle_num}_{principle_name.replace(' ', '')}"
        
        if principle_key not in responses_by_principle:
            responses_by_principle[principle_key] = []
        
        responses_by_principle[principle_key].append(response)
    
    # Validate we have all 11 principles
    if len(responses_by_principle) != 11:
        raise ValueError(
            f"Expected responses for 11 principles, got {len(responses_by_principle)}. "
            f"Principles present: {list(responses_by_principle.keys())}"
        )
    
    # Calculate score for each principle
    principle_scores = {}
    
    for principle_key, responses in responses_by_principle.items():
        principle_scores[principle_key] = calculate_principle_score(responses)
    
    return principle_scores


def calculate_total_readiness(principle_scores: Dict[str, PrincipleScore]) -> float:
    """
    Calculate overall readiness score (average of all principle scores).
    
    Args:
        principle_scores: Dictionary of PrincipleScore objects for all principles
        
    Returns:
        Overall readiness score (0.0 to 1.0)
        
    Example:
        >>> # If P1=0.80, P2=1.00, P3=0.90, ..., P11=0.85
        >>> total = calculate_total_readiness(principle_scores)
        >>> total
        0.87  # Average of all 11 principle scores
        
    GOVERNANCE NOTES:
    - Simple average (not weighted) - all principles equally important
    - Aligns with AI Verify framework guidance
    - Rounded to 2 decimal places
    """
    if not principle_scores:
        raise ValueError("Cannot calculate total readiness from empty principle scores")
    
    if len(principle_scores) != 11:
        raise ValueError(f"Expected 11 principle scores, got {len(principle_scores)}")
    
    total_score = sum(score.readiness_percentage for score in principle_scores.values())
    average_score = total_score / len(principle_scores)
    
    return round(average_score, 2)


def generate_principle_scores_json(principle_scores: Dict[str, PrincipleScore]) -> Dict[str, float]:
    """
    Generate JSON-compatible principle scores for BigQuery storage.
    
    Args:
        principle_scores: Dictionary of PrincipleScore objects
        
    Returns:
        Dictionary mapping principle keys to readiness percentages
        Example: {"P1_Transparency": 0.80, "P2_Explainability": 1.00, ...}
        
    GOVERNANCE NOTES:
    - This format matches BigQuery JSON column structure
    - Enables easy querying: WHERE principle_scores.P1_Transparency >= 0.8
    """
    return {
        principle_key: score.readiness_percentage
        for principle_key, score in principle_scores.items()
    }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Sample assessment with 4 questions from P1 Transparency
    sample_responses = [
        {
            "question_id": "Q001",
            "pid": "1.1.1",
            "principle_number": 1,
            "principle_name": "Transparency",
            "question_text": "Does the vendor align with PDPC guidelines?",
            "answer": "Have",
            "score": 1.0
        },
        {
            "question_id": "Q002",
            "pid": "1.1.2",
            "principle_number": 1,
            "principle_name": "Transparency",
            "question_text": "Does the vendor maintain transparency measures?",
            "answer": "Have",
            "score": 1.0
        },
        {
            "question_id": "Q003",
            "pid": "1.2.1",
            "principle_number": 1,
            "principle_name": "Transparency",
            "question_text": "Does the vendor document model architecture?",
            "answer": "Partial",
            "score": 0.5
        },
        {
            "question_id": "Q004",
            "pid": "1.2.2",
            "principle_number": 1,
            "principle_name": "Transparency",
            "question_text": "Does the vendor disclose data sources?",
            "answer": "Gap",
            "score": 0.0
        }
    ]
    
    # Calculate score for P1
    p1_score = calculate_principle_score(sample_responses)
    
    print("=" * 60)
    print("SAMPLE PRINCIPLE SCORE CALCULATION")
    print("=" * 60)
    print(f"Principle: {p1_score.principle_name} (P{p1_score.principle_number})")
    print(f"Total Checks: {p1_score.total_checks}")
    print(f"  - Have: {p1_score.have_count}")
    print(f"  - Partial: {p1_score.partial_count}")
    print(f"  - Gap: {p1_score.gap_count}")
    print(f"\nReadiness: {p1_score.readiness_percentage:.0%}")
    print(f"Calculation: ({p1_score.have_count} + 0.5 × {p1_score.partial_count}) / {p1_score.total_checks}")
    print(f"           = ({p1_score.have_count} + {0.5 * p1_score.partial_count}) / {p1_score.total_checks}")
    print(f"           = {p1_score.have_count + 0.5 * p1_score.partial_count} / {p1_score.total_checks}")
    print(f"           = {p1_score.readiness_percentage}")
    print("=" * 60)
