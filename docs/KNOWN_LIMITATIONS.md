# Known Limitations & Design Decisions

**Project:** AI Procurement Readiness Assessment Tool  
**Version:** 1.0 (Security-Enhanced)  
**Date:** March 2026  
**Author:** Chan (Learning Portfolio Project)  

---

## 📌 Purpose of This Document

This document provides an **honest assessment** of what this tool does NOT have compared to production-grade government systems. 

**Why document limitations?**
- Demonstrates self-awareness and security thinking
- Shows understanding of production requirements
- Provides clear roadmap for future work
- Sets appropriate expectations for portfolio viewers

**Important Context:**
This is a **learning and portfolio project**, not production software. Certain production requirements were intentionally deferred to maintain project scope and demonstrate core capabilities within a reasonable timeframe.

---

## 🎯 Design Philosophy

**What this project prioritizes:**
- ✅ Core functionality (assessment workflow, scoring, reporting)
- ✅ Governance alignment (AI Verify framework mapping)
- ✅ Learning outcomes (LangGraph, BigQuery, Gemini API)
- ✅ Basic security (reference integrity, input validation)

**What was intentionally deferred:**
- ❌ Production-grade authentication
- ❌ Enterprise-level security hardening
- ❌ Full compliance automation
- ❌ Comprehensive testing suite

---

## 🔴 CRITICAL LIMITATIONS (Production Blockers)

These gaps **must be addressed** before deploying to actual government use.

---

### 1. No Authentication System

**Current State:**  
No authentication or authorization system implemented. Users self-declare their assessor ID.

**Security Risk:**  
- Anyone can run assessments claiming to be any assessor
- No identity verification
- No role-based access control
- No audit trail of who actually performed actions

**Mitigation (Currently Implemented):**
- Input validation prevents some malicious inputs
- BigQuery logs include self-declared assessor IDs
- Tool is intended for local/internal use only

**Production Requirement:**
- Singpass/Corppass integration for government SSO
- Role-based access control (RBAC):
  - Assessor role: Can create/edit assessments
  - Reviewer role: Can approve/reject assessments
  - Admin role: Can manage users and settings
- Multi-factor authentication (MFA)
- Session management with timeout
- Audit logging of authentication events

**Why Deferred:**
- SSO integration requires government infrastructure access
- OAuth/OIDC flows add 2-3 weeks of complexity
- Core workflow demonstration doesn't require authentication
- Portfolio focus is on assessment logic, not auth infrastructure
- Can be added when deploying to actual government environment

**Estimated Effort to Fix:** 2-3 weeks
- Week 1: Singpass/Corppass integration, basic RBAC
- Week 2: Session management, MFA
- Week 3: Testing and security audit

**Governance Impact:** HIGH  
Without authentication, the tool cannot enforce accountability or prevent unauthorized assessments.

---

### 2. Evidence Storage Not Fully Immutable

**Current State:**  
Evidence files are stored in Google Cloud Storage with SHA-256 hashing, but the bucket does not have immutability policies enabled.

**Security Risk:**
- Files could theoretically be replaced or deleted after assessment
- No versioning enabled (overwrites possible)
- No retention lock preventing deletion

**Mitigation (Currently Implemented):**
- File hashes are recorded in BigQuery at upload time
- Hash verification would detect file replacement
- Service account has minimal permissions
- Files are named with timestamps and assessment IDs

**Production Requirement:**
- GCS bucket with Object Versioning enabled
- Retention policy preventing deletion for 7 years (compliance requirement)
- Bucket Lock to prevent policy changes
- Content-addressable storage (CAS) for true immutability
- Audit logging of all file access/modification attempts

**Why Deferred:**
- Requires careful GCS configuration and testing
- File hashing provides 90% of integrity benefit
- Full immutability is enhancement, not blocker for portfolio
- Simple to enable when moving to production

**Estimated Effort to Fix:** 2-3 days
- Day 1: Enable GCS versioning and retention policy
- Day 2: Test versioning and recovery scenarios
- Day 3: Document procedures and update code

**Governance Impact:** MEDIUM  
Hash verification provides good integrity checking, but true immutability is needed for legal defensibility.

---

### 3. Audit Trail Not Immutable

**Current State:**  
Assessment records are stored in BigQuery with standard permissions. Users with BigQuery access could theoretically delete or modify records.

**Security Risk:**
- Audit trail could be tampered with
- No protection against admin-level deletion
- No cryptographic proof of record integrity

**Mitigation (Currently Implemented):**
- Service accounts have minimal permissions (insert-only in application code)
- BigQuery native audit logs track all operations
- GCP project-level logging provides backup audit trail
- Assessment IDs are UUIDs (hard to guess for targeted deletion)

**Production Requirement:**
- Append-only tables (revoke UPDATE and DELETE permissions)
- Hash chaining to detect tampering (each record includes hash of previous)
- Separate admin vs application service accounts
- Immutable audit log export to cold storage
- Regular integrity verification jobs

**Why Deferred:**
- Requires careful IAM setup and testing
- Risk is low in portfolio/demo context (no malicious actors)
- BigQuery native audit logs provide good backup
- Standard best practice is to restrict permissions, which is implemented

**Estimated Effort to Fix:** 1 week
- Days 1-2: Implement append-only permissions and test
- Days 3-4: Build hash chaining mechanism
- Day 5: Create integrity verification job

**Governance Impact:** HIGH  
Audit trail integrity is critical for compliance and dispute resolution.

---

### 4. No Rate Limiting

**Current State:**  
No per-user quotas or rate limiting implemented.

**Security Risk:**
- Tool could be abused for spam assessments
- No protection against resource exhaustion attacks
- Gemini API costs could spike unexpectedly
- BigQuery storage could grow unbounded

**Mitigation (Currently Implemented):**
- Input validation limits request size (10MB max description, 10MB max files)
- Streamlit runs locally (not public-facing, so no internet abuse)
- Manual monitoring of BigQuery costs
- Assessment workflow has natural rate limiting (takes time to complete)

**Production Requirement:**
- Per-user daily/hourly quotas (e.g., 10 assessments per day)
- IP-based rate limiting (for public-facing deployment)
- Cost monitoring and alerts (BigQuery, Gemini API)
- CAPTCHA for public-facing deployment
- Graceful degradation when limits exceeded

**Why Deferred:**
- Local deployment has no abuse risk (single user)
- Cloud deployment needs hosting infrastructure first
- Can be added with API Gateway or Cloud Run middleware
- Portfolio demonstration doesn't need public exposure

**Estimated Effort to Fix:** 2-3 days
- Day 1: Implement user quota tracking in BigQuery
- Day 2: Add rate limiting middleware
- Day 3: Testing and documentation

**Governance Impact:** MEDIUM  
Important for cost control and abuse prevention, but not a security vulnerability in local deployment.

---

### 5. No Peer Review / Two-Person Rule

**Current State:**  
Single assessor completes entire assessment without mandatory peer review.

**Risk:**
- No four-eyes principle for high-value contracts
- Single point of failure (assessor error or bias)
- No checks and balances

**Mitigation (Currently Implemented):**
- HITL (Human-in-the-Loop) review gate before storage
- Audit trail shows who performed assessment
- Reports can be manually reviewed by supervisors
- Assessment methodology is transparent and documented

**Production Requirement:**
- Mandatory peer review for contracts above threshold (e.g., >$1M SGD)
- Workflow states: draft → pending_review → approved → stored
- Email notifications for review requests
- Reviewer must be different from original assessor
- Conflict of interest checks

**Why Deferred:**
- Requires workflow state management (adds complexity)
- Notification infrastructure (email/Slack)
- User management system (to assign reviewers)
- Portfolio focus is on assessment logic, not approval workflows

**Estimated Effort to Fix:** 1-2 weeks
- Week 1: Add workflow states and reviewer assignment
- Week 2: Build notification system and testing

**Governance Impact:** MEDIUM  
Important for high-value procurements, but single assessor is acceptable for lower-risk assessments.

---

## 🟡 COMPLIANCE LIMITATIONS (Regulatory Requirements)

These gaps relate to legal/regulatory compliance (PDPA, records management).

---

### 6. No PDPA Data Subject Rights Implementation

**Current State:**  
No mechanism for data access, correction, or deletion requests as required by Singapore's Personal Data Protection Act (PDPA).

**Regulatory Risk:**
- Non-compliance with PDPA Section 21 (Access)
- Non-compliance with PDPA Section 22 (Correction)
- Non-compliance with PDPA Section 26 (Retention Limitation)

**Mitigation (Currently Implemented):**
- Data minimization: Only necessary fields collected
- No sensitive personal data collected (no NRIC, no financial data)
- Assessment data stored with clear ownership (assessor ID)
- Tool operates at system/organizational level (not individual-level)

**Production Requirement:**
- Data access endpoint: Users can export all their data
- Data correction workflow: Users can request corrections with justification
- Automated retention and deletion: After 7 years, records archived/deleted
- Privacy policy and terms of service
- PDPA compliance officer designated
- Data breach response plan

**Why Deferred:**
- Legal requirement only applies when processing real user data
- Portfolio/demo uses test data only
- Production deployment needs legal review first
- PDPA compliance requires organizational policies, not just code

**Estimated Effort to Fix:** 1-2 weeks
- Days 1-3: Build data access and correction endpoints
- Days 4-5: Implement retention automation
- Days 6-7: Legal documentation and testing

**Governance Impact:** HIGH (for production)  
Critical for legal compliance, but not applicable to portfolio demonstration.

---

### 7. No Automated Data Retention Policy

**Current State:**  
No automated deletion of data after retention period expires.

**Regulatory Risk:**
- Holding data longer than necessary (PDPA violation)
- Increased storage costs
- Increased breach risk (more data = more exposure)

**Mitigation (Currently Implemented):**
- BigQuery data can be manually purged
- Retention period documented (7 years per government records policy)
- Data is queryable by date for manual cleanup

**Production Requirement:**
- Cloud Scheduler job to identify records > 7 years old
- Automated archival to cold storage (Cloud Storage Nearline/Archive)
- Automated deletion after archival
- User notification 30 days before deletion
- Audit log of retention actions

**Why Deferred:**
- No real user data yet (only test data)
- Simple to add as Cloud Scheduler + Cloud Function
- Requires governance approval on exact retention period
- Portfolio demonstration doesn't span 7 years

**Estimated Effort to Fix:** 3-5 days
- Days 1-2: Build retention check job
- Day 3: Test archival and deletion
- Days 4-5: Documentation and monitoring

**Governance Impact:** MEDIUM  
Important for compliance, but not urgent for short-term portfolio use.

---

## 🟢 FUNCTIONAL LIMITATIONS (Quality & Maintainability)

These gaps affect maintainability and reliability but are not security/compliance issues.

---

### 8. No Automated Testing

**Current State:**  
Manual testing only. No unit tests, integration tests, or end-to-end tests.

**Risk:**
- Regressions not caught when code changes
- Harder to refactor with confidence
- Deployment errors more likely
- Slower development velocity

**Mitigation (Currently Implemented):**
- Manual test cases documented
- Code review before commits (self-review)
- Integration examples provided for security modules
- Self-test functions in security modules

**Production Requirement:**
- pytest unit tests with 80%+ coverage
- Integration tests for LangGraph workflow
- End-to-end tests for complete assessment flow
- CI/CD pipeline running tests on every commit
- Test data fixtures and factories

**Why Deferred:**
- Time constraint: Testing infrastructure would double development time
- Portfolio focus is "can you build" not "can you test"
- Manual testing sufficient for demonstration
- Can be added incrementally

**Estimated Effort to Fix:** 2-3 weeks
- Week 1: Write unit tests for all modules
- Week 2: Write integration tests
- Week 3: Set up CI/CD pipeline

**Governance Impact:** LOW (for portfolio), HIGH (for production)  
Critical for production maintainability, but acceptable to defer for portfolio.

---

### 9. No Deployment Automation

**Current State:**  
Manual local setup. No containerization, no CI/CD, no infrastructure-as-code.

**Risk:**
- Deployment errors (missing dependencies, config drift)
- Hard to reproduce environments
- Manual deployment is slow and error-prone

**Mitigation (Currently Implemented):**
- Documented setup instructions in README
- `requirements.txt` for Python dependencies
- `.env.example` for configuration template
- GCP project configuration documented

**Production Requirement:**
- Docker containerization
- Cloud Run or GKE deployment
- GitHub Actions CI/CD pipeline
- Infrastructure as Code (Terraform or Cloud Deployment Manager)
- Automated deployment to staging and production environments
- Health checks and readiness probes

**Why Deferred:**
- Local-first approach for learning and demonstration
- Deployment complexity not core learning goal
- Production hosting requires government approval
- Can be added when deployment environment is available

**Estimated Effort to Fix:** 1-2 weeks
- Week 1: Dockerize application, set up Cloud Run
- Week 2: Build CI/CD pipeline with GitHub Actions

**Governance Impact:** LOW  
Operational concern, not governance concern.

---

### 10. Limited Error Handling

**Current State:**  
Basic error handling with try-catch blocks on API calls. Some edge cases may not be gracefully handled.

**Risk:**
- Application crashes on unexpected inputs
- Poor user experience (cryptic error messages)
- Hard to debug issues in production

**Mitigation (Currently Implemented):**
- Input validation prevents most bad inputs
- Try-catch blocks on external API calls (Gemini, BigQuery)
- Error messages printed to console
- Workflow state preserved on most errors (can resume)

**Production Requirement:**
- Comprehensive error handling for all failure modes
- User-friendly error messages (not stack traces)
- Error reporting and logging (Sentry, Cloud Logging)
- Graceful degradation (partial functionality on partial failure)
- Error recovery mechanisms (retry logic, fallbacks)

**Why Deferred:**
- Diminishing returns (80/20 rule applies)
- Caught major error cases (API failures, invalid inputs)
- Polish vs core functionality tradeoff
- Can be improved iteratively

**Estimated Effort to Fix:** 1 week
- Days 1-3: Add comprehensive error handling
- Days 4-5: Integrate error tracking service
- Days 6-7: Testing and documentation

**Governance Impact:** LOW  
User experience issue, not governance issue.

---

## 📊 LIMITATIONS SUMMARY TABLE

| # | Limitation | Severity | Prod Blocker? | Effort to Fix | Governance Impact |
|---|------------|----------|---------------|---------------|-------------------|
| 1 | No Authentication | 🔴 Critical | YES | 2-3 weeks | HIGH |
| 2 | Evidence Storage | 🟡 Medium | NO | 2-3 days | MEDIUM |
| 3 | Audit Immutability | 🔴 High | YES | 1 week | HIGH |
| 4 | No Rate Limiting | 🟡 Medium | NO | 2-3 days | MEDIUM |
| 5 | No Peer Review | 🟡 Medium | NO | 1-2 weeks | MEDIUM |
| 6 | No PDPA Rights | 🔴 High | YES | 1-2 weeks | HIGH |
| 7 | Retention Policy | 🟡 Medium | YES | 3-5 days | MEDIUM |
| 8 | No Automated Tests | 🟢 Low | NO | 2-3 weeks | LOW |
| 9 | No CI/CD | 🟢 Low | NO | 1-2 weeks | LOW |
| 10 | Error Handling | 🟢 Low | NO | 1 week | LOW |

**Total Estimated Effort to Production:** 10-14 weeks (2.5-3.5 months)

---

## 💡 DESIGN DECISIONS (Not Limitations)

These are intentional design choices that are **correct** for the use case:

### 1. No Multi-Tenancy

**Decision:** Single-organization deployment model

**Rationale:**
- Government agencies don't share assessment data
- Each agency would have own deployment
- Simpler security model (no cross-organization data leakage risk)
- Aligns with government data sovereignty requirements

**This is NOT a gap** — it's the correct design for government use.

---

### 2. Manual Evidence Upload

**Decision:** Assessor uploads files per question (not bulk upload)

**Rationale:**
- Ensures assessor reviews each requirement carefully
- Prevents bulk-accept without reading
- Aligns with procurement rigor and due diligence
- Creates clear audit trail (which file supports which answer)

**This is NOT a gap** — it's the correct design for accountability.

---

### 3. Local Streamlit Deployment

**Decision:** Run locally, not cloud-hosted

**Rationale:**
- Simpler for learning and demonstration
- No public hosting costs during development
- Avoids internet exposure before security hardening
- Government deployments would use Cloud Run anyway (not public Streamlit)

**This is NOT a gap** — it's appropriate for portfolio stage.

---

## 🎯 Honest Assessment

### **Is this production-ready?**
**NO** — Missing critical security and compliance features (#1, #3, #6).

### **Is this portfolio-ready?**
**YES** — Demonstrates core capabilities, learning outcomes, and honest self-assessment.

### **Can this be made production-ready?**
**YES** — With 2.5-3.5 months of additional work (see roadmap in `FUTURE_IMPROVEMENTS.md`).

### **Should it be made production-ready?**
**ONLY IF** — An actual government agency wants to deploy it and provides:
- Access to Singpass/Corppass infrastructure
- Legal review of PDPA compliance approach
- Security audit and penetration testing
- Budget for hosting and ongoing maintenance

---

## 📝 What This Document Shows

**To employers and portfolio reviewers, this document demonstrates:**

1. ✅ **Self-awareness** — Knows what's missing and why
2. ✅ **Security thinking** — Identifies risks and mitigations
3. ✅ **Pragmatism** — Knows when to stop and ship vs over-engineer
4. ✅ **Honesty** — Doesn't oversell capabilities
5. ✅ **Planning ability** — Can estimate effort and prioritize fixes
6. ✅ **Communication** — Explains technical concepts clearly

**This honest assessment is MORE impressive than claiming the project is perfect.**

---

## 🔗 Related Documentation

- [FUTURE_IMPROVEMENTS.md](FUTURE_IMPROVEMENTS.md) — Roadmap for v2.0
- [PROJECT_FINAL_STATUS.md](PROJECT_FINAL_STATUS.md) — What was built
- [README.md](../README.md) — Project overview and setup

---

**Last Updated:** 31 March 2026  
**Document Version:** 1.0  
**Author:** Chan (AI Governance Learning Portfolio)
