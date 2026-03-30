# ✅ PHASE 2 COMPLETE: Question Bank Generated

**Date**: 29 March 2026  
**Status**: 90 Questions Generated & Validated

---

## What You Built

### Input
- 90 process checks from `framework_structure_complete.json`
- Each check has: PID, criteria, process text, metric, description

### Output
- `question_bank.json` (178 KB, 3,792 lines)
- 90 Assessment Questions (Q001 to Q090)
- All questions validated and ready for Phase 3

---

## The 90 Questions

### By Principle

| Principle | Count | Sample Question |
|-----------|-------|-----------------|
| P1 Transparency | 10 | "Does the vendor align with PDPC's Advisory Guidelines...?" |
| P2 Explainability | 1 | "Does the vendor demonstrate preference for explainable models...?" |
| P3 Reproducibility | 15 | "Does the vendor record the provenance of AI models...?" |
| P4 Safety | 9 | "Does the vendor carry out assessment of materiality...?" |
| P5 Security | 14 | "Does the vendor ensure team competency in security...?" |
| P6 Robustness | 7 | "Does the vendor put in place measures to ensure data quality...?" |
| P7 Fairness | 10 | "Does the vendor assess within-group fairness...?" |
| P8 Data Governance | 4 | "Does the vendor put in place measures to ensure data quality...?" |
| P9 Accountability | 11 | "Does the vendor establish clear internal governance mechanisms...?" |
| P10 Human Agency & Oversight | 8 | "Does the vendor ensure parties involved in using/reviewing...?" |
| P11 Inclusive Growth | 1 | "Does the vendor ensure development of AI system for beneficial outcome...?" |
| **TOTAL** | **90** | — |

---

## Structure of Each Question

Every question follows the same structure:

```json
{
  "question_id": "Q001",
  "pid": "1.1.1",
  "principle_number": 1,
  "principle_name": "Transparency",
  "question_text": "Does the vendor align with (1) the PDPC's Advisory Guidelines...?",
  
  "answer_options": {
    "Have": {
      "label": "Have",
      "score": 1.0,
      "description": "Yes, complete implementation with evidence provided",
      "evidence_required": true,
      "requires_explanation": false
    },
    "Partial": {
      "label": "Partial",
      "score": 0.5,
      "description": "Partial implementation or incomplete documentation",
      "evidence_required": true,
      "requires_explanation": true
    },
    "Gap": {
      "label": "Gap",
      "score": 0.0,
      "description": "Not implemented or no evidence",
      "evidence_required": false,
      "requires_explanation": false
    }
  },
  
  "evidence": {
    "type": "Internal documentation (e.g., policy document)",
    "examples": ["Privacy Policy PDF", "PDPA Compliance Statement", "Policy Document"],
    "description": "Documentary evidence of internal policy..."
  },
  
  "assessment_guidance": "Review documented evidence that demonstrates compliance...",
  "governance_notes": "[P1 TRANSPARENCY] Essential for regulatory compliance..."
}
```

---

## Key Features

### 1. Question-to-PID Mapping (1:1)
Every question maps to exactly ONE process check (PID).

```
Q001 ↔ PID 1.1.1 ↔ Process Check
```

Score for Q001 = score for PID 1.1.1 in framework assessment.

### 2. Consistent Scoring
All 90 questions use the same 3-point scale:
- **Have** = 1.0 (complete)
- **Partial** = 0.5 (incomplete)
- **Gap** = 0.0 (not present)

No variations, no exceptions.

### 3. Clear Evidence Requirements
Every answer option specifies:
- Is evidence required?
- Must assessor explain their answer?

**Example:**
- Have: evidence required ✅ | explanation not required
- Partial: evidence required ✅ | explanation required (must explain gap)
- Gap: evidence not required | explanation optional

### 4. Assessment Guidance
Each question includes guidance on how assessors should evaluate answers.

Prevents subjective scoring. Ensures consistency across assessors.

### 5. Governance Notes
Each question includes notes explaining its importance and context.

**Example:**
> "[P1 TRANSPARENCY] Essential for regulatory compliance and user trust. Foundational principle for all AI systems in Singapore context."

---

## Validation Results

✅ **All 90 questions passed validation:**

- PID format correct (N.N.N)
- Principle numbers valid (1-11)
- Answer options present (Have, Partial, Gap)
- Scores correct (1.0, 0.5, 0.0)
- Evidence specified
- Guidance and notes present

No errors. No warnings. All questions ready for use.

---

## Files Created in Phase 2

### Code
```
src/phase2_question_bank/
├── question_bank.py            ← Schema & data classes (Step 1)
├── generate_questions.py        ← Question generator (Step 2)
└── __init__.py
```

### Output
```
question_bank.json              ← All 90 questions (machine-readable)
PHASE_2_COMPLETE.md            ← This summary
```

### Documentation
```
PHASE_2_OVERVIEW.md            ← What we're building
STEP_1_EXPLANATION.md          ← Schema explanation
```

---

## How This Works in Phase 3+

### Phase 3: Scoring & BigQuery Schema
Will use question_bank.json to:
1. Create BigQuery schema for assessments
2. Map answers to scores
3. Calculate readiness per principle
4. Store audit trail

### Phase 4: LangGraph Workflow
Will use question_bank.json to:
1. Load questions sequentially
2. Present to assessor
3. Collect answers & evidence
4. Score responses
5. Generate reports

### Phase 5: Word Report Generation
Will use question_bank.json to:
1. Group questions by principle
2. Show scores per principle
3. Generate readiness scorecard
4. Include assessment guidance (why each score)

---

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Total Questions | 90 | 90 | ✅ |
| PID Mapping | 1:1 | 1:1 | ✅ |
| Validation Errors | 0 | 0 | ✅ |
| Evidence Specs | 90 | 90 | ✅ |
| Assessment Guidance | 90 | 90 | ✅ |
| Governance Notes | 90 | 90 | ✅ |

All metrics met.

---

## What's Next (Phase 3)

Phase 3 will:
1. ✅ Load question_bank.json
2. ✅ Design BigQuery schema for assessments
3. ✅ Implement scoring logic
4. ✅ Create assessment storage

Timeline: 1-2 days

---

## Summary

✅ **PHASE 2 DELIVERED:**
- 90 assessment questions
- Mapped to 90 framework checks
- Validated & error-free
- Ready for operational use

This is the core of your procurement assessment tool. Every question traces back to the official AI Verify framework. Every assessment will be traceable, auditable, and governance-compliant.

**READY FOR PHASE 3!** 🚀

