\# Intelligent Candidate Discovery \& Ranking



\## Overview



This project implements an AI-powered candidate ranking system for the Redrob Hackathon.



The system combines semantic similarity, candidate experience, behavioral signals, and skill matching to rank the top candidates for a given job description.



\## Methodology



\- Read the job description.

\- Load candidate profiles.

\- Filter candidates using AI-related keywords.

\- Generate embeddings using the all-MiniLM-L6-v2 Sentence Transformer.

\- Compute semantic similarity between the job description and candidate profiles.

\- Combine similarity with:

&#x20; - Experience score

&#x20; - Recruiter response rate

&#x20; - GitHub activity

&#x20; - Profile completeness

&#x20; - Skill bonus

&#x20; - Domain mismatch penalty

\- Generate the Top 100 ranked candidates with reasoning.



\## Tech Stack



\- Python

\- Sentence Transformers

\- pandas

\- scikit-learn

\- tqdm



\## Run



```bash

python src/rank\_candidates.py

```



\## Output



The script generates:



\- `outputs/submission.csv`



which follows the required competition submission format.

