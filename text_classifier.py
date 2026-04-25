# ============================================
# FILE: text_classifier.py
# ============================================
import PyPDF2
from docx import Document
import re
from collections import Counter

class TextClassifier:
    def __init__(self):
        self.gri_keywords = {
            'GRI 302: Energy': ['energy', 'electricity', 'fuel', 'consumption', 'kwh', 'megawatt', 'renewable'],
            'GRI 303: Water': ['water', 'withdrawal', 'discharge', 'consumption', 'aquifer', 'wastewater'],
            'GRI 305: Emissions': ['emission', 'ghg', 'carbon', 'co2', 'methane', 'greenhouse', 'offset'],
            'GRI 306: Waste': ['waste', 'landfill', 'recycling', 'hazardous', 'disposal', 'circular'],
            'GRI 403: Health': ['safety', 'accident', 'injury', 'health', 'incident', 'training']
        }
        
        self.sentiment_keywords = {
            'positive': ['improved', 'reduced', 'achieved', 'success', 'target met', 'exceeded'],
            'negative': ['increase', violation, 'failure', 'exceeded limit', 'non-compliance']
        }
    
    def classify_documents(self, doc_files):
        results = []
        
        for doc_file in doc_files:
            text = self._extract_text(doc_file)
            
            if not text:
                continue
            
            # GRI scoring
            gri_scores = {}
            for standard, keywords in self.gri_keywords.items():
                score = sum(text.lower().count(keyword) for keyword in keywords)
                gri_scores[standard] = min(1.0, score / 20)
            
            # Extract key phrases
            words = re.findall(r'\b\w+\b', text.lower())
            word_freq = Counter(words)
            common_words = word_freq.most_common(20)
            key_phrases = [word for word, count in common_words if len(word) > 3 and count > 1][:15]
            
            # Sentiment analysis
            sentiment_score = 0
            for sentiment, keywords in self.sentiment_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        sentiment_score += 1 if sentiment == 'positive' else -1
            
            sentiment = 'positive' if sentiment_score > 0 else 'negative' if sentiment_score < 0 else 'neutral'
            
            results.append({
                'filename': doc_file.name,
                'gri_scores': gri_scores,
                'key_phrases': key_phrases,
                'sentiment': sentiment,
                'sentiment_score': sentiment_score / 10 if sentiment_score != 0 else 0.5
            })
        
        return results
    
    def _extract_text(self, doc_file):
        text = ""
        try:
            if doc_file.name.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(doc_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            elif doc_file.name.endswith('.docx'):
                doc = Document(doc_file)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
        except:
            return ""
        return text