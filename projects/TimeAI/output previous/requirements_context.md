--- [TimeAIOverview.pdf] (pdf) ---
[Page 1]
Time AI Overview
OVERVIEW
Time AI is a memo research and drafting tool for professional accountants. Its primary goals are to:
• Store a large corpus of accounting memos (dating back to the 1970s).
• Allow semantic search across memos using context‐rich retrieval.
• Provide guidance on memo relevance (similarities/differences) via a Large Language Model (LLM).
• Let users read, summarize, and create new memos based on retrieved content.
• The application leverages a Retrieval Augmented Generation (RAG) approach, which integrates a
search layer for retrieving relevant memos and an LLM for generating summarized or newly drafted
memos.
KEY FEATURES
GRAPH‐BASED SEMANTIC SEARCH
• Stores memos and all relevant metadata—title, creation date, guidance references, associated
managers—in a knowledge graph.
• Employs vector embeddings or other semantic algorithms for similarity searches.
• Leverages relationships (e.g., memo topics, references) to boost relevant retrieval.
MEMO EXPLANATION
For each retrieved memo, an LLM generates concise text on:
• Similarities: how the memo responds to user’s query.
• Differences: potential gaps or differences in scope.
SUMMARIZATION
• Users can request a high‐level overview of any memo.
• The LLM condenses the memo into key points on classification, guidance references, relevant
background, etc.
DRAFTING NEW MEMOS
• Users supply new “fact patterns” for their client’s scenario.
• The system draws on retrieved memos’ content and an LLM to propose a draft structure
(introduction, analysis, conclusion).
• Users can refine or finalize that draft, then store it within Time AI for future reference.

[Page 2]
ARCHITECTURE OVERVIEW
DATA & STORAGE
• Memos Date Range: Spanning multiple decades, from 1970s onward.
• Possible Approach:
o Store memo texts, structured metadata (date, guidance references, etc.), and
precomputed embeddings to aid semantic search.
o Maintain a system for indexing newly created memos.
• Scalability: Should allow for quick retrieval from a large historical corpus.
GRAPHRAG DESIGN
Knowledge Graph Query
• When a user performs a search, the system identifies relevant graph nodes and edges that match
the query (via embeddings or graph traversal).
• Top relevant items are surfaced for LLM processing.
Augmented Generation
• The LLM references the retrieved nodes (memos, topics, relationships) to develop explanations,
summaries, or new content.
APPLICATION LOGIC & USER EXPERIENCE
Frontend
• Renders pages for searching, displaying results, reading memos, and drafting new memos.
• Sends user queries and new fact patterns to the backend.
Backend
• Interfaces with storage and indexing systems.
• Manages calls to the LLM for commentary, summarization, and memo drafting.
• Stores newly created memos with relevant metadata.
WIREFRAMES & USER FLOWS
SEARCH PAGE
• A search box for keywords or queries.
• Optional filters (e.g., by guidance topic, Partner/Managing Director, Manager, etc.).
• A “Search” button that initiates a semantic search across the memo corpus.

[Page 3]
User Flow
1. User enters query and/or filters.
2. The system returns a list of relevant memos.
RESULTS LIST
• Displays memo search outcomes in a list containing memo metadata (e.g., ID, Title, Guidance,
etc.).
• Shows a brief “Similarities” and “Differences” analysis for each memo.
• Allows users to take actions: “Read” the memo, “Summarize” it, or “Draft New” memo based on it.
User Flow
1. User reviews short LLM‐generated commentary on how each memo aligns or diverges from the
query.
2. User can open the memo in detail, get an LLM summary, or start drafting a new memo
immediately.
MEMO DETAIL VIEW
• Presents the full text of the selected memo.
• Shows relevant metadata (title, clearance date, guidance references, prior consultations).
• Repeats the “Similarities” and “Differences” highlights so the user can quickly recall how it relates
to their query.
• Provides “Draft New” as a shortcut to generating a new memo off this content or “Summarize” to
condense the memo.
User Flow
1. User navigates here from the results list.
2. They can read the detailed content or request an instant summary.
3. When ready, they can jump to drafting a new memo.
MEMO SUMMARY VIEW
• An abridged bullet‐point version of the memo content via LLM summarization.
• Key accounting topics (equity vs. liability, embedded derivatives, etc.).
• “Draft New” enables the user to create a new memo, incorporating references from the
summarized content.

[Page 4]
User Flow
1. Users seeking a quick read can glance at the summary.
2. They can proceed to “Draft New” once they confirm relevance.
CONCLUSION
Time AI provides a modern approach for accountants to discover and reuse valuable memo insights
through a combination of semantic search, LLM‐generated commentary, and automated drafting. By
storing extensive memo history, offering context‐rich retrieval, and enabling new memo creation, Time AI
streamlines the research and documentation processes.