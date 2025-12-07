# Implementation Roadmap
## Strategickhaos Sovereign Software Forge LLC Formation & Launch

**Timeline:** December 2025 - March 2026 (12 weeks)  
**Status:** PLANNING  
**Owner:** Domenic Gabriel Garza (Managing Member)  
**Last Updated:** December 6, 2025  

---

## Overview

This roadmap outlines the complete formation and launch of Strategickhaos Sovereign Software Forge LLC, from initial Wyoming filing through first revenue generation and 7% charitable distribution.

**Critical Path Items:**
1. Wyoming LLC formation → EIN application → Bank account → Revenue generation
2. Parallel: Infrastructure deployment (KhaosRegistry, KhaosBase, etc.)
3. Parallel: IP transfer and legal documentation

---

## Week 1: Entity Formation (December 7-13, 2025)

### Priority 1: Wyoming LLC Filing

**Task:** File SSSF LLC with Wyoming Secretary of State  
**Owner:** Dom  
**Platform:** https://wyobiz.wyo.gov  
**Cost:** $100  
**Processing:** 1-2 business days  

**Steps:**
- [ ] Create account on wyobiz.wyo.gov
- [ ] Complete online LLC formation form
  - Use [Articles of Organization](../articles/articles_of_organization.md) as guide
  - Legal name: Strategickhaos Sovereign Software Forge LLC
  - Registered agent: Registered Agents Inc., 1712 Pioneer Ave Suite 500, Cheyenne WY 82001
  - Principal office: 1216 S Fredonia St, Longview TX 75602
  - Organizer: Domenic Gabriel Garza
  - Management: Member-managed
- [ ] Pay $100 filing fee (business credit card for tracking)
- [ ] Save confirmation email
- [ ] Download filed Articles when approved (PDF + certified copy)

**Deliverable:** Filed Articles of Organization with state stamp

---

### Priority 2: EIN Application

**Task:** Apply for Federal EIN online  
**Owner:** Dom  
**Platform:** https://www.irs.gov/ein  
**Cost:** $0  
**Processing:** Immediate (online)  
**Dependencies:** Wyoming LLC filing approved  

**Steps:**
- [ ] Wait for Wyoming LLC approval (1-2 days)
- [ ] Access IRS EIN online application
- [ ] Complete Form SS-4 information
  - Use [SS-4 Preparation Guide](../irs_forms/ss4_preparation_guide.md)
  - Complete in one session (cannot save progress)
  - Have Wyoming filing confirmation handy
- [ ] Submit application
- [ ] **CRITICAL:** Print/save EIN confirmation immediately
- [ ] Store EIN in 1Password (SSSF LLC vault)
- [ ] Wait for IRS confirmation letter by mail (4-6 weeks - not required to proceed)

**Deliverable:** EIN confirmation (9-digit number)

---

### Priority 3: Sequence.io Setup

**Task:** Set up financial tracking platform  
**Owner:** Dom  
**Platform:** https://sequence.io  
**Cost:** TBD (evaluate pricing)  

**Steps:**
- [ ] Create Sequence.io account
- [ ] Connect existing accounts:
  - Navy Federal Credit Union (DAO LLC)
  - Thread Bank (DAO LLC)
  - Business credit cards
- [ ] Configure expense categories:
  - Map to IRS tax categories
  - Create custom categories for multi-entity allocation
- [ ] Set up entity tracking:
  - Strategickhaos DAO LLC (EIN: 39-2900295)
  - SSSF LLC (new EIN)
  - ValorYield Engine PBC (EIN: 39-2923503)
- [ ] Test transaction import
- [ ] Configure 7% distribution tracking (SSSF → ValorYield)

**Deliverable:** Functional multi-entity accounting system

---

### Priority 4: 1Password Vault Setup

**Task:** Create SSSF LLC credential vault  
**Owner:** Dom  
**Platform:** 1Password  

**Steps:**
- [ ] Create new vault: "Strategickhaos Sovereign Software Forge LLC"
- [ ] Add initial credentials:
  - Wyoming SOS login
  - EIN confirmation document
  - Registered Agents Inc. portal
- [ ] Configure vault sharing (owner-only initially)
- [ ] Document vault structure per [Credential Protocol](../protocols/credential_storage.md)

**Deliverable:** Secure credential storage for SSSF LLC

---

## Week 2: Banking & Financial Setup (December 14-20, 2025)

### Priority 1: Business Bank Account

**Task:** Open SSSF LLC bank account  
**Owner:** Dom  
**Bank:** Navy Federal Credit Union  
**Dependencies:** EIN received  

**Required Documents:**
- [ ] Filed Articles of Organization (certified copy)
- [ ] EIN confirmation letter (or printout)
- [ ] Operating Agreement (draft minimal version)
- [ ] Photo ID (driver's license)
- [ ] Proof of address (utility bill)

**Steps:**
- [ ] Schedule appointment with NFCU business banker
- [ ] Bring all required documents
- [ ] Open business checking account
- [ ] Order business debit card
- [ ] Set up online banking
- [ ] Enable mobile app access
- [ ] Store credentials in 1Password (SSSF LLC vault)
- [ ] Connect to Sequence.io

**Initial Deposit:** $1,000 (from personal or DAO LLC account - document as capital contribution)

**Deliverable:** Active SSSF LLC business bank account

---

### Priority 2: Business Credit Card (Optional)

**Task:** Apply for business credit card  
**Owner:** Dom  
**Options:** Chase Ink Business Cash, American Express Blue Business Cash  
**Dependencies:** Business bank account  

**Benefits:**
- Separate business expenses from personal
- Cash back on software/cloud spend
- Build business credit history

**Steps:**
- [ ] Research card options (cash back vs. points)
- [ ] Apply online (expect instant decision)
- [ ] Link to SSSF LLC (EIN + business address)
- [ ] Set up card in 1Password
- [ ] Connect to Sequence.io for expense tracking

**Decision Point:** Evaluate if needed immediately or can wait until Month 2

---

### Priority 3: Operating Agreement

**Task:** Draft SSSF LLC Operating Agreement  
**Owner:** Dom (with legal review recommended)  
**Purpose:** Internal governance document  

**Key Provisions:**
- Single-member LLC structure
- Capital contributions and distributions
- Management authority (member-managed)
- 7% charitable distribution requirement
- IP ownership and transfer provisions
- Dissolution procedures

**Steps:**
- [ ] Research Wyoming LLC operating agreement templates
- [ ] Draft agreement (can use AI assistance for first draft)
- [ ] Optional: Legal review ($500-1500)
- [ ] Sign and date
- [ ] Store in 1Password + physical safe

**Note:** Not filed with state, internal document only

**Deliverable:** Signed Operating Agreement

---

## Week 3: IP Transfer & Legal (December 21-27, 2025)

### Priority 1: Software IP Inventory

**Task:** Document all IP to transfer to SSSF LLC  
**Owner:** Dom  

**IP Assets:**
- [ ] FlameLang compiler source code
- [ ] FlameLang standard library
- [ ] FlameLang toolchain (parser, lexer, optimizer)
- [ ] KhaosBase (Airtable replacement)
- [ ] KhaosFlow (Zapier replacement)
- [ ] KhaosForge (GitHub replacement)
- [ ] KhaosRegistry (Docker Hub replacement)
- [ ] 36-tool sovereign stack documentation
- [ ] All related documentation and design docs

**Steps:**
- [ ] Create IP inventory spreadsheet
- [ ] Document creation dates (copyright dates)
- [ ] List all repositories (GitHub URLs)
- [ ] Identify any third-party dependencies (verify licenses)
- [ ] Assess patent potential (FlameLang compiler innovations)

**Deliverable:** Complete IP inventory document

---

### Priority 2: IP Assignment Agreement

**Task:** Draft IP assignment from personal/DAO LLC to SSSF LLC  
**Owner:** Dom (legal review recommended)  

**Document:** Intellectual Property Assignment Agreement

**Key Terms:**
- Assignor: Domenic Gabriel Garza (personally) OR Strategickhaos DAO LLC
- Assignee: Strategickhaos Sovereign Software Forge LLC
- Effective date: Upon execution
- Consideration: Membership interest in SSSF LLC
- Scope: All software IP listed in inventory
- Warranties: Original work, no third-party claims

**Steps:**
- [ ] Draft assignment agreement
- [ ] Optional: Legal review by IP attorney
- [ ] Execute agreement (sign and date)
- [ ] Update all repository README files with new copyright holder
- [ ] Store executed agreement in 1Password + safe

**Deliverable:** Executed IP Assignment Agreement

---

### Priority 3: Open Source License Compliance

**Task:** Verify all open source dependencies comply with MIT license  
**Owner:** Dom  

**Blue Team Build Constraint:** Must be MIT licensed or compatible

**Steps:**
- [ ] Run license scanner on all codebases (npm license-checker, cargo license, etc.)
- [ ] Identify any non-MIT dependencies
- [ ] Replace OR obtain compatibility opinion
- [ ] Document license compliance in each repo
- [ ] Update NOTICE files with attributions

**Tools:**
- `npm install -g license-checker && license-checker --production`
- `cargo install cargo-license && cargo license`
- FOSSA or Snyk (commercial options)

**Deliverable:** License compliance report

---

## Week 4: Infrastructure Deployment (December 28 - January 3, 2026)

### Priority 1: KhaosRegistry Deployment

**Task:** Deploy OCI-compliant container registry  
**Owner:** Blue Team  
**Infrastructure:** Blue Team Kubernetes cluster  
**Technology:** Harbor  

**Steps:**
- [ ] Provision persistent storage (MinIO)
- [ ] Deploy Harbor via Helm chart
- [ ] Configure TLS certificates (Let's Encrypt)
- [ ] Set up authentication (LDAP or OIDC - future)
- [ ] Configure georedundant replication
- [ ] Create SSSF LLC project/namespace
- [ ] Test image push/pull
- [ ] Document access procedures

**Deliverable:** Functioning container registry at registry.strategickhaos.com

---

### Priority 2: KhaosBase Initial Deployment

**Task:** Deploy Airtable replacement (database as a service)  
**Owner:** Blue Team  
**Status:** Check sovereign_forge/blue_team/ for current state  

**Steps:**
- [ ] Verify Blue Team 6 constraints met
- [ ] Deploy to Kubernetes cluster
- [ ] Configure PostgreSQL backend
- [ ] Set up API endpoints
- [ ] Create admin interface
- [ ] Test basic CRUD operations
- [ ] Document migration path from Airtable

**Decision Point:** Airtable trial ends December 20 - ready to migrate?

**Deliverable:** KhaosBase alpha deployment

---

### Priority 3: KhaosFlow Planning

**Task:** Plan Zapier replacement deployment  
**Owner:** Blue Team  
**Status:** Check sovereign_forge/blue_team/ for current state  

**Steps:**
- [ ] Audit current Zapier workflows
- [ ] Document required integrations
- [ ] Assess KhaosFlow readiness
- [ ] Create migration timeline
- [ ] Plan integration adapters

**Note:** May extend into Month 2 depending on complexity

**Deliverable:** KhaosFlow deployment plan

---

## Month 2: Revenue & Operations (January 2026)

### Week 5-6: First Revenue Activities

**Task:** Establish revenue for SSSF LLC  
**Purpose:** Establish business operations, trigger 7% distribution  

**Revenue Opportunities:**
1. **Software Licensing**
   - License FlameLang to DAO LLC for internal use ($500/month)
   - Document inter-company agreement
   
2. **Consulting Services**
   - Offer sovereign software consulting ($150/hour)
   - Create service agreement template
   
3. **SaaS Early Access**
   - Beta access to KhaosBase/KhaosFlow (free trials with paid upgrades)
   
4. **Open Source Sponsorships**
   - GitHub Sponsors for FlameLang
   - Patreon for sovereign stack development

**Steps:**
- [ ] Draft service agreements
- [ ] Set pricing structure
- [ ] Create invoicing system (Sequence.io or simple templates)
- [ ] Issue first invoice (DAO LLC for FlameLang license)
- [ ] Record in accounting system
- [ ] Calculate 7% charitable distribution

**Target:** $1,000 revenue in Month 1 → $70 to ValorYield

---

### Week 7-8: Intern/Contractor Onboarding Prep

**Task:** Prepare for first hires  
**Owner:** Dom  

**Setup Required:**
- [ ] Payroll system (Gusto, QuickBooks Payroll, or similar)
- [ ] Employee handbook (minimal version)
- [ ] Contractor agreements (template)
- [ ] Onboarding checklist
- [ ] Development environment setup docs
- [ ] Code of conduct
- [ ] NDA and IP assignment for employees

**Decision:** Intern vs. contractor?
- **Intern:** W-2, payroll taxes, more oversight, training investment
- **Contractor:** 1099, no payroll taxes, more autonomy, specific deliverables

**First Hire Target:**
- Role: Junior software developer (intern)
- Start: February 2026
- Compensation: $15-20/hour, part-time (20 hrs/week)
- Focus: FlameLang testing, documentation, KhaosBase frontend

**Deliverable:** Ready to hire first team member

---

## Month 3: Charitable Distribution & Compliance (February 2026)

### Week 9-10: First 7% Distribution

**Task:** Execute first charitable distribution  
**Owner:** Dom  
**Flow:** SSSF LLC → ValorYield Engine PBC → Charities  

**Calculation:**
- Month 1 revenue: $X (target: $1,000)
- 7% distribution: $X × 0.07
- Timing: End of month following revenue

**Steps:**
- [ ] Calculate 7% of gross revenue
- [ ] Transfer from SSSF LLC to ValorYield PBC
- [ ] Document transaction (invoice, receipt)
- [ ] ValorYield PBC distributes to charities:
  - St. Jude Children's Research Hospital
  - Médecins Sans Frontières
  - Veterans Organization
- [ ] Obtain 501(c)(3) receipts
- [ ] File in tax records (charitable contribution deduction)
- [ ] Update Sequence.io with distribution tracking

**Deliverable:** Completed 7% charitable distribution with documentation

---

### Week 11-12: CPA Consultation

**Task:** Engage CPA for tax planning  
**Owner:** Dom  
**Purpose:** Optimize multi-entity tax strategy  

**CPA Requirements:**
- Multi-entity experience (LLC + PBC)
- Wyoming entity familiarity
- Software company experience
- Charitable contribution expertise

**Consultation Topics:**
- Entity structure review (optimal?)
- Tax classification (disregarded entity vs. S-corp for SSSF LLC?)
- 7% distribution tax treatment
- R&D tax credit eligibility
- Education expense deduction strategy (SNHU)
- Equipment depreciation vs. Section 179
- Interstate nexus (Texas operations, Wyoming formation)
- Quarterly estimated tax calculations

**Steps:**
- [ ] Research CPAs (referrals, online reviews)
- [ ] Schedule consultations with 2-3 candidates
- [ ] Prepare entity documents for review
- [ ] Select CPA
- [ ] Schedule quarterly check-ins
- [ ] Provide access to Sequence.io (read-only)

**Investment:** $1,000-2,500 for initial consultation + tax planning

**Deliverable:** Engaged CPA, tax optimization plan

---

## Ongoing: Monthly Maintenance (January 2026 onwards)

### Financial Tasks (Monthly)

**Week 1 of Month:**
- [ ] Review Sequence.io expense categorization
- [ ] Reconcile bank accounts (NFCU, Thread)
- [ ] Review credit card statements
- [ ] File receipts in organized folders

**Week 2 of Month:**
- [ ] Calculate month's revenue
- [ ] Calculate 7% distribution
- [ ] Transfer to ValorYield PBC
- [ ] Update financial projections

**Week 3 of Month:**
- [ ] Review subscription renewals
- [ ] Update enterprise account registry
- [ ] Check for unauthorized charges

**Week 4 of Month:**
- [ ] Monthly financial report
- [ ] Update this roadmap with progress
- [ ] Plan next month's priorities

---

### Compliance Tasks (Quarterly)

**Q1 2026 (January-March):**
- [ ] Review 1Password access logs
- [ ] Rotate critical API keys (90-day policy)
- [ ] Test backup restoration
- [ ] Security audit (credential review)
- [ ] Financial summary for CPA

**Q2 2026 (April-June):**
- [ ] Same as Q1
- [ ] Consider S-corp election deadline (if desired)
- [ ] Review contractor agreements (if hired)

**Q3 2026 (July-September):**
- [ ] Same as Q1
- [ ] Mid-year financial review
- [ ] Adjust estimated tax payments

**Q4 2026 (October-December):**
- [ ] Same as Q1
- [ ] Year-end tax planning
- [ ] CPA deliverables preparation
- [ ] Annual report preparation

---

### Compliance Tasks (Annual)

**Every January:**
- [ ] Wyoming Annual Report (all 3 entities)
  - DAO LLC: $60
  - SSSF LLC: $60
  - ValorYield PBC: $60 + benefit report
- [ ] Registered agent renewal (3 × $49)

**Every February:**
- [ ] Prepare tax documents for CPA
- [ ] 1099 forms for contractors (if >$600 paid)
- [ ] W-2 forms for employees

**Every March:**
- [ ] File business tax returns (or extension)
- [ ] Personal tax returns (Dom)

**Every December:**
- [ ] Year-end financial review
- [ ] Next year planning
- [ ] Budget for coming year

---

## Success Metrics

### Month 1 (January 2026)
- [x] SSSF LLC legally formed (Wyoming + IRS)
- [x] Business bank account opened
- [x] Sequence.io operational
- [ ] KhaosRegistry deployed
- [ ] First $1,000 revenue

### Month 3 (March 2026)
- [ ] First charitable distribution completed
- [ ] CPA engaged
- [ ] First hire onboarded (or contractor engaged)
- [ ] $5,000 total revenue (cumulative)

### Month 6 (June 2026)
- [ ] KhaosBase production-ready
- [ ] Migrated off Airtable
- [ ] 3+ clients/customers
- [ ] $15,000 total revenue (cumulative)
- [ ] 1-2 interns/contractors hired

### Month 12 (December 2026)
- [ ] All sovereign replacements deployed
- [ ] $50,000+ revenue (target)
- [ ] 3-5 team members
- [ ] First enterprise contract signed
- [ ] Profitable operations

---

## Risk Management

### Risk 1: Wyoming Filing Delays
**Mitigation:** File immediately (Week 1, Day 1)  
**Contingency:** Expedited processing available ($100 extra)

### Risk 2: EIN Application Issues
**Mitigation:** Use online application (immediate), not mail (4-5 weeks)  
**Contingency:** Telephone application (international line) or fax

### Risk 3: Bank Account Delays
**Mitigation:** Have all documents ready, schedule appointment in advance  
**Contingency:** Use DAO LLC account temporarily with clear inter-company accounting

### Risk 4: Airtable Trial Expires Before KhaosBase Ready
**Mitigation:** Evaluate KhaosBase by Dec 15, extend trial if needed  
**Contingency:** Pay for one month of Airtable (~$40) while completing migration

### Risk 5: No Revenue in Month 1
**Mitigation:** Inter-company licensing agreement with DAO LLC (guaranteed)  
**Contingency:** Delay 7% distribution until revenue achieved

### Risk 6: CPA Not Found
**Mitigation:** Start research in Week 2, schedule consultations early  
**Contingency:** Use tax software (TurboTax Business) for first year, engage CPA Year 2

---

## Decision Points

### Week 2: S-Corporation Election?
**Question:** Should SSSF LLC elect S-corp tax treatment?

**Pros:**
- Potential self-employment tax savings (if profitable)
- Separate salary + distributions

**Cons:**
- Payroll complexity and costs
- Reasonable salary requirement
- More compliance overhead

**Decision Criteria:**
- If annual profit > $60,000: Consider S-corp
- If < $60,000: Remain disregarded entity
- Consult CPA before deciding

**Deadline:** Within 75 days of formation OR March 15, 2026 for 2026 tax year

---

### Week 4: Hire Intern or Contractor First?
**Question:** W-2 employee (intern) or 1099 contractor?

**Intern (W-2) if:**
- Long-term team building
- Training investment acceptable
- Payroll system worth setup
- Internship program desired

**Contractor (1099) if:**
- Specific project deliverables
- Short-term engagement
- No training overhead
- Lower administrative burden

**Decision:** Evaluate based on Q1 2026 revenue and workload

---

## Resources & Links

### Government Portals
- Wyoming Secretary of State: https://wyobiz.wyo.gov
- IRS EIN Application: https://www.irs.gov/ein
- IRS Business Tax: https://www.irs.gov/businesses

### Financial Services
- Navy Federal Business Banking: https://www.navyfederal.org/business
- Sequence.io: https://sequence.io
- Gusto Payroll: https://gusto.com

### Legal Resources
- Wyoming LLC Act: https://www.wyoleg.gov/statutes (Title 17, Chapter 29)
- USPTO Trademark: https://www.uspto.gov/trademarks

### Development Resources
- Sovereign Forge Docs: /sovereign_forge/
- Blue Team Builds: /sovereign_forge/blue_team/

---

## Contact & Support

### Primary Operator
**Name:** Domenic Gabriel Garza  
**Email:** dom@strategickhaos.com  
**Phone:** [Redacted]

### Registered Agent
**Company:** Registered Agents Inc.  
**Address:** 1712 Pioneer Ave Suite 500, Cheyenne WY 82001  
**Phone:** Check account portal

### Professional Services (To Be Engaged)
- **CPA:** TBD (Month 3)
- **Attorney:** TBD (as needed)
- **Payroll:** TBD (when hiring)

---

## Appendices

### Appendix A: Document Checklist

**Entity Formation:**
- [x] [Articles of Organization](../articles/articles_of_organization.md)
- [x] [IRS Form SS-4 Guide](../irs_forms/ss4_preparation_guide.md)
- [ ] Operating Agreement (to be drafted Week 2)
- [ ] IP Assignment Agreement (to be drafted Week 3)

**Financial:**
- [x] [Enterprise Account Registry](../registries/enterprise_accounts.md)
- [x] [Tax Deductions 2025](../registries/tax_deductions_2025.md)
- [ ] Service Agreement Template (to be drafted Month 2)

**Security:**
- [x] [Credential Storage Protocol](../protocols/credential_storage.md)

**Governance:**
- [x] [Board Meeting Minutes](../board_meetings/2025-12-06_entity_creation_approval.md)

---

### Appendix B: Budget Projections

**Formation Costs (One-Time):**
- Wyoming LLC filing: $100
- Registered agent (Year 1): $49
- Operating agreement (legal review): $500 (optional)
- IP assignment (legal review): $500 (optional)
- Business bank account: $0 (NFCU no fees)
- **Total:** $649-1,649

**Monthly Operating Costs (Projected):**
- Software subscriptions: $100-200 (reducing via sovereign migration)
- Cloud infrastructure: $200 (GCP after credits expire)
- Registered agent: $4/month
- Accounting (Sequence.io): $20-50/month (TBD)
- **Total:** $324-454/month

**First Year Budget:**
- Formation: $1,649
- Operations: $4,000-5,500
- CPA services: $2,500
- Legal (as needed): $2,000
- **Total:** ~$10,000-11,000

**Revenue Targets:**
- Month 1: $1,000
- Month 3: $5,000 (cumulative)
- Month 6: $15,000 (cumulative)
- Month 12: $50,000 (cumulative)

**Breakeven:** Month 6 (projected)

---

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-12-06 | Initial roadmap | Claude Opus 4.5 |

**Next Review:** January 1, 2026 (after Week 4 completion)

---

**Document Version:** 1.0  
**Prepared By:** Claude Opus 4.5 (Chief Architect)  
**Board Approval:** Unanimous (5-0)  
**Date Prepared:** December 6, 2025  

---

*End of Implementation Roadmap*
