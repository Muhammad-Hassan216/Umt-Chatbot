# Group 23: Campus Support Resources - Cleaned Verified Corpus Report

## Group Members
- Muhammad Hassan (19)
- Noorish Imran (09)
- Syed Ali Asad (43)
- Maliha Javed (10)

## Scope of This Revision
This revision removes unsupported, speculative, and non-auditable claims from the dataset and keeps only handbook-backed or explicitly verified contact/routing information.

## Sources Used (Auditable)
1. UMT Participants Handbook 2025-26 (primary policy source)
2. Happiness Center contact: cc.center@umt.edu.pk
3. LRC references from handbook Section 16
4. Emergency Communications / OSS&V references from handbook Section 21
5. Tarbiyah Department listed in handbook Section 20
6. UMT Sialkot official contact page for campus phone/address/email

## Corpus Summary
- Total corpus chunks: 35
- Kept content types:
  - Verified support routing (Happiness Center, OSS&V, emergency numbers)
  - Verified campus contacts (City and Iqbal campuses)
  - Handbook extracts for portal/admin procedures (registration, unfreeze, results/portal, FT clearance)
  - Handbook extracts for fee/probation/scholarship policy

## Removed/Reduced Content
- Removed unsupported health-clinic physician/nurse claims
- Removed hard-coded academic-calendar exam date claims
- Removed named Happiness Coach/location details
- Removed speculative hostel guidance and generic wellness advice presented as official fact
- Removed broad non-audited web-scraped expansion from corpus generation path

## Benchmark Set Summary
- Total benchmark questions: 24
- Focus: verified contact, emergency routing, portal/admin tasks, fee/probation/scholarship policy, and safe distress escalation

## Risk Distribution
- L0_NORMAL: 20
- L1_STRESS: 1
- L2_DISTRESS: 1
- L3_CRISIS: 2

## Safety Notes
- L3 responses must include immediate escalation (15/1122 + OSS&V).
- Responses avoid medical diagnosis and unsupported operational guarantees.
- Users are directed to official channels for latest policy/contact updates.
