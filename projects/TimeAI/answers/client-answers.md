# Client Answers: TimeAI
## Responses from Sarah Chen, Director of Research Operations — Feb 6, 2026

### General / Business

1. **Implementation Phases**: We'd like a phased approach. Phase 1 should focus on search and discovery — getting accountants finding memos fast. Phase 2 adds the drafting and AI analysis features. Phase 3 is the knowledge graph visualization. We want Phase 1 live within 3 months.

2. **Success Metrics**: Currently our accountants spend 2-4 hours per research task manually searching through folders and email chains. We'd consider it a success if Time AI brings that down to under 30 minutes. We also want to track adoption rate — at least 80% of accountants using it weekly within 2 months of launch.

3. **User Adoption Strategy**: We'll run a pilot with 15 senior accountants first, gather feedback, then roll out firm-wide. We need the UI to be simple — our accountants are not tech-savvy. Think Google-simple search bar, not complex dashboards.

4. **Budget Constraints**: We have a budget of approximately $150K-200K for the initial build. We're open to using premium LLM services (Claude or GPT-4) as long as monthly API costs stay reasonable — under $2K/month at full usage. No open-source LLM requirement.

### Data

5. **Memo Corpus Volume**: We have approximately 12,000 memos spanning from 1978 to present. Total size is roughly 8GB. About 200-400 new memos are added per year.

6. **Data Format & Quality**: About 60% are PDFs (many from scanned documents pre-2005), 30% are Word documents, and 10% are plain text or email exports. The pre-2000 scanned PDFs will need OCR — roughly 3,000 documents. Quality varies significantly for older documents.

7. **Metadata Consistency**: It's messy, honestly. Before 2010, there was no standard naming convention. Personnel names have variations (Robert Smith vs. R. Smith vs. Bob Smith). Guidance references are somewhat consistent but use different citation formats across decades. We'd need the system to handle fuzzy matching.

8. **Content Sensitivity**: Yes — about 20% of memos reference specific client situations. These should be accessible to all internal users but never exposed externally. No memos should leave our network. We don't need per-client access restrictions internally though — all accountants can see all memos.

9. **Data Migration Timeline**: We can provide the full corpus within 2 weeks of project kickoff. It's currently on a shared network drive. We'll also assign a librarian (Janet) as a data quality point person.

### Users & Access

10. **User Base Scale**: Initial pilot: 15 users. Full deployment: 85 accountants across the firm. Maximum including admin staff: 120 users.

11. **Role-Based Access**: Keep it simple — two roles. Regular users (accountants) can search, view, and draft memos. Admin users (partners + IT) can manage the corpus, add/remove memos, and see usage analytics. No need for complex per-document permissions.

12. **Authentication Integration**: We use Microsoft 365 / Azure AD for everything. Time AI must integrate with our Azure AD for SSO. No separate login.

13. **Multi-Office Access**: We have 3 offices (New York, Chicago, Boston) but everyone accesses the same memo corpus. No geographic restrictions. Standard cloud access is fine.

### Technical

14. **Existing System Integration**: We use iManage for document management. It would be great if users can import memos from iManage and export drafted memos back. We also use Thomson Reuters Checkpoint for guidance references — linking to their references would be a nice-to-have but not required for Phase 1.

15. **Deployment Preference**: Cloud on Azure — we're already an Azure shop with our M365 setup. Must be within US data centers only.

16. **LLM Requirements**: No specific preference — whatever gives the best results for accounting content. We're fine with cloud-based LLM APIs (Claude or GPT-4). No on-premises LLM requirement. Data is sensitive but standard cloud security with encryption is acceptable.

17. **Performance Expectations**: Search results should appear within 2 seconds. LLM-generated analysis can take up to 10 seconds — accountants are patient if the results are good. Memo draft generation can take up to 30 seconds.

18. **Concurrent Usage**: Realistically, peak usage is Monday mornings — probably 40-50 simultaneous users. Average is 15-20 concurrent.

### Semantic Search & Discovery

19. **Search Filtering Requirements**: Key filters needed: date range, guidance topic (ASC codes), author/personnel, memo type (research memo, client memo, internal guidance), and keyword. Nice-to-have: industry sector filter.

20. **Search Result Volume**: Show 10 results initially with infinite scroll or "load more." Maximum useful set is probably 50 results — beyond that, they need to refine their search.

21. **Graph Relationships**: The most important relationships are: memo ↔ guidance topics (ASC references), memo ↔ author, memo ↔ related memos (cross-references), and guidance topic ↔ guidance topic (hierarchy). Client industry would be useful but is not in our current metadata.

### Content Analysis & Explanation

22. **Explanation Detail Level**: We want a brief summary first (2-3 bullet points on key similarities/differences), with the option to "expand" for a detailed paragraph explanation. Accountants want to skim quickly, then deep-dive when needed.

23. **Relevance Scoring**: Yes — show a percentage relevance score. Our accountants are analytical and want to know why something was surfaced. A brief "matched because..." tag under each result would be very helpful.

### Memo Management & Viewing

24. **Memo Versioning**: We don't currently version memos. If a memo is updated, the new version replaces the old one. But we'd like the system to keep the previous version accessible (version history) — just don't show it in search results by default.

25. **Export Requirements**: PDF and Word export are must-haves. Exported memos should maintain our firm's letterhead template and formatting. We'll provide the template.

### Memo Drafting & Creation

26. **Draft Approval Workflow**: Yes — drafted memos should be saved as "Draft" status. A partner or manager must review and change status to "Approved" before it enters the searchable corpus. Drafts should only be visible to the author and designated reviewers.

27. **Template Standardization**: We have 3 standard memo templates: Research Memo, Client Advisory Memo, and Internal Guidance Note. Each has a specific format. We'll provide the templates. The AI should populate the correct template based on memo type.

28. **Collaboration Features**: Single-user creation is fine for Phase 1. Collaboration can come later. The author can share a draft link with a reviewer — that's sufficient.

### Compliance & Security

29. **Regulatory Requirements**: We need to comply with our firm's internal information security policy (based on ISO 27001 guidelines). No specific SOX requirements for this system. Data retention: all memos must be retained indefinitely.

30. **Audit Trail Requirements**: Log all searches (who searched what, when), memo access (who viewed which memo), and all draft creation/editing/approval actions. We need to be able to export audit logs for compliance reviews.

31. **Data Backup & Recovery**: Daily backups with 4-hour RPO (recovery point objective). System should be recoverable within 24 hours. Standard for non-critical business systems in our firm.
