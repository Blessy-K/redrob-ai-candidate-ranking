\# Methodology



\## Objective



Build an intelligent candidate ranking system that ranks candidates beyond simple keyword matching by combining semantic similarity with recruiter-centric signals.



\## Approach



\### 1. Candidate Filtering



Candidates are first filtered using AI-related keywords such as:



\- AI

\- ML

\- Machine Learning

\- Python

\- NLP

\- LLM

\- Retrieval

\- Ranking

\- Embedding

\- Vector



This reduces computation while retaining relevant candidates.



\### 2. Semantic Matching



The Job Description and candidate profiles are converted into dense embeddings using the Sentence Transformer model:



\- all-MiniLM-L6-v2



Cosine similarity is computed using normalized embeddings.



\### 3. Experience Scoring



Candidates with approximately 5–9 years of experience receive the highest experience score because this aligns with the job description.



\### 4. Behavioral Signals



Behavioral features are incorporated using:



\- Profile completeness

\- GitHub activity

\- Recruiter response rate



These signals improve ranking by favoring active and engaged candidates.



\### 5. Skill Bonus



Additional score is awarded for candidates mentioning relevant technologies including:



\- Retrieval

\- Embeddings

\- Ranking

\- FAISS

\- Pinecone

\- Milvus

\- Vector Search

\- NLP

\- LLM

\- Python



\### 6. Penalty



Candidates whose primary background is unrelated to the role receive a small penalty, including domains such as:



\- Robotics

\- Speech Recognition

\- Computer Vision

\- Marketing



\### 7. Final Ranking



The final score combines:



\- Semantic similarity

\- Experience

\- Behavioral signals

\- Skill bonus

\- Penalty



Candidates are sorted in descending order, duplicate IDs are removed, and the Top 100 are exported in the required submission format.



\## Explainability



Each ranked candidate includes a short explanation describing:



\- Current role

\- Years of experience

\- Number of AI-related skills

\- Recruiter response rate



This makes the ranking interpretable and suitable for recruiter review.



\## Future Improvements



\- Cross-encoder reranking

\- Learning-to-Rank models

\- Hybrid BM25 + Dense Retrieval

\- Better semantic skill extraction

\- More advanced behavioral feature engineering

