from transformers import pipeline
import PyPDF2
from docx import Document

nlp = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

gri_topics = ["energy", "water", "emissions", "waste", "social", "governance"]

def extract_text(file):
    if file.name.endswith("pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages])
    elif file.name.endswith("docx"):
        doc = Document(file)
        return " ".join([p.text for p in doc.paragraphs])
    return ""

def classify_texts(files):
    all_labels = {}
    for f in files:
        text = extract_text(f)
        if text:
            result = nlp(text, candidate_labels=gri_topics)
            all_labels[f.name] = dict(zip(result["labels"], result["scores"]))
    return all_labels