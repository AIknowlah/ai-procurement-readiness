# Future Improvements Roadmap

**Project:** AI Procurement Readiness Assessment Tool  
**Current Version:** 1.0 (Security-Enhanced)  
**Target Version:** 2.0 (Production-Ready)  
**Date:** March 2026  
**Author:** Chan

---

## 📌 Purpose

This document outlines the roadmap to transform the current portfolio project into a **production-ready government procurement tool**.

**Important Context:**  
These improvements are **NOT planned for immediate implementation**. This roadmap exists to:
- Document what production deployment would require
- Show understanding of production standards
- Provide effort estimates for future planning
- Demonstrate gap awareness

**Decision Point:**  
Implementation only proceeds if:
- A government agency expresses interest in deployment
- Budget and infrastructure access are provided
- Legal and security reviews are commissioned

---

## 🎯 Production Readiness Phases

**Total Estimated Time:** 12-16 weeks (3-4 months)

| Phase | Focus | Duration | Priority |
|-------|-------|----------|----------|
| 7 | Security Hardening | 4 weeks | CRITICAL |
| 8 | Compliance & Governance | 3 weeks | CRITICAL |
| 9 | Testing & Quality | 3 weeks | HIGH |
| 10 | Deployment & Operations | 2 weeks | MEDIUM |

---

## 🔐 Phase 7: Security Hardening (4 weeks)

**Goal:** Address critical security gaps from [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md)

### **Week 1: Authentication & Authorization**

**Tasks:**
1. Singpass/Corppass integration
   - Register application with Singpass
   - Implement OAuth 2.0 / OIDC flow
   - Handle authentication callbacks
   - Session management

2. Role-Based Access Control (RBAC)
   - Define roles: Assessor, Reviewer, Admin
   - Implement permission checks
   - Create role assignment UI

3. Multi-Factor Authentication (MFA)
   - SMS OTP integration
   - TOTP app support (Google Authenticator, etc.)
   - Backup codes

**Deliverables:**
- Working Singpass/Corppass login
- RBAC enforcement throughout application
- MFA enabled for all users

**Testing:**
- Authentication flow testing
- Permission boundary testing
- Session timeout testing

---

### **Week 2: Audit Trail Immutability**

**Tasks:**
1. Append-only BigQuery tables
   - Revoke UPDATE and DELETE permissions
   - Create separate admin service account
   - Test permission boundaries

2. Hash chaining implementation
   - Each record includes hash of previous record
   - Merkle tree for batch verification
   - Integrity check job (daily)

3. Audit log export
   - Export to Cloud Storage (cold storage)
   - Immutable object versioning
   - Retention policy (7 years)

**Deliverables:**
- Tamper-proof audit trail
- Automated integrity verification
- Cold storage backup

**Testing:**
- Attempt to modify records (should fail)
- Verify hash chain integrity
- Test recovery from backup

---

### **Week 3: Evidence Storage Immutability**

**Tasks:**
1. GCS Object Versioning
   - Enable versioning on evidence bucket
   - Configure retention policy (7 years)
   - Bucket Lock to prevent policy changes

2. Content-addressable storage
   - Store files by SHA-256 hash
   - Prevent duplicate storage
   - Verify file integrity on retrieval

3. Access logging
   - Enable Cloud Audit Logs for GCS
   - Monitor file access patterns
   - Alert on suspicious activity

**Deliverables:**
- Immutable evidence storage
- Version history for all files
- Comprehensive access logs

**Testing:**
- Attempt file deletion (should fail)
- Verify file versioning
- Test file recovery

---

### **Week 4: Rate Limiting & DDoS Protection**

**Tasks:**
1. User quotas
   - Track assessments per user per day
   - Configurable limits (e.g., 10/day)
   - Graceful degradation when limit hit

2. API rate limiting
   - Cloud Armor for DDoS protection
   - Rate limiting by IP (Cloud Run)
   - CAPTCHA for public endpoints

3. Cost monitoring
   - BigQuery cost alerts
   - Gemini API usage tracking
   - Budget alerts (GCP)

**Deliverables:**
- Per-user assessment quotas
- DDoS protection
- Cost monitoring and alerts

**Testing:**
- Exceed quota limits
- Load testing
- Cost projection testing

---

## ⚖️ Phase 8: Compliance & Governance (3 weeks)

**Goal:** Implement PDPA compliance and governance automation

### **Week 1: PDPA Data Subject Rights**

**Tasks:**
1. Data access endpoint
   - User can export all their data
   - JSON format with readable structure
   - Include all assessments, responses, evidence

2. Data correction workflow
   - User requests correction with justification
   - Admin approves/rejects
   - Audit trail of corrections

3. Data deletion endpoint
   - User requests deletion
   - Grace period (30 days)
   - Anonymization vs hard delete (compliance decision)

**Deliverables:**
- Self-service data export
- Correction request workflow
- Deletion mechanism

**Testing:**
- Export completeness
- Correction audit trail
- Deletion verification

**Legal Review Required:** Yes

---

### **Week 2: Automated Retention & Archival**

**Tasks:**
1. Retention policy automation
   - Cloud Scheduler job (daily)
   - Identify records > 7 years old
   - Automated archival to cold storage

2. Deletion workflow
   - User notification 30 days before deletion
   - Opt-in to extend retention
   - Secure deletion with verification

3. Archival format
   - Compressed JSON exports
   - Include all evidence files
   - Self-contained (can be restored)

**Deliverables:**
- Automated retention enforcement
- Cold storage archival
- User notification system

**Testing:**
- Simulate 7-year lifecycle
- Test archival and restoration
- Verify deletion completeness

---

### **Week 3: Peer Review Workflow**

**Tasks:**
1. Assessment states
   - Draft, Pending Review, Approved, Rejected, Stored
   - State transitions with business rules
   - Only approved assessments stored

2. Reviewer assignment
   - Automatic assignment based on agency/role
   - Conflict of interest checks
   - Workload balancing

3. Notification system
   - Email notifications for review requests
   - Slack integration (optional)
   - Dashboard for pending reviews

**Deliverables:**
- Multi-state workflow
- Reviewer assignment logic
- Notification infrastructure

**Testing:**
- State transition testing
- Reviewer assignment logic
- Notification delivery

---

## 🧪 Phase 9: Testing & Quality (3 weeks)

**Goal:** Comprehensive test coverage and quality assurance

### **Week 1: Unit Testing**

**Tasks:**
1. pytest setup
   - Configure pytest with coverage
   - Write unit tests for all modules
   - Target: 80%+ code coverage

2. Test modules (priority order):
   - Security module (validation, hashing)
   - Scoring calculator
   - BigQuery storage functions
   - Report generator
   - Input validators

3. Fixtures and factories
   - Test data generators
   - Mock objects for external services
   - Reusable test utilities

**Deliverables:**
- 80%+ code coverage
- ~200+ unit tests
- CI integration (GitHub Actions)

**Tools:**
- pytest
- pytest-cov (coverage)
- pytest-mock (mocking)

---

### **Week 2: Integration Testing**

**Tasks:**
1. LangGraph workflow tests
   - End-to-end workflow execution
   - Error handling scenarios
   - State persistence tests

2. Database integration tests
   - BigQuery read/write tests
   - Transaction handling
   - Error recovery

3. External API tests
   - Gemini API integration
   - Authentication flow
   - Rate limiting behavior

**Deliverables:**
- ~50+ integration tests
- Workflow test suite
- External service mocking

**Tools:**
- pytest
- testcontainers (if using Docker)
- VCR.py (API call recording)

---

### **Week 3: Security & Load Testing**

**Tasks:**
1. Security testing
   - OWASP Top 10 checks
   - Penetration testing (manual)
   - Dependency vulnerability scanning

2. Load testing
   - Concurrent user simulation
   - Performance benchmarks
   - Resource usage profiling

3. User acceptance testing (UAT)
   - Test with real users
   - Usability feedback
   - Bug fixes

**Deliverables:**
- Security audit report
- Load test results
- UAT feedback incorporated

**Tools:**
- Bandit (security linting)
- Safety (dependency checking)
- Locust (load testing)

---

## 🚀 Phase 10: Deployment & Operations (2 weeks)

**Goal:** Production deployment with monitoring and maintenance

### **Week 1: Containerization & CI/CD**

**Tasks:**
1. Docker containerization
   - Multi-stage Dockerfile
   - Optimize image size
   - Health check endpoints

2. Cloud Run deployment
   - Deploy to Cloud Run (asia-southeast1)
   - Configure scaling (min/max instances)
   - Set up custom domain

3. GitHub Actions CI/CD
   - Automated testing on PR
   - Automated deployment on merge to main
   - Rollback mechanism

**Deliverables:**
- Docker image
- Cloud Run deployment
- CI/CD pipeline

**Tools:**
- Docker
- Cloud Run
- GitHub Actions

---

### **Week 2: Monitoring & Documentation**

**Tasks:**
1. Observability setup
   - Cloud Logging integration
   - Cloud Monitoring dashboards
   - Error tracking (Sentry or Cloud Error Reporting)

2. Alerting
   - Error rate alerts
   - Performance degradation alerts
   - Cost threshold alerts

3. Operational documentation
   - Runbook for common issues
   - Disaster recovery plan
   - Incident response procedures

**Deliverables:**
- Monitoring dashboards
- Alert configuration
- Operational runbook

**Tools:**
- Cloud Logging
- Cloud Monitoring
- Sentry (optional)

---

## 📊 Phase Summary

| Phase | Weeks | Key Outcomes | Production Blockers Resolved |
|-------|-------|--------------|------------------------------|
| **7: Security** | 4 | Authentication, immutability, rate limiting | #1, #3, #4 |
| **8: Compliance** | 3 | PDPA rights, retention, peer review | #5, #6, #7 |
| **9: Testing** | 3 | 80% coverage, security audit, load tests | #8 |
| **10: Deployment** | 2 | Cloud Run, CI/CD, monitoring | #9, #10 |
| **TOTAL** | **12 weeks** | Production-ready system | All 10 gaps resolved |

---

## 💰 Estimated Costs

**One-Time Costs:**
- Security audit (external): $5,000 - $10,000 SGD
- Legal review (PDPA compliance): $3,000 - $5,000 SGD
- Penetration testing: $8,000 - $15,000 SGD

**Recurring Costs (Monthly):**
- GCP hosting (Cloud Run, BigQuery, Storage): $200 - $500 SGD
- Gemini API usage: $100 - $300 SGD (depends on volume)
- Monitoring tools (Sentry, etc.): $50 - $100 SGD
- Maintenance & support: Variable

**Total First-Year Cost:** ~$30,000 - $50,000 SGD

---

## 🎯 Success Criteria

**Phase 7 Complete When:**
- ✅ Singpass authentication working
- ✅ All audit logs tamper-proof
- ✅ Evidence files immutable
- ✅ Rate limiting enforced

**Phase 8 Complete When:**
- ✅ PDPA data rights implemented
- ✅ Retention policy automated
- ✅ Peer review workflow functional

**Phase 9 Complete When:**
- ✅ 80%+ test coverage achieved
- ✅ Security audit passed
- ✅ Load testing successful

**Phase 10 Complete When:**
- ✅ Production deployment live
- ✅ Monitoring dashboards operational
- ✅ Runbook documented

**Production-Ready When:**
- ✅ All 10 limitations from KNOWN_LIMITATIONS.md resolved
- ✅ Security audit passed with no critical issues
- ✅ Legal review approved for PDPA compliance
- ✅ Load testing shows system can handle expected traffic
- ✅ Disaster recovery plan tested

---

## 🚧 Risks & Mitigations

### **Risk 1: Singpass Integration Delays**
**Impact:** Cannot authenticate users  
**Mitigation:** Start Singpass registration early, have fallback plan (email OTP)

### **Risk 2: Security Audit Failures**
**Impact:** Cannot go to production  
**Mitigation:** Pre-audit security review, fix known issues proactively

### **Risk 3: Performance Issues**
**Impact:** Poor user experience  
**Mitigation:** Load testing early, optimize hot paths, caching strategy

### **Risk 4: Budget Overruns**
**Impact:** Project delayed or cancelled  
**Mitigation:** Phased approach, cost monitoring, regular budget reviews

### **Risk 5: PDPA Compliance Gaps**
**Impact:** Legal liability  
**Mitigation:** Legal review early, PDPA officer consultation, conservative approach

---

## 📚 Required Resources

**Personnel:**
- 1 Full-stack developer (12 weeks full-time)
- 1 Security engineer (4 weeks consulting)
- 1 Legal advisor (PDPA compliance review)
- 1 UX designer (1 week for UAT)

**External Services:**
- Security audit firm
- Penetration testing firm
- Legal firm (PDPA compliance)

**Infrastructure:**
- GCP account with billing
- Singpass developer account
- Domain name for production

---

## 🎓 Learning Opportunities

If these phases were implemented, additional learning outcomes:

**Phase 7:**
- OAuth 2.0 / OIDC flows
- Cryptographic security patterns
- DDoS mitigation strategies

**Phase 8:**
- PDPA compliance implementation
- Workflow state machines
- Notification systems

**Phase 9:**
- Test-driven development
- Security testing methodologies
- Performance optimization

**Phase 10:**
- Container orchestration
- CI/CD pipeline design
- Production monitoring

---

## 🔄 Maintenance After Launch

**Ongoing Activities:**
- Security patch updates (monthly)
- Dependency updates (quarterly)
- Framework updates (when AI Verify releases new versions)
- User feedback incorporation
- Performance optimization
- Cost optimization

**Estimated Ongoing Effort:** 10-15 hours/month

---

## 📌 Decision Gates

**Gate 1: Proceed with Phase 7?**
- ✅ Government agency committed to deployment
- ✅ Budget approved
- ✅ Singpass access granted
- ✅ Security audit commissioned

**Gate 2: Proceed with Phase 8?**
- ✅ Phase 7 complete and tested
- ✅ Legal review initiated
- ✅ PDPA officer assigned

**Gate 3: Proceed with Phase 9?**
- ✅ Phase 7-8 complete
- ✅ Code freeze for testing period
- ✅ UAT users identified

**Gate 4: Proceed with Phase 10?**
- ✅ All tests passing
- ✅ Security audit passed
- ✅ Legal review approved
- ✅ Production environment ready

---

## 🎯 Alternative: Minimum Viable Production (MVP)

If full 12-week roadmap is not feasible, a **6-week MVP** could include:

**Week 1-2:** Authentication (basic email/password, no Singpass)  
**Week 3:** Audit trail immutability (hash chaining only)  
**Week 4:** Unit tests for critical paths  
**Week 5:** Docker + Cloud Run deployment  
**Week 6:** Basic monitoring + runbook  

**Trade-offs:**
- ❌ No Singpass (less secure)
- ❌ No peer review workflow
- ❌ No PDPA automation
- ✅ Still better than current v1.0
- ✅ Faster to market

---

## 📝 Conclusion

This roadmap transforms a **portfolio project** into a **production system** in 12-16 weeks.

**Current Status:** v1.0 (portfolio-ready, not production-ready)  
**After Roadmap:** v2.0 (production-ready, government-deployable)  

**Key Message:**  
The gap between portfolio and production is **well-understood and plannable**. The project demonstrates core capabilities; the roadmap demonstrates production awareness.

---

## 🔗 Related Documentation

- [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) — What needs fixing
- [PROJECT_FINAL_STATUS.md](PROJECT_FINAL_STATUS.md) — What exists now
- [README.md](../README.md) — Project overview

---

**Last Updated:** 31 March 2026  
**Document Version:** 1.0  
**Author:** Chan
