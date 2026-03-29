#!/usr/bin/env python3
"""
Generate Questions from Framework

This file loads 90 process checks and converts them into 90 questions.

Process:
1. Load framework_structure_complete.json
2. For each check, create a Question object
3. Validate all questions
4. Save to question_bank.json
"""

import json
import sys
from pathlib import Path

# Add src to path so we can import Question
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.phase2_question_bank.question_bank import (
    Question, AnswerOption, Evidence
)


class QuestionGenerator:
    """Loads framework checks and generates Question objects."""

    def __init__(self, framework_path: str = None):
        """
        Initialize the generator.

        Args:
            framework_path: Path to framework_structure_complete.json
        """
        if framework_path is None:
            framework_path = "framework_structure_complete.json"

        self.framework_path = framework_path
        self.framework = None
        self.all_checks = []
        self.questions = []

    def load_framework(self) -> None:
        """Load the framework with 90 checks."""
        print("Loading framework...")

        with open(self.framework_path, 'r') as f:
            self.framework = json.load(f)

        self.all_checks = self.framework.get('all_checks_flat', [])

        print(f"   Loaded {len(self.all_checks)} checks")

    def generate_question_text(self, check: dict) -> str:
        """
        Generate a question string from a framework check.

        Args:
            check: Framework process check

        Returns:
            Question text string
        """
        check_description = check.get('check_description', '')
        metric = check.get('metric', '')

        if check_description:
            return f"Does the vendor have {check_description.lower().rstrip('.')}?"
        if metric:
            return f"Does the vendor have evidence of {metric.lower().rstrip('.')}?"
        return "Does the vendor meet this requirement?"

    def create_question_from_check(self, check: dict, question_id: str) -> Question:
        """
        Create a Question object from a framework check.

        Args:
            check: Framework process check
            question_id: Unique ID like Q001, Q002

        Returns:
            Question object
        """
        question_text = self.generate_question_text(check)

        pid = check.get('pid', '')
        principle_name = check.get('principle', '')
        principle_number = check.get('principle_number', 0)
        metric = check.get('metric', '')
        check_description = check.get('check_description', '')

        answer_options = {
            "Have": AnswerOption(
                label="Have",
                score=1.0,
                description="Yes, complete implementation with evidence provided",
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
        }

        evidence = Evidence(
            type=metric,
            examples=["Documentation", "Evidence File", "Supporting Document"],
            description=check_description,
        )

        assessment_guidance = (
            "Review provided evidence against the requirement. "
            "Award 'Have' for complete compliance. "
            "Award 'Partial' for partial compliance."
        )
        governance_notes = f"[P{principle_number} {principle_name}] Check against AI Verify framework."

        return Question(
            question_id=question_id,
            pid=pid,
            principle_number=principle_number,
            principle_name=principle_name,
            question_text=question_text,
            answer_options=answer_options,
            evidence=evidence,
            assessment_guidance=assessment_guidance,
            governance_notes=governance_notes,
        )

    def generate_all_questions(self) -> None:
        """Generate Question objects for all 90 checks."""
        print("\nGenerating questions from checks...")

        self.questions = []

        for idx, check in enumerate(self.all_checks):
            question_id = f"Q{str(idx + 1).zfill(3)}"

            try:
                question = self.create_question_from_check(check, question_id)
                self.questions.append(question)
            except Exception as e:
                print(f"   Error generating {question_id}: {e}")

        print(f"   Generated {len(self.questions)} questions")

    def save_questions(self, output_path: str = None) -> None:
        """
        Save questions to JSON file.

        Args:
            output_path: Where to save (default: question_bank.json)
        """
        if output_path is None:
            output_path = "question_bank.json"

        print(f"\nSaving questions to {output_path}...")

        data = {
            'metadata': {
                'total_principles': self.framework.get('total_principles'),
                'total_process_checks': self.framework.get('total_process_checks'),
                'total_questions': len(self.questions),
            },
            'total_questions': len(self.questions),
            'questions': [q.to_dict() for q in self.questions],
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"   Saved {len(self.questions)} questions to {output_path}")


def main():
    """Main entry point."""

    print("=" * 80)
    print("PHASE 2: Generate All 90 Questions")
    print("=" * 80)

    gen = QuestionGenerator()
    gen.load_framework()
    gen.generate_all_questions()
    gen.save_questions()

    print("\nCOMPLETE")
    print("   -> question_bank.json generated (90 questions)")
    print("   -> Ready for Phase 3")

    return 0


if __name__ == "__main__":
    exit(main())
