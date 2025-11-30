# File: backend/app/services/parser.py
import fitz  # PyMuPDF
import re

class ResumeParser:
    def extract_text(self, file_path: str) -> str:
        """
        Opens PDF, extracts text from all pages, and cleans whitespace.
        """
        try:
            doc = fitz.open(file_path)
            full_text = []

            for page in doc:
                # "text" preserves natural reading order better than raw bytes
                text = page.get_text("text")
                full_text.append(text)
            
            # Join all pages and clean it
            return self._clean_text("\n".join(full_text))
            
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""

    def _clean_text(self, text: str) -> str:
        """
        Removes extra newlines and weird spacing to save tokens for the AI.
        """
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n+', '\n', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()