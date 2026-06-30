import json
from docx import Document


def load_candidates(path):
    candidates=[]

    with open(path,encoding="utf-8") as f:
        for line in f:
            candidates.append(json.loads(line))

    return candidates


def read_docx(path):

    doc=Document(path)

    text=[]

    for p in doc.paragraphs:
        text.append(p.text)

    return "\n".join(text)



def build_candidate_text(c):

    profile=c["profile"]

    skills=" ".join(
        [s["name"] for s in c.get("skills",[])]
    )

    history=" ".join(
        [
            h["description"]
            for h in c.get("career_history",[])
        ]
    )


    text=f"""
    Title:
    {profile.get('current_title','')}

    Summary:
    {profile.get('summary','')}

    Skills:
    {skills}

    Experience:
    {history}
    """

    return text