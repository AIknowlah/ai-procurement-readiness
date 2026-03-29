# AI Procurement Readiness Tool

Singapore government agencies evaluate vendor AI systems against 11 AI Verify principles.

## Project Status

### Phase 1: Framework Extraction ✅
- Extracted 90 process checks from official AI Verify GitHub
- Fixed P9 Accountability parsing issue
- Deliverable: `framework_structure_complete.json`

### Phase 2: Question Bank Construction ✅
- Generated 90 assessment questions (Q001-Q090)
- Each question mapped 1:1 to framework check (PID)
- Standardized scoring: Have=1.0, Partial=0.5, Gap=0.0
- Deliverable: `question_bank.json`

### Phase 3: Scoring & BigQuery Schema ⏳
- BigQuery schema for assessments
- Scoring algorithm (Have/Partial/Gap → readiness %)
- Audit trail logging

### Phase 4: LangGraph Workflow ⏳
- Assessment state machine
- Question-by-question flow
- HITL review gate
- Gemini integration (narrative generation)

### Phase 5: Word Report Generation ⏳
- Readiness scorecard
- Principle-by-principle summary
- Professional Word document output

### Phase 6: Streamlit UI ⏳
- Web interface for assessors
- Evidence file upload
- Real-time scoring display

## Tech Stack

- Python 3.11+
- LangGraph (workflow orchestration)
- Google Gemini API (AI)
- Google BigQuery (audit trail, asia-southeast1)
- python-docx (Word report generation)
- Streamlit (web UI)

## How to Run Phase 2
```bash
python src/phase2_question_bank/generate_questions.py
```

Generates `question_bank.json` with 90 assessment questions.

## Project Structure
```
src/
├── phase1_framework/
│   ├── extract_aiverify_framework.py
│   └── __init__.py
└── phase2_question_bank/
    ├── question_bank.py
    ├── generate_questions.py
    └── __init__.py

docs/
└── PHASE_2_COMPLETE.md

README.md
.gitignore
```

## Governance

- Framework extracted from official IMDA AI Verify source
- All questions mapped to framework checks (audit trail)
- Scoring standardized across all questions
- Every assessment logged to BigQuery (immutable append-only)

## Author

AIknowlah - Learning AI Governance through hands-on project work

Singapore | 2026
```

Save the file.

---

## **Step 4: Create `.gitignore`**

Create a new file called `.gitignore` in your root folder:
```
# Generated outputs
question_bank.json
*.pyc
__pycache__/
.env
venv/
.DS_Store