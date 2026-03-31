import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# In a production environment, these categories would be pulled dynamically from your Tag database.
# For now, we define a static library of expected campus subjects and courses to train the vectorizer.
PREDEFINED_CATEGORIES = {
    "Computer Science - Operating Systems": "kernel memory process thread deadlock scheduling filesystem linux windows concurrency",
    "Computer Science - Database Systems": "sql relational algebra normalization indexing transaction concurrency postgresql mysql nosql",
    "Mathematics - Linear Algebra": "matrix vector eigenvalue eigenvector determinant subspace orthogonal transformation",
    "Engineering - Lab Report": "experiment methodology results discussion conclusion abstract apparatus calibration",
}

class ResourceClassifier:
    def __init__(self, threshold=0.6):
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(
            stop_words='english', 
            max_features=20 # Extract the top 20 weighted keywords as the feature vector
        )
        self.category_names = list(PREDEFINED_CATEGORIES.keys())
        self.category_texts = list(PREDEFINED_CATEGORIES.values())
        
        # Pre-calculate the TF-IDF vectors for our predefined categories
        self.category_vectors = self.vectorizer.fit_transform(self.category_texts)

    def _clean_text(self, text):
        """Standardizes text by removing special characters and making it lowercase."""
        if not text:
            return ""
        # Remove non-alphanumeric characters and extra whitespace
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.lower().strip()

    def classify_text(self, extracted_text):
        """
        Takes raw extracted text, cleans it, calculates its TF-IDF vector,
        and uses Cosine Similarity against predefined categories.
        """
        cleaned_text = self._clean_text(extracted_text)
        
        if not cleaned_text:
             return {"status": "PENDING", "suggested_tags": []}

        # Transform the incoming document into the same vector space
        doc_vector = self.vectorizer.transform([cleaned_text])
        
        # Calculate cosine similarity between the document and all categories
        similarities = cosine_similarity(doc_vector, self.category_vectors).flatten()
        
        # Find the best match
        best_match_index = np.argmax(similarities)
        highest_score = similarities[best_match_index]
        
        # Apply the threshold logic
        if highest_score >= self.threshold:
            return {
                "status": "AUTO_FILED",
                "suggested_tags": [self.category_names[best_match_index]],
                "confidence_score": round(highest_score, 4)
            }
        else:
            # If it falls below the threshold, flag for manual review, but still offer the best guess
            return {
                "status": "PENDING",
                "suggested_tags": [self.category_names[best_match_index]] if highest_score > 0 else [],
                "confidence_score": round(highest_score, 4)
            }

# Initialize a global instance of the classifier to be used by the views
classifier = ResourceClassifier(threshold=0.15) # Set low initially for testing with small text samples