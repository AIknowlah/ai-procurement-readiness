# AI Procurement Readiness Assessment Tool - Final Status Report

**Project:** AI Procurement Readiness Assessment Tool  
**Version:** 1.0 (Security-Enhanced)  
**Status:** Feature-Complete Portfolio Project  
**Date:** March 2026  
**Author:** Chan (AI Governance Learning Portfolio)  
**GitHub:** [github.com/AIknowlah/ai-procurement-readiness](https://github.com/AIknowlah/ai-procurement-readiness)

---

## 📌 Executive Summary

This tool helps Singapore government procurement officers assess AI vendor systems against the 11 principles of the **IMDA AI Verify Testing Framework (2025 Edition)**. It provides a structured assessment workflow, automated scoring, professional Word report generation, and audit trail storage in BigQuery.

**⚠️ Portfolio Project Notice:**  
This is a **learning and demonstration project**. It is NOT production-ready for actual government deployment without security hardening and compliance enhancements. See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for detailed gap analysis.

**Intended Use:**  
- Portfolio demonstration of AI governance capabilities
- Learning project for LangGraph, BigQuery, Gemini API
- Proof of concept for structured AI assessment methodology

**NOT Intended:**  
- Production government deployment (requires additional 3-4 months of work)
- High-stakes procurement decisions (no authentication/authorization)
- Compliance-critical environments (PDPA rights not implemented)

---

## ✨ What This Tool Does

### **Core Functionality**

**Input:**
- Vendor name
- AI system description
- Assessor identification
- System documentation (optional)

**Process:**
1. AI-powered document analysis (Gemini 1.5 Flash vision)
2. 90 structured questions across 11 AI Verify principles
3. Evidence collection with file upload
4. Automated scoring per principle
5. Human-in-the-loop (HITL) review gate
6. BigQuery audit trail storage

**Output:**
- Overall readiness score (0-100%)
- Per-principle scores (11 principles)
- Professional Word report (.docx)
- Permanent audit trail in BigQuery
- Evidence files with SHA-256 hashes

### **Key Features**

✅ **Governance-Aligned Assessment**
- 90 questions mapped 1:1 to AI Verify process checks
- Coverage of all 11 principles (no gaps)
- Questions focused on vendor capabilities (not organizational maturity)

✅ **AI-Assisted Analysis**
- Gemini 1.5 Flash vision for document analysis
- Extracts relevant information from PDFs/images
- Provides assessment context (not automated scoring)

✅ **Structured Workflow**
- LangGraph state machine for reliable execution
- Progress auto-save and resume capability
- HITL review gate before final storage

✅ **Audit Trail**
- Immutable BigQuery storage (asia-southeast1 region)
- SHA-256 hashing for evidence files
- Timestamp and assessor tracking

✅ **Professional Reporting**
- Word document generation (python-docx)
- Executive summary with scores
- Detailed findings per principle
- Evidence references

✅ **Security Enhancements** (v1.0)
- Reference document integrity verification (SHA-256)
- Input validation and sanitization
- Protection against SQL injection, prompt injection, path traversal
- File upload validation (size, type, filename safety)

---

## 🏗️ What Has Been Built

### **Phase 1: Framework Extraction** ✅
**Duration:** 2 days  
**Deliverables:**
- Extracted 11 principles, 90 process checks from AI Verify GitHub repos
- Created `framework_structure_complete.json` (master reference)
- Fixed P9 Accountability JSON parsing error (79 → 90 total checks)

**Learning Outcomes:**
- GitHub API navigation
- JSON schema design
- Data validation and integrity checking

---

### **Phase 2: Question Bank Generation** ✅
**Duration:** 3 days  
**Deliverables:**
- 90 vendor-focused questions (1:1 mapping to process checks)
- `question_bank.py` with dataclasses (Question, AnswerOption, Evidence)
- `generate_questions.py` with QuestionGenerator class
- `question_bank.json` (structured question database)

**Learning Outcomes:**
- Python dataclasses for structured data
- Question design for procurement context
- Mapping abstract principles to concrete questions

**Key Design Decision:**
Questions focus on **vendor system capabilities** (not organizational maturity). Example:
- ❌ Wrong: "Does your organization have a data governance policy?"
- ✅ Right: "Does this AI system have documented data lineage tracking?"

---

### **Phase 3: BigQuery Schema & Scoring** ✅
**Duration:** 2 days  
**Deliverables:**
- `schema_design.sql` (assessments, responses, evidence tables)
- `bigquery_storage.py` (storage functions with parameterized queries)
- `scoring_calculator.py` (readiness calculation logic)
- BigQuery project in asia-southeast1 region

**Learning Outcomes:**
- BigQuery schema design for audit data
- Parameterized queries (SQL injection prevention)
- Regional data residency (Singapore compliance)

**Scoring Formula:**
```
Readiness per principle = (Have + 0.5 × Partial) ÷ Total checks
Overall readiness = Average of 11 principle scores
```

---

### **Phase 4: LangGraph Workflow** ✅
**Duration:** 3 days  
**Deliverables:**
- `assessment_state.py` (TypedDict state definition)
- `assessment_nodes.py` (7 workflow nodes)
- `assessment_workflow.py` (StateGraph orchestration)
- HITL review gate implementation

**Learning Outcomes:**
- LangGraph state machine design
- Conditional routing in workflows
- Human-in-the-loop patterns

**Workflow Steps:**
1. Load questions from JSON
2. Present question → Collect answer (loop 90x)
3. Calculate scores per principle
4. HITL review gate (human approval required)
5. Store to BigQuery
6. Mark complete

---

### **Phase 5: Word Report Generation** ✅
**Duration:** 2 days  
**Deliverables:**
- `report_generator.py` (python-docx report builder)
- Professional Word template with:
  - Executive summary
  - Overall readiness score
  - Per-principle breakdown
  - Detailed findings
  - Evidence references

**Learning Outcomes:**
- python-docx library for Word automation
- Document structure for professional reports
- Formatting and styling in code

---

### **Phase 6: Streamlit UI** ✅
**Duration:** 3 days  
**Deliverables:**
- `streamlit_app.py` (web interface)
- Document upload and AI analysis (Gemini vision)
- Progress persistence (auto-save/resume)
- File upload for evidence
- Real-time scoring display

**Learning Outcomes:**
- Streamlit UI/UX design
- File upload handling
- Session state management
- Gemini API integration (vision model)

**Key Features:**
- Upload vendor documents (PDF/images)
- AI extracts relevant info (Gemini 1.5 Flash)
- Progress auto-saved to local JSON
- Resume incomplete assessments
- Evidence file upload per question

---

### **Phase 7a: Security Enhancements** ✅
**Duration:** 1 day  
**Deliverables:**
- `src/security/security.py` (reference document integrity)
- `src/security/input_validator.py` (input validation)
- Integration into assessment workflow
- Comprehensive testing

**Learning Outcomes:**
- Cryptographic hashing (SHA-256)
- Input sanitization patterns
- Attack detection (SQL injection, prompt injection, path traversal)

**Protection Against:**
- Reference document tampering
- SQL injection attacks
- Prompt injection attacks
- Path traversal attacks
- Resource exhaustion (size limits)
- Malware uploads (file type validation)

---

## 🛠️ Technology Stack

### **Core Technologies**
- **Python 3.11+** — Primary language
- **LangGraph** — State machine workflow orchestration
- **Google Gemini API** — AI document analysis (Gemini 1.5 Flash vision)
- **Google BigQuery** — Audit trail storage (asia-southeast1 region)
- **python-docx** — Word document generation
- **Streamlit** — Web UI framework

### **Supporting Libraries**
- **google-cloud-bigquery** — BigQuery client
- **google-generativeai** — Gemini API client
- **python-dotenv** — Environment variables
- **typing-extensions** — Type hints

### **Development Tools**
- **Git/GitHub** — Version control
- **VS Code** — IDE
- **PowerShell** — Windows terminal

### **Cloud Infrastructure**
- **GCP Project** — `ai-procurement-readiness-sg`
- **BigQuery Dataset** — `procurement_assessments` (asia-southeast1)
- **Cloud Storage** — Evidence file storage (asia-southeast1)

---

## 📊 Project Statistics

**Code:**
- **Total Files:** ~20 Python files, 5 JSON files
- **Total Lines:** ~3,000+ lines of Python code
- **Documentation:** ~1,500 lines of markdown

**Data:**
- **Questions:** 90 structured questions
- **Principles:** 11 AI Verify principles
- **Process Checks:** 90 (1:1 mapped to questions)

**Testing:**
- **Manual Test Cases:** 3 fictional scenarios
- **Security Tests:** 6 attack scenarios (all blocked)
- **Integration Tests:** End-to-end workflow tested

**Development Timeline:**
- **Phase 1-6:** ~3 weeks (core functionality)
- **Phase 7a:** 1 day (security enhancements)
- **Total:** ~4 weeks of focused work

---

## 🎯 Governance Alignment

### **AI Verify Testing Framework (2025 Edition)**

**Coverage:**
- ✅ All 11 principles covered
- ✅ All 90 process checks mapped to questions
- ✅ Official framework structure preserved
- ✅ No gaps or omissions

**Principles Covered:**
1. Transparency & Explainability (9 checks)
2. Safety & Robustness (11 checks)
3. Accountability (11 checks)  ← Fixed from 79 to 90 total
4. Data Governance (9 checks)
5. Human Agency & Oversight (6 checks)
6. Fairness & Non-Discrimination (9 checks)
7. Inclusivity (6 checks)
8. Environmental Sustainability (6 checks)
9. Security (9 checks)
10. Privacy (8 checks)
11. Business Continuity (6 checks)

**Framework Sources:**
- `aiverify-foundation/aiverify` GitHub repo
- `aiverify-foundation/moonshot` GitHub repo
- IMDA official documentation

---

### **PDPA Awareness**

While full PDPA compliance is not implemented (see [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md)), the tool demonstrates awareness:

✅ **Data Minimization**
- Only necessary fields collected
- No NRIC, no financial data, no health data
- Assessment-level data (not individual-level)

✅ **Consent & Purpose**
- Assessor role documented
- Assessment purpose clear (procurement evaluation)
- Data use limited to assessment scope

✅ **Security Safeguards**
- Input validation (basic protection)
- Reference document integrity (tamper detection)
- Audit trail (who did what, when)

❌ **Not Implemented** (production requirements):
- Data subject rights (access, correction, deletion)
- Automated retention policy
- Data breach notification procedures

**Reference:** PDPA 2012 (revised 17 May 2022)

---

### **Model AI Governance Framework Alignment**

**Principles Applied:**
- ✅ **Internal Governance** — Structured assessment methodology
- ✅ **Human Involvement** — HITL review gate
- ✅ **Operations Management** — Audit trail and documentation
- ✅ **Stakeholder Engagement** — Vendor assessment process

**Framework Version:** Model AI Governance Framework (2nd Edition) + Generative AI Supplement

---

## 🎓 Key Learning Outcomes

### **Technical Skills Developed**

**1. LangGraph State Machines**
- State management with TypedDict
- Conditional routing between nodes
- Error handling in workflows
- Human-in-the-loop patterns

**2. Google Cloud Platform**
- BigQuery schema design and queries
- Regional data residency (asia-southeast1)
- Cloud Storage for file handling
- Service account management

**3. AI API Integration**
- Gemini API for document analysis
- Vision model usage (image/PDF processing)
- Prompt engineering for structured outputs
- Cost management and rate limiting

**4. Document Processing**
- python-docx for Word generation
- PDF text extraction
- Image analysis with vision models
- Structured report templates

**5. Security Fundamentals**
- Cryptographic hashing (SHA-256)
- Input validation and sanitization
- Attack pattern recognition
- Secure coding practices

---

### **Governance & Compliance Knowledge**

**1. AI Verify Testing Framework**
- 11 principles and 90 process checks
- Practical application to vendor assessment
- Gap analysis methodology

**2. PDPA (Personal Data Protection Act)**
- Data protection principles
- Consent and purpose limitation
- Data subject rights
- Retention requirements

**3. Procurement Best Practices**
- Evidence-based evaluation
- Audit trail requirements
- Four-eyes principle (HITL)
- Documentation standards

---

### **Software Engineering Practices**

**1. Code Organization**
- Modular architecture
- Separation of concerns
- Clear file structure
- Comprehensive documentation

**2. Version Control**
- Git workflow
- Meaningful commit messages
- Documentation in repository

**3. Error Handling**
- Try-catch patterns
- Graceful degradation
- User-friendly error messages

**4. Testing Approach**
- Manual test cases
- Security testing
- Integration verification

---

## 🚫 What This Project Is NOT

**Honest Limitations:**

❌ **Not production-ready** — Missing authentication, full security hardening, compliance automation

❌ **Not certified** — Not reviewed by IMDA, PDPC, or security auditors

❌ **Not a product** — No support, no SLA, no warranty

❌ **Not authoritative** — AI Verify framework interpretation is best-effort, not official

❌ **Not replacing consultants** — Does not replace professional AI governance consulting

**See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for complete gap analysis.**

---

## 🎯 Project Goals (Achieved)

### **Primary Goals** ✅

1. **Learn by Building** — Hands-on experience with LangGraph, BigQuery, Gemini API
2. **Governance Application** — Apply AI Verify framework to practical use case
3. **Portfolio Demonstration** — Show technical and governance capabilities
4. **Structured Methodology** — Create systematic vendor assessment approach

### **Secondary Goals** ✅

5. **Security Awareness** — Demonstrate basic security thinking
6. **Documentation Excellence** — Clear, honest, comprehensive docs
7. **Code Quality** — Readable, maintainable, well-commented code
8. **Learning Transparency** — Document what was learned, what was challenging

---

## 💼 Portfolio Value

### **What This Project Demonstrates**

**Technical Capabilities:**
- ✅ Multi-step workflow orchestration (LangGraph)
- ✅ Cloud infrastructure usage (GCP)
- ✅ AI API integration (Gemini)
- ✅ Database design (BigQuery)
- ✅ Document generation (python-docx)
- ✅ Web UI development (Streamlit)
- ✅ Security fundamentals (input validation, hashing)

**Governance Understanding:**
- ✅ AI Verify framework application
- ✅ PDPA awareness
- ✅ Procurement processes
- ✅ Audit trail requirements
- ✅ Evidence-based evaluation

**Soft Skills:**
- ✅ Self-awareness (honest limitations doc)
- ✅ Project scoping (knew when to stop)
- ✅ Documentation (clear, comprehensive)
- ✅ Problem-solving (fixed P9 framework bug)

**Learning Ability:**
- ✅ Learned 5+ new technologies in 4 weeks
- ✅ Applied official frameworks to practical use
- ✅ Built end-to-end solution from scratch
- ✅ Documented learning journey

---

## 📈 Future Direction

See [FUTURE_IMPROVEMENTS.md](FUTURE_IMPROVEMENTS.md) for detailed roadmap.

**If this project were to go to production:**
- 3-4 months additional work
- Authentication and authorization
- Full security hardening
- PDPA compliance implementation
- Comprehensive testing suite
- Deployment automation

**More likely next steps:**
- **Portfolio use** — Showcase in job applications
- **Learning continuation** — Build different project with different tech stack
- **Knowledge sharing** — Blog posts, documentation
- **Move on** — Apply learnings to next project

---

## 🙏 Acknowledgments

**Frameworks & Standards:**
- IMDA AI Verify Foundation (framework source)
- Singapore PDPC (PDPA guidance)
- Model AI Governance Framework (principles)

**Open Source:**
- LangChain/LangGraph (workflow orchestration)
- Google Generative AI (Gemini API)
- Python ecosystem (countless libraries)

**Learning Resources:**
- LangGraph documentation
- Google Cloud documentation
- Python community tutorials

---

## 📞 Contact

**GitHub:** [github.com/AIknowlah](https://github.com/AIknowlah)  
**Project Repo:** [github.com/AIknowlah/ai-procurement-readiness](https://github.com/AIknowlah/ai-procurement-readiness)

---

**Built as part of a learning journey in AI governance and software engineering.**

**Last Updated:** 31 March 2026  
**Document Version:** 1.0
