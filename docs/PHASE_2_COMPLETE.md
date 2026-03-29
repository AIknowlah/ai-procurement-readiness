# Phase 2: Question Bank Construction — COMPLETE ✅

**Date**: 29 March 2026  
**Status**: 90 Questions Generated & Validated

## What Was Built

- ✅ `question_bank.py` - Question schema (AnswerOption, Evidence, Question classes)
- ✅ `generate_questions.py` - Question generator (loads 90 checks, creates 90 questions)
- ✅ `question_bank.json` - Output file with all 90 assessment questions

## The 90 Questions

- P1 Transparency: 10 questions
- P2 Explainability: 1 question
- P3 Reproducibility: 15 questions
- P4 Safety: 9 questions
- P5 Security: 14 questions
- P6 Robustness: 7 questions
- P7 Fairness: 10 questions
- P8 Data Governance: 4 questions
- P9 Accountability: 11 questions
- P10 Human Agency & Oversight: 8 questions
- P11 Inclusive Growth: 1 question

**Total: 90 questions**

## Question Structure

Each question has:
- `question_id`: Q001 to Q090
- `pid`: Mapped to framework check (1.1.1, 1.2.1, etc.)
- `principle_number`: 1-11
- `principle_name`: Transparency, Safety, etc.
- `question_text`: The actual question
- `answer_options`: Have (1.0), Partial (0.5), Gap (0.0)
- `evidence`: What proof is needed
- `assessment_guidance`: How to score
- `governance_notes`: Why it matters

## How to Run
```bash
python src/phase2_question_bank/generate_questions.py
```

This generates `question_bank.json`.

## Key Features

✅ 1:1 mapping: Each question maps to exactly one framework check (PID)
✅ Consistent scoring: All questions use Have=1.0, Partial=0.5, Gap=0.0
✅ Evidence explicit: Every answer specifies what evidence is required
✅ Validated: All 90 questions pass validation with 0 errors

## What's Next

Phase 3: BigQuery schema + scoring logic