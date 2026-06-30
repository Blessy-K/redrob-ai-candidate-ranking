import os
import pandas as pd
from tqdm import tqdm

from sentence_transformers import SentenceTransformer

from utils import (
    load_candidates,
    read_docx,
    build_candidate_text
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


CAND_FILE = os.path.join(
    BASE_DIR,
    "candidates.jsonl"
)

JOB_FILE = os.path.join(
    BASE_DIR,
    "job_description.docx"
)

OUTPUT = os.path.join(
    BASE_DIR,
    "outputs",
    "ranked_candidates.csv"
)


print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


print("Reading JD")

job_text = read_docx(JOB_FILE)


print("Loading candidates")

candidates = load_candidates(
    CAND_FILE
)


filtered = []


for c in tqdm(candidates):

    profile = c["profile"]

    title = profile.get(
        "current_title",
        ""
    ).lower()


    skills = " ".join(
        [
            s["name"]
            for s in c.get("skills", [])
        ]
    ).lower()


    keywords = [
        "ai",
        "ml",
        "machine learning",
        "data",
        "backend",
        "engineer",
        "python",
        "nlp",
        "llm",
        "retrieval",
        "ranking",
        "embedding",
        "vector"
    ]


    match = sum(
        1 for k in keywords
        if k in title + " " + skills
    )


    if (
    match >= 3
    or (
        5 <= profile.get("years_of_experience", 0) <= 9
        and "engineer" in title
    )
    ):
       filtered.append(c)



print(
    "Candidates after filtering:",
    len(filtered)
)


filtered = sorted(
    filtered,
    key=lambda c: (
        c.get("redrob_signals", {}).get("profile_completeness_score", 0),
        c.get("redrob_signals", {}).get("github_activity_score", 0),
        c.get("redrob_signals", {}).get("recruiter_response_rate", 0)
    ),
    reverse=True
)

candidates = filtered[:5000]
print("Candidates used for embedding:", len(candidates))


texts = []


for c in candidates:
    texts.append(
        build_candidate_text(c)
    )



print("Creating candidate embeddings")


candidate_embeddings = model.encode(
    texts,
    batch_size=256,
    show_progress_bar=True,
    normalize_embeddings=True
)



job_embedding = model.encode(
    [job_text],
    normalize_embeddings=True
)



print("Calculating similarity")


similarities = (
    candidate_embeddings @ job_embedding.T
).flatten()



results = []


for i,c in enumerate(candidates):

    signals = c.get(
        "redrob_signals",
        {}
    )


    exp = c["profile"].get(
        "years_of_experience",
        0
    )


    experience_score = (
        1 if 5 <= exp <= 9 else 0.5
    )


    behavior = (
        signals.get(
            "profile_completeness_score",
            0
        ) / 100
        +
        signals.get(
            "github_activity_score",
            0
        ) / 10
        +
        signals.get(
            "recruiter_response_rate",
            0
        )
    ) / 3



    text = texts[i].lower()



    bonus = 0


    strong_skills = [
        "embedding",
        "retrieval",
        "ranking",
        "vector",
        "faiss",
        "milvus",
        "pinecone",
        "nlp",
        "llm",
        "python",
        "machine learning"
    ]


    for skill in strong_skills:
        if skill in text:
            bonus += 0.02



    penalty = 0


    bad_signals = [
        "speech recognition",
        "computer vision",
        "robotics",
        "marketing manager"
    ]


    for item in bad_signals:
        if item in text:
            penalty -= 0.03



    final_score = (
        similarities[i] * 0.60
        +
        experience_score * 0.20
        +
        behavior * 0.15
        +
        bonus
        +
        penalty
    )


    results.append(
    {
        "candidate_id": c["candidate_id"],
        "score": float(final_score) / 1.5
    }
)



df = pd.DataFrame(results)

df = (
    df.sort_values(
        by=["score", "candidate_id"],
        ascending=[False, True]
    )
    .drop_duplicates(subset=["candidate_id"])
    .head(100)
    .reset_index(drop=True)
)
adjusted_scores = []

for i, score in enumerate(df["score"]):
    adjusted_scores.append(
        round(score - (i * 0.0001), 4)
    )

df["score"] = adjusted_scores

ranks = []
reasoning = []

for i, row in df.iterrows():

    candidate = next(
        c for c in candidates
        if c["candidate_id"] == row["candidate_id"]
    )

    profile = candidate["profile"]

    title = profile.get(
        "current_title",
        "Unknown"
    )

    exp = profile.get(
        "years_of_experience",
        0
    )

    skills = [
        s["name"]
        for s in candidate.get("skills", [])
    ]

    ai_keywords = [
        "python",
        "machine learning",
        "ml",
        "ai",
        "llm",
        "nlp",
        "retrieval",
        "embedding",
        "vector",
        "ranking",
        "faiss",
        "pinecone",
        "milvus"
    ]

    ai_count = sum(
        1
        for skill in skills
        if any(
            k in skill.lower()
            for k in ai_keywords
        )
    )

    response = candidate.get(
        "redrob_signals",
        {}
    ).get(
        "recruiter_response_rate",
        0
    )

    ranks.append(i + 1)

    reasoning.append(
        f"{title} with {exp:.1f} yrs; {ai_count} AI core skills; response rate {response:.2f}."
    )

df["rank"] = ranks
df["reasoning"] = reasoning

df = df[
    [
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ]
]

df.to_csv(
    "outputs/submission.csv",
    index=False
)

print("Completed")
print(df.head(10))