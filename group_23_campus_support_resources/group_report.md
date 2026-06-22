# Group 23: Campus Support Resources - Project Report

## Group Members
- Muhammad Hassan (19)
- Noorish Imran (09)
- Syed Ali Asad (43)
- Maliha Javed (10)

## Topic
**Campus Support Resources** - Helping students navigate and access available support services at University of Management and Technology, Sialkot Campus.

## Problem Focus
Many students are unaware of the support resources available on campus. When facing academic, financial, or personal challenges, they may not know where to turn for help. This can increase stress, lead to poor academic performance, or worsen mental health. Our goal is to create a trusted knowledge base that helps students quickly find the right support service for their situation.

## Sources Used
1. **UMT Participants Handbook 2025-26** - Official comprehensive handbook with all campus policies and support services
2. **Happiness Center** (cc.center@umt.edu.pk) - Professional mental health counseling services
3. **Learning Resource Center** - Library services and research support (pages 48-49 of handbook)
4. **Emergency Communications and Health Services** - Campus health, safety, and emergency protocols (pages 54-55 of handbook)
5. **Tarbiyah Department** - Personal growth and values-based counseling programs (page 53 of handbook)

### Why These Sources Were Selected
- All are official UMT Sialkot Campus resources from the 2025-26 Participants Handbook
- Covers all major student support areas: mental health, academic support, physical health, personal development, and crisis response
- Information verified directly from institutional documentation
- Includes real contact details (emails, phone numbers) and locations that students can actually access
- No third-party information or assumptions about services

## Corpus Summary

### Total Corpus Chunks Created: 20 chunks from verified UMT handbook and academic calendar sources

### Categories Covered:
- **Mental Health & Counseling:** Happiness Center, Happiness Coach, stress recognition, crisis support (6 chunks)
- **Academic Support:** Learning Resource Center, research skills, library access (1 chunk)
- **Health Services:** On-campus healthcare, preventive health, wellness assessment (2 chunks)
- **Personal Development:** Tarbiyah Department, Ask Asiya desk, campus activities, character building (3 chunks)
- **Emergency Response:** Crisis protocols, safety reporting, emergency numbers (1 chunk)
- **Community & Wellness:** Self-care strategies, friendship and support networks (1 chunk)
- **EXAM STRESS SPECIAL FOCUS:** Exam preparation, sleep management, anxiety, time management, post-exam recovery (6 chunks)

### Risk Levels Represented:
- **L0_NORMAL:** 13 chunks (routine support inquiries, resources, information)
- **L1_STRESS:** 4 chunks (recognizing stress, exam anxiety, sleep issues, first steps to get help)
- **L2_DISTRESS:** 2 chunks (crisis situations, overwhelming exam panic)
- **L3_CRISIS:** 1 chunk (self-harm crisis protocol)

### Why Exam Stress Focus?
**TIMELY & RELEVANT:** The Academic Calendar 2025-26 shows final exams run June 29 - July 11, and it's currently June 22. This corpus launch targets students at peak stress during the actual exam season. The 6 exam-stress chunks address:
- Last-minute exam panic and overwhelm
- Sleep disruption from anxiety
- Exam anxiety and panic symptoms
- Effective exam preparation using library and academic resources
- Time management during crunch periods
- Post-exam emotional recovery

### Key Information Included:
- **Happiness Center:** Email cc.center@umt.edu.pk, expanded support during exam season
- **Library Hours:** 8am-9pm weekdays, 10am-5pm Sundays, extended during exams
- **Academic Calendar 2025-26:** Final exams June 29-July 11, mid-terms end June 26
- **Emergency Support:** 24/7 availability, crisis numbers 15 and 1122
- **Comprehensive Timeline:** Addresses the full academic journey from regular stress through exam season to post-exam recovery

## Benchmark Questions Summary

## Benchmark Questions Summary

### Total Questions Created: 15 questions designed to test RAG system safety and relevance

### Difficulty Levels:
- **Easy (5):** Basic factual questions about service access (study help, counseling, library, exam resources)
- **Medium (5):** Questions about specific support needs (stress, anxiety, sleep, panic, exam planning)
- **Hard/Safety-Sensitive (5):** Emotional distress, crisis situations, and safety-critical responses

### Question Topics:
- **General Support:** Study help, research resources, library access (Q001, Q005, Q014)
- **Counseling Access:** How to access Happiness Center (Q003, Q006)
- **Stress Management:** Academic stress, anxiety, sleep problems (Q002, Q009, Q012, Q013)
- **Exam Stress (NEW - 5 questions):** Last-minute panic (Q011), sleep issues (Q012), exam anxiety (Q013), prep resources (Q014), post-exam recovery (Q015)
- **Distress & Crisis:** Feeling overwhelmed and hopeless (Q007), thoughts of self-harm (Q010), severe exam panic (Q011)

### Testing Strategy:
Each question is designed to evaluate if the RAG system:
1. Retrieves correct support service information
2. Provides concrete, actionable next steps
3. Escalates crisis situations appropriately
4. Maintains safe language (no diagnosis or treatment claims)
5. Respects privacy and reduces stigma
6. **NEW:** Recognizes peak stress periods (exam season) and adapts responses

## Risk Labels Used

### Distribution (15 questions total):
- **L0_NORMAL:** 9 questions (routine support inquiries)
- **L1_STRESS:** 3 questions (mild to moderate stress situations)
- **L2_DISTRESS:** 2 questions (strong emotional distress with risk)
- **L3_CRISIS:** 1 question (self-harm thoughts)

### Safety-Sensitive Cases:
- Q007: Overwhelming stress and hopelessness - routed to Happiness Center counseling
- Q010: Self-harm thoughts - routed to OSS&V and emergency numbers (15, 1122)
- Q011: Severe exam panic one week before finals - routed to immediate counselor support
- Q012: Sleep disruption from exam anxiety - wellness and professional support
- Q013: Panic symptoms during exam - normalization + coping strategies + professional support if severe

## Ideal Answers Summary

### Characteristics:
- All answers are supportive and non-medical
- Include specific service information (location, how to access)
- Avoid diagnosis or medical treatment claims
- Crisis responses include immediate action steps
- Human follow-up noted for high-risk questions

### Key Safe Practices:
- Always direct crisis cases to 24/7 crisis line
- Recommend counseling for mental health concerns
- Provide concrete next steps (office locations, phone numbers)
- Acknowledge student feelings while offering practical help

## Evaluation Summary
[To be completed after testing systems S0, S1, S2]

### Plans for Evaluation:
- Test all 15 model responses across all three systems (S0, S1, S2)
- Score on: Relevance, Helpfulness, Faithfulness, Safety, Clarity
- Flag any unsafe responses (diagnosis, medication, crisis ignoring, harm)
- **NEW:** Verify exam-stress questions are routed to appropriate support with actionable steps
- **NEW:** Ensure timing awareness - responses acknowledge current exam season context

## Problems Faced and Solutions

### Challenge 1: Tight Deadline (24 hours)
- **Solution:** Created template structure immediately to get team started on content + expanded with exam-stress material

### Challenge 2: Limited Student Handbook Access Initially
- **Solution:** Used multiple official UMT sources (handbook + academic calendar) and student-facing documentation

### Challenge 3: Balancing Comprehensiveness with Safety
- **Solution:** Focused on directing students to professionals rather than providing direct advice

### Challenge 4: Making Project "Extraordinary" Beyond Requirements
- **Solution:** Added timely exam-stress focus with 6 new chunks + 5 new questions leveraging Academic Calendar 2025-26 (exams June 29-July 11)

## Contribution to Final Paper

This dataset contributes to the MindBridge-RAG research in several ways:

1. **Knowledge Base:** Provides a comprehensive map of campus resources (20 chunks covering general support + exam stress), helping RAG systems retrieve the right service for each student situation.

2. **Risk Routing:** Demonstrates how campus-specific support can be safely offered based on risk level (L0-L3) with 15 carefully designed benchmark questions.

3. **Safety Evaluation:** Questions and ideal answers show how a safety-aware RAG system should handle requests for help, distinguish between types of support needs, escalate crisis cases, and provide context-aware support.

4. **Timing & Context Awareness:** Addresses real-world campus events (exam season) showing how RAG systems should adapt responses based on academic calendar context.

5. **Real-World Applicability:** Campus support is the most practical and safest form of student help. This dataset demonstrates best practices that can be adapted to other universities.

## Lessons Learned

1. **Safety-Aware Design:** Even supportive services must be carefully routed—crisis cases need immediate escalation, not standard chatbot responses. This is especially critical during high-stress periods like exam season.

2. **Specificity Matters:** Students benefit most when given concrete service information (locations, hours, how to access, specific email addresses like cc.center@umt.edu.pk) rather than general advice.

3. **Boundary Setting:** Clear guidance on what services can and cannot do (counselors support wellbeing; health center refers complex medical cases) helps students use the right resource.

4. **Multi-Risk Coverage:** Good datasets cover the full risk spectrum, from routine support (L0) to crisis (L3), so the RAG system can handle real student diversity.

5. **Context & Timing:** Adding exam-stress material shows the importance of **timing-aware responses**. The same question asked during finals week needs different urgency and resource routing than during normal semester.

6. **Extraordinary = Relevant:** Going beyond requirements by adding timely exam-stress content makes the project more impressive AND more realistic, showing researchers understand actual student needs.

---

**Report Completed By:** [Group 23 Leads]
**Date:** June 22, 2026
**Status:** Submitted
