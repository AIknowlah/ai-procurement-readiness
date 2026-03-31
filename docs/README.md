# AI Procurement Readiness Assessment Tool

> A structured assessment tool for evaluating AI vendor systems against Singapore's IMDA AI Verify Testing Framework

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-green.svg)](https://github.com/langchain-ai/langgraph)

---

## 📌 Overview

This tool helps Singapore government procurement officers assess AI vendor systems against the **11 principles** of the IMDA AI Verify Testing Framework (2025 Edition). It provides:

- 📋 **90 structured questions** mapped to AI Verify process checks
- 🤖 **AI-assisted document analysis** using Google Gemini vision
- 📊 **Automated scoring** with readiness percentages per principle
- 📄 **Professional Word reports** for procurement documentation
- 🗄️ **BigQuery audit trail** for compliance and transparency

---

## ⚠️ Portfolio Project Notice

**This is a learning and demonstration project.**

✅ **Intended for:**
- Portfolio demonstration of AI governance capabilities
- Learning LangGraph, BigQuery, Gemini API
- Proof of concept for structured AI assessment

❌ **NOT production-ready for:**
- Actual government procurement (requires 3-4 months additional work)
- High-stakes decisions (missing authentication/authorization)
- Compliance-critical environments (PDPA rights not fully implemented)

**See [KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md) for complete gap analysis.**

---

## ✨ Features

### **Core Capabilities**

🎯 **Governance-Aligned Assessment**
- 90 questions covering all 11 AI Verify principles
- Questions focus on vendor system capabilities
- No gaps in framework coverage

🤖 **AI-Powered Document Analysis**
- Upload vendor documentation (PDF, images)
- Gemini 1.5 Flash extracts relevant information
- Contextual assistance (not automated scoring)

📊 **Automated Scoring**
- Readiness score per principle (0-100%)
- Overall readiness percentage
- Transparent calculation methodology

📄 **Professional Reporting**
- Word document generation
- Executive summary with scores
- Detailed findings per principle
- Evidence references

🔒 **Security Enhanced (v1.0)**
- Reference document integrity (SHA-256)
- Input validation and sanitization
- Protection against injection attacks

💾 **Audit Trail**
- Permanent storage in BigQuery (asia-southeast1)
- Evidence files with SHA-256 hashes
- Timestamp and assessor tracking

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │  ← User Interface
└────────┬────────┘
         │
┌────────▼────────┐
│ LangGraph       │  ← Workflow Orchestration
│ State Machine   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬─────────────┐
    │         │          │             │
┌───▼────┐ ┌─▼──────┐ ┌─▼────────┐ ┌──▼──────┐
│Gemini  │ │BigQuery│ │python-   │ │Security │
│API     │ │Storage │ │docx      │ │Modules  │
└────────┘ └────────┘ └──────────┘ └─────────┘
```

---

## 🛠️ Tech Stack

**Core:**
- Python 3.11+
- LangGraph (workflow orchestration)
- Google Gemini API (document analysis)
- Google BigQuery (audit storage)
- python-docx (report generation)
- Streamlit (web UI)

**Infrastructure:**
- Google Cloud Platform (asia-southeast1 region)
- Git/GitHub (version control)

---

## 📋 What's Covered

### **AI Verify Testing Framework (2025 Edition)**

All 11 principles, 90 process checks:

1. **Transparency & Explainability** (9 checks) — Model interpretability, documentation
2. **Safety & Robustness** (11 checks) — Error handling, edge cases, adversarial inputs
3. **Accountability** (11 checks) — Ownership, incident response, governance
4. **Data Governance** (9 checks) — Lineage, quality, protection
5. **Human Agency & Oversight** (6 checks) — Human review, override mechanisms
6. **Fairness & Non-Discrimination** (9 checks) — Bias testing, fairness metrics
7. **Inclusivity** (6 checks) — Accessibility, diverse user needs
8. **Environmental Sustainability** (6 checks) — Energy efficiency, carbon footprint
9. **Security** (9 checks) — Access control, encryption, threat modeling
10. **Privacy** (8 checks) — Data minimization, consent, anonymization
11. **Business Continuity** (6 checks) — Disaster recovery, failover, backup

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.11 or higher
- Google Cloud account (for BigQuery and Gemini API)
- Git

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/AIknowlah/ai-procurement-readiness.git
cd ai-procurement-readiness
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json

# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# BigQuery
BIGQUERY_DATASET=procurement_assessments
BIGQUERY_LOCATION=asia-southeast1
```

4. **Create BigQuery dataset**
```bash
python create_table.py
```

5. **Run the application**
```bash
streamlit run streamlit_app.py
```

6. **Open your browser**
```
http://localhost:8501
```

---

## 📖 Usage

### **Basic Workflow**

1. **Start Assessment**
   - Enter vendor name
   - Enter AI system description
   - Upload vendor documentation (optional)

2. **Document Analysis** (if documents uploaded)
   - Gemini analyzes documents
   - Extracts relevant information
   - Provides context for assessment

3. **Answer Questions**
   - 90 questions across 11 principles
   - Answer options: Have / Partial / Gap
   - Upload evidence files per question
   - Provide explanations for "Partial" answers

4. **Review Scores**
   - View readiness per principle
   - Overall readiness percentage
   - Real-time score updates

5. **HITL Review**
   - Human review of assessment
   - Approve or reject before storage

6. **Generate Report**
   - Professional Word document
   - Executive summary
   - Detailed findings
   - Evidence references

7. **Audit Trail**
   - Permanent storage in BigQuery
   - Evidence files with SHA-256 hashes

---

## 📚 Documentation

Comprehensive documentation is available in the `/docs` folder:

- **[PROJECT_FINAL_STATUS.md](docs/PROJECT_FINAL_STATUS.md)** — What was built, tech stack, learning outcomes
- **[KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md)** — Honest gap analysis, production requirements
- **[FUTURE_IMPROVEMENTS.md](docs/FUTURE_IMPROVEMENTS.md)** — Roadmap to production (Phases 7-10)
- **[DEMO_GUIDE.md](docs/DEMO_GUIDE.md)** — How to run, test cases, expected outputs

---

## 🧪 Testing

**Security tests:**
```bash
python test_security_setup.py
```

**Integration examples:**
```bash
python examples/security_integration_example.py
python examples/input_validation_integration_example.py
```

---

## 📊 Project Statistics

- **Questions:** 90 structured questions
- **Principles:** 11 AI Verify principles
- **Code:** ~3,000+ lines of Python
- **Documentation:** ~1,500 lines of markdown
- **Development:** ~4 weeks of focused work

---

## 🎯 Key Learnings

This project demonstrates:

**Technical Skills:**
- LangGraph state machine orchestration
- Google Cloud Platform (BigQuery, Gemini API)
- Document processing (python-docx, PDF extraction)
- Security fundamentals (input validation, hashing)

**Governance Knowledge:**
- AI Verify Testing Framework application
- PDPA awareness
- Procurement best practices
- Evidence-based evaluation

**Software Engineering:**
- Modular code architecture
- Comprehensive documentation
- Version control workflow
- Self-awareness of limitations

---

## 🚫 Known Limitations

**Critical gaps (see [KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md) for details):**

1. ❌ No authentication system (Singpass/Corppass not integrated)
2. ❌ Audit trail not fully immutable
3. ❌ PDPA data subject rights not implemented
4. ❌ No automated testing suite
5. ❌ No deployment automation

**Production-ready estimate:** 3-4 months additional work

---

## 🛣️ Roadmap

**v1.0 (Current)** — Portfolio demonstration ✅
- Core assessment workflow
- Basic security enhancements
- Comprehensive documentation

**v2.0 (Future)** — Production-ready (if deployed)
- Authentication & authorization
- Full security hardening
- PDPA compliance automation
- Comprehensive testing
- CI/CD deployment

See [FUTURE_IMPROVEMENTS.md](docs/FUTURE_IMPROVEMENTS.md) for detailed roadmap.

---

## 🤝 Contributing

This is a personal portfolio project and is not accepting contributions.

If you're building something similar:
- Use the documentation as reference
- Check out the [examples/](examples/) folder
- Read [KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md) to avoid the same gaps

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

**Frameworks & Standards:**
- [IMDA AI Verify Foundation](https://github.com/aiverify-foundation) (framework source)
- Singapore PDPC (PDPA guidance)
- Model AI Governance Framework (principles)

**Open Source:**
- [LangGraph](https://github.com/langchain-ai/langgraph) (workflow orchestration)
- [Google Generative AI](https://ai.google.dev/) (Gemini API)
- Python ecosystem

---

## 📧 Contact

**Author:** Chan (AI Governance Learning Portfolio)  
**GitHub:** [@AIknowlah](https://github.com/AIknowlah)  
**Repository:** [github.com/AIknowlah/ai-procurement-readiness](https://github.com/AIknowlah/ai-procurement-readiness)

---

## ⚖️ Disclaimer

This tool is provided for **educational and demonstration purposes only**.

- Not certified or endorsed by IMDA, PDPC, or any government agency
- Not a substitute for professional AI governance consulting
- Interpretation of AI Verify framework is best-effort, not authoritative
- No warranty or support provided

**For actual government procurement, consult qualified AI governance professionals and legal advisors.**

---

**Built as part of a learning journey in AI governance and software engineering.**

**Last Updated:** March 2026
