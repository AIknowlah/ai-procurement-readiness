#!/usr/bin/env python3
"""
Question Bank Schema

This file defines what a question looks like.
Every assessment question must follow this structure.

Think of it like a template:
- question_id: Q001, Q002, etc.
- pid: 1.1.1 (maps to framework check)
- question_text: The actual question
- answer_options: Have, Partial, or Gap
- evidence: What proof is needed
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AnswerOption:
    """
    One answer choice: Have, Partial, or Gap.
    
    Example:
        AnswerOption(
            label="Have",
            score=1.0,
            description="Yes, complete implementation",
            evidence_required=True
        )
    """
    label: str
    score: float
    description: str
    evidence_required: bool = False
    requires_explanation: bool = False


@dataclass
class Evidence:
    """
    What evidence does the assessor need to provide?
    
    Example:
        Evidence(
            type="Internal documentation",
            examples=["Privacy Policy PDF", "Policy Document"],
            description="Documentary evidence of internal policy..."
        )
    """
    type: str
    examples: List[str]
    description: str


@dataclass
class Question:
    """
    A single assessment question.
    
    One question per process check (PID).
    Every question has 3 answer options: Have, Partial, Gap.
    
    Example:
        q = Question(
            question_id="Q001",
            pid="1.1.1",
            principle_number=1,
            principle_name="Transparency",
            question_text="Does the vendor have documented policies...?",
            answer_options={...},
            evidence={...},
            assessment_guidance="...",
            governance_notes="..."
        )
    """
    question_id: str
    pid: str
    principle_number: int
    principle_name: str
    question_text: str
    answer_options: Dict[str, AnswerOption]
    evidence: Evidence
    assessment_guidance: str
    governance_notes: str

    def to_dict(self) -> Dict:
        """
        Convert question to a dictionary (for JSON).
        
        Returns:
            Dictionary representation of the question
        """
        return {
            "question_id": self.question_id,
            "pid": self.pid,
            "principle_number": self.principle_number,
            "principle_name": self.principle_name,
            "question_text": self.question_text,
            "answer_options": {
                label: {
                    "label": option.label,
                    "score": option.score,
                    "description": option.description,
                    "evidence_required": option.evidence_required,
                    "requires_explanation": option.requires_explanation,
                }
                for label, option in self.answer_options.items()
            },
            "evidence": {
                "type": self.evidence.type,
                "examples": self.evidence.examples,
                "description": self.evidence.description,
            },
            "assessment_guidance": self.assessment_guidance,
            "governance_notes": self.governance_notes,
        }

if __name__ == "__main__":
    # Test: Create one example question
    example = Question(
        question_id="Q001",
        pid="1.1.1",
        principle_number=1,
        principle_name="Transparency",
        question_text="Does the vendor have documented internal policies aligned with PDPC guidelines?",
        answer_options={
            "Have": AnswerOption(
                label="Have",
                score=1.0,
                description="Yes, complete documentation provided",
                evidence_required=True,
            ),
            "Partial": AnswerOption(
                label="Partial",
                score=0.5,
                description="Partial implementation or incomplete documentation",
                evidence_required=True,
                requires_explanation=True,
            ),
            "Gap": AnswerOption(
                label="Gap",
                score=0.0,
                description="Not implemented or no evidence",
                evidence_required=False,
            ),
        },
        evidence=Evidence(
            type="Internal documentation",
            examples=["Privacy Policy PDF", "PDPA Compliance Statement"],
            description="Documentary evidence of internal policy aligned with PDPC guidelines",
        ),
        assessment_guidance="Review documented evidence that demonstrates compliance.",
        governance_notes="[P1 TRANSPARENCY] Essential for regulatory compliance.",
    )
    
    print("✅ Question created successfully!")
    print(f"Question ID: {example.question_id}")
    print(f"PID: {example.pid}")
    print(f"Question: {example.question_text}")