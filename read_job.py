from docx import Document

doc = Document("job_description.docx")

text = ""

for p in doc.paragraphs:
    text += p.text + "\n"

print(text)