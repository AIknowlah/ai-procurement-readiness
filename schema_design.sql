-- ============================================================================
-- AI Procurement Readiness Tool - BigQuery Schema
-- ============================================================================
-- Version: 1.0
-- Date: 2026-03-30
-- Purpose: Store vendor AI system assessments with full audit trail
-- 
-- GOVERNANCE SIGNIFICANCE:
-- This schema implements append-only immutable storage for regulatory compliance.
-- Every assessment is a permanent record. No UPDATE or DELETE operations.
-- Audit trail includes: who assessed, when, what answers, what evidence.
-- ============================================================================

CREATE TABLE `ai-procurement-sg.procurement_assessment.assessments`
(
  -- PRIMARY IDENTIFIER
  assessment_id STRING NOT NULL OPTIONS(description="Unique assessment identifier (e.g., ASM-2026-001)"),
  
  -- VENDOR INFORMATION
  vendor_name STRING NOT NULL OPTIONS(description="Name of AI system vendor being assessed"),
  system_name STRING OPTIONS(description="Name of the AI system/product"),
  system_description STRING OPTIONS(description="Brief description of what the AI system does"),
  
  -- ASSESSMENT METADATA
  assessment_date TIMESTAMP NOT NULL OPTIONS(description="Date assessment was conducted"),
  assessor_id STRING NOT NULL OPTIONS(description="ID of government officer who conducted assessment"),
  assessor_agency STRING OPTIONS(description="Government agency of the assessor"),
  assessment_status STRING NOT NULL OPTIONS(description="Status: draft, submitted, reviewed, approved"),
  
  -- SCORING RESULTS
  -- Each principle gets a score between 0.0 (0% ready) and 1.0 (100% ready)
  -- Formula: (Have + 0.5 × Partial) / Total checks
  principle_scores JSON NOT NULL OPTIONS(description="JSON object with scores per principle {P1: 0.80, P2: 1.00, ...}"),
  total_readiness_score FLOAT64 NOT NULL OPTIONS(description="Overall readiness score (average of all principle scores)"),
  
  -- DETAILED RESPONSES
  -- Complete record of all 90 questions and answers
  responses JSON NOT NULL OPTIONS(description="Array of all Q&A pairs with evidence references"),
  
  -- EVIDENCE TRACKING
  -- References to uploaded evidence files (stored in GCS)
  evidence_files JSON OPTIONS(description="Array of evidence file metadata {filename, gcs_path, question_id}"),
  
  -- AUDIT TRAIL
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() OPTIONS(description="Record creation timestamp (immutable)"),
  last_modified_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() OPTIONS(description="Last modification timestamp"),
  
  -- ADDITIONAL CONTEXT
  procurement_stage STRING OPTIONS(description="Stage of procurement: planning, evaluation, pre-award, post-award"),
  estimated_contract_value FLOAT64 OPTIONS(description="Estimated contract value in SGD (for materiality assessment)"),
  notes STRING OPTIONS(description="Additional notes or context from assessor")
)
PARTITION BY DATE(assessment_date)
CLUSTER BY vendor_name, assessment_status
OPTIONS(
  description="Vendor AI system assessments against IMDA AI Verify framework (90 process checks)",
  labels=[("env", "production"), ("project", "ai-procurement-tool"), ("region", "sg")]
);

-- ============================================================================
-- INDEXES (for query performance)
-- ============================================================================
-- BigQuery automatically indexes partitioned and clustered columns
-- Queries filtering by assessment_date, vendor_name, or assessment_status will be fast

-- ============================================================================
-- SAMPLE RECORD STRUCTURE
-- ============================================================================
-- {
--   "assessment_id": "ASM-2026-001",
--   "vendor_name": "Example AI Corp",
--   "system_name": "SmartDoc Analyzer",
--   "system_description": "Document classification AI for government archives",
--   "assessment_date": "2026-03-30T14:00:00Z",
--   "assessor_id": "officer_chan_123",
--   "assessor_agency": "GovTech Singapore",
--   "assessment_status": "submitted",
--   
--   "principle_scores": {
--     "P1_Transparency": 0.80,
--     "P2_Explainability": 1.00,
--     "P3_Reproducibility": 0.73,
--     "P4_Safety": 0.89,
--     "P5_Security": 0.86,
--     "P6_Robustness": 0.71,
--     "P7_Fairness": 0.90,
--     "P8_DataGovernance": 0.75,
--     "P9_Accountability": 0.82,
--     "P10_HumanAgency": 0.88,
--     "P11_InclusiveGrowth": 1.00
--   },
--   "total_readiness_score": 0.85,
--   
--   "responses": [
--     {
--       "question_id": "Q001",
--       "pid": "1.1.1",
--       "principle_name": "Transparency",
--       "question_text": "Does the vendor align with PDPC's Advisory Guidelines...?",
--       "answer": "Have",
--       "score": 1.0,
--       "evidence_provided": true,
--       "evidence_files": ["privacy_policy.pdf", "pdpa_compliance.pdf"],
--       "explanation": null,
--       "assessed_at": "2026-03-30T14:05:00Z"
--     },
--     {
--       "question_id": "Q002",
--       "pid": "1.1.2",
--       "principle_name": "Transparency",
--       "question_text": "Does the vendor maintain transparency measures...?",
--       "answer": "Partial",
--       "score": 0.5,
--       "evidence_provided": true,
--       "evidence_files": ["transparency_statement.pdf"],
--       "explanation": "Vendor has transparency measures but documentation is incomplete for algorithmic decision explanations",
--       "assessed_at": "2026-03-30T14:07:00Z"
--     }
--     // ... 88 more responses
--   ],
--   
--   "evidence_files": [
--     {
--       "filename": "privacy_policy.pdf",
--       "gcs_path": "gs://ai-procurement-evidence/ASM-2026-001/privacy_policy.pdf",
--       "question_ids": ["Q001"],
--       "uploaded_at": "2026-03-30T14:05:00Z",
--       "file_size_bytes": 245780
--     },
--     {
--       "filename": "pdpa_compliance.pdf",
--       "gcs_path": "gs://ai-procurement-evidence/ASM-2026-001/pdpa_compliance.pdf",
--       "question_ids": ["Q001", "Q003"],
--       "uploaded_at": "2026-03-30T14:05:30Z",
--       "file_size_bytes": 189340
--     }
--     // ... more evidence files
--   ],
--   
--   "created_at": "2026-03-30T14:00:00Z",
--   "last_modified_at": "2026-03-30T14:45:00Z",
--   "procurement_stage": "evaluation",
--   "estimated_contract_value": 500000.00,
--   "notes": "Assessment conducted during RFP evaluation phase. Vendor responsive to questions."
-- }

-- ============================================================================
-- GOVERNANCE NOTES
-- ============================================================================
-- 
-- 1. IMMUTABILITY
--    - Use INSERT only, never UPDATE or DELETE
--    - Each assessment is a permanent record
--    - If corrections needed, insert new version with updated assessment_id
--
-- 2. AUDIT TRAIL
--    - Every field tracks who, what, when
--    - Evidence files referenced (not stored in table)
--    - Complete reproducibility: same inputs = same outputs
--
-- 3. PARTITIONING
--    - Partitioned by assessment_date for query performance
--    - Older assessments can be archived if needed (not deleted)
--
-- 4. PRIVACY
--    - No PII stored (assessor_id is pseudonymous)
--    - Evidence files in separate GCS bucket (not in table)
--    - Access controlled via IAM roles
--
-- 5. COMPLIANCE
--    - Aligns with Singapore PDPA requirements
--    - Supports AI governance audit requirements
--    - Retention policy: 7 years (typical government requirement)
--
-- ============================================================================
