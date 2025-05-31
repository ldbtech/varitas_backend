from typing import List, Dict, Tuple
from datetime import datetime
import google.generativeai as genai
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

class CreateASummary:
    """
    This class is responsible for:
    1. Processing articles about the same topic from different sources
    2. Using Gemini LLM to create a comprehensive summary
    3. Managing references and source attribution
    """
    def __init__(self):
        self.summary = None
        self.references = []
        # Initialize Gemini
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        
    def process_articles(self, 
                        articles: List[Dict], 
                        embeddings: np.ndarray,
                        threshold: float = 0.7) -> Dict:
        """
        Process articles about the same topic from different sources and generate a comprehensive summary
        
        Args:
            articles: List of article dictionaries about the same topic
            embeddings: Pre-computed embeddings for the articles
            threshold: Similarity threshold (not used in this version as articles are about same topic)
            
        Returns:
            Dictionary containing the summary and references
        """
        if not articles or not embeddings:
            return {"error": "No articles or embeddings provided"}
            
        if len(articles) != len(embeddings):
            return {"error": "Number of articles and embeddings must match"}
            
        # Prepare context for Gemini with all articles
        context = """Please create a comprehensive summary of the following news articles about the same topic.
        Focus on:
        1. Key developments and facts that are consistent across sources
        2. Unique perspectives or additional details from each source
        3. Timeline of events if mentioned
        4. Different viewpoints or reactions if present
        
        Articles:
        """
        
        for i, article in enumerate(articles, 1):
            context += f"\nSource {i} - {article.get('source', {}).get('name', 'N/A')}:\n"
            context += f"Title: {article.get('title', 'N/A')}\n"
            context += f"Description: {article.get('description', 'N/A')}\n"
            if article.get('content'):
                context += f"Content: {article.get('content', 'N/A')}\n"
            context += f"Published: {article.get('publishedAt', 'N/A')}\n"
            
        # Generate comprehensive summary using Gemini
        response = self.gemini_model.generate_content(
            context + "\nCreate a comprehensive summary that combines information from all sources, highlighting both common facts and unique perspectives."
        )
        
        # Add references
        for article in articles:
            self.references.append({
                "title": article.get("title", "N/A"),
                "source": article.get("source", {}).get("name", "N/A"),
                "author": article.get("author", "N/A"),
                "published_at": article.get("publishedAt", "N/A"),
                "url": article.get("url", "N/A")
            })
        
        # Generate a final title using Gemini
        title_prompt = f"""Based on this comprehensive summary of multiple sources, create a clear and informative title that captures the main story:
        
        {response.text}"""
        title_response = self.gemini_model.generate_content(title_prompt)
        
        self.summary = {
            "title": title_response.text.strip(),
            "main_content": response.text,
            "references": self.references,
            "generated_at": datetime.utcnow().isoformat(),
            "source_count": len(articles)
        }
        
        return self.summary
    
    def get_summary(self) -> Dict:
        """Return the generated summary"""
        if not self.summary:
            return {"error": "No summary available. Call process_articles() first."}
        return self.summary
