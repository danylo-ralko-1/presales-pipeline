# Client Questions: TimeAI

# CLIENT QUESTIONS

## General / Business

1. **Implementation Phases**: Do you want to deploy Time AI in phases (e.g., search first, then drafting) or as a complete system? This affects development timeline and resource allocation.

2. **Success Metrics**: How do you currently measure research efficiency, and what specific improvements would constitute success (e.g., 50% reduction in research time)? This determines performance benchmarks and ROI measurement.

3. **User Adoption Strategy**: How do you plan to transition accountants from current research methods to Time AI? This affects UI complexity and training requirements.

4. **Budget Constraints**: Are there budget limitations that would affect technology choices (e.g., premium LLM services vs. open-source alternatives)? This impacts architecture decisions.

## Data

5. **Memo Corpus Volume**: Approximately how many memos span from the 1970s to present, and what's the total data size? This affects storage architecture and search performance optimization.

6. **Data Format & Quality**: What formats are the historical memos in (PDF, Word, scanned images), and what percentage require OCR or data cleaning? This determines data ingestion complexity and timeline.

7. **Metadata Consistency**: How standardized are guidance references, personnel names, and dates across different decades? Inconsistent metadata affects knowledge graph design and search accuracy.

8. **Content Sensitivity**: Do any memos contain client-confidential information requiring special handling or access restrictions? This affects security architecture and data classification.

9. **Data Migration Timeline**: When can the historical memo corpus be made available for ingestion? This affects project scheduling and testing phases.

## Users & Access

10. **User Base Scale**: How many accountants will use the system initially and at full deployment? This affects infrastructure sizing and licensing costs.

11. **Role-Based Access**: Do different user levels (staff, managers, partners) need access to different memo subsets or system features? This determines authorization complexity.

12. **Authentication Integration**: Do you have existing SSO or Active Directory systems that Time AI must integrate with? This affects authentication architecture.

13. **Multi-Office Access**: Will users from different offices or regions access the same memo corpus, and are there any geographic data restrictions? This affects deployment architecture.

## Technical

14. **Existing System Integration**: What document management, accounting software, or other systems must Time AI integrate with for memo export/import? This affects API requirements and data flow design.

15. **Deployment Preference**: Do you prefer cloud deployment (AWS, Azure, GCP) or on-premises hosting due to security/compliance requirements? This determines infrastructure architecture.

16. **LLM Requirements**: Do you have preferences for specific LLM providers, or are there requirements for on-premises LLM deployment due to data sensitivity? This affects AI architecture and costs.

17. **Performance Expectations**: What are acceptable response times for search queries and LLM-generated content (e.g., <3 seconds for search results)? This affects caching strategy and infrastructure sizing.

18. **Concurrent Usage**: What's the expected peak number of simultaneous users during busy periods? This affects system capacity planning.

## Semantic Search & Discovery

19. **Search Filtering Requirements**: Beyond the mentioned guidance topic and personnel filters, what other metadata filters are important (date ranges, memo types, client industries)? This affects search interface design.

20. **Search Result Volume**: How many search results should be displayed initially, and what's the maximum useful result set size? This affects pagination and relevance ranking.

21. **Graph Relationships**: Besides memo topics and personnel, what other relationships should the knowledge graph capture (client types, accounting standards, cross-references)? This affects graph schema design.

## Content Analysis & Explanation

22. **Explanation Detail Level**: How detailed should the LLM-generated similarities/differences analysis be (brief bullets vs. paragraph explanations)? This affects prompt engineering and response formatting.

23. **Relevance Scoring**: Should the system display numerical relevance scores or confidence levels for memo matches? This affects algorithm transparency and user trust.

## Memo Management & Viewing

24. **Memo Versioning**: How should the system handle multiple versions of the same memo or updates to historical memos? This affects data model and version control strategy.

25. **Export Requirements**: What formats do users need for memo export (PDF, Word, plain text), and are there formatting requirements? This affects document generation capabilities.

## Memo Drafting & Creation

26. **Draft Approval Workflow**: Do new memos require review/approval before being stored in the searchable corpus? This affects workflow design and user permissions.

27. **Template Standardization**: Are there standard memo formats or templates that drafts should follow? This affects draft generation prompts and formatting.

28. **Collaboration Features**: Do multiple users need to collaborate on memo drafts, or is it single-user creation? This affects editing interface and version control.

## Compliance & Security

29. **Regulatory Requirements**: What compliance standards must the system meet (SOX, industry regulations, data retention policies)? This affects security architecture and audit capabilities.

30. **Audit Trail Requirements**: What user actions need logging for compliance (searches, memo access, draft creation)? This affects logging design and data retention.

31. **Data Backup & Recovery**: What are your requirements for data backup frequency and disaster recovery time objectives? This affects backup strategy and infrastructure redundancy.

---

**Default Assumptions if Questions Remain Unanswered:**
- Single-phase deployment with all features
- Cloud deployment on major provider (AWS/Azure)
- Standard business authentication (no complex SSO initially)
- 100-500 concurrent users maximum
- PDF/Word export capabilities
- Basic audit logging for compliance
- Standard memo templates with flexible customization