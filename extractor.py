import pdfplumber
import os
from interfaces import IExtractor
from typing import List, Any, Dict

class PlumberGridExtractor(IExtractor):
    def __init__(self, settings: Dict[str, Any] = None):
        # UPDATED SETTINGS:
        # 1. vertical_strategy="lines": We trust the vertical lines to separate columns (Jan, Feb, Mar).
        # 2. horizontal_strategy="text": We use TEXT positions to separate rows, because the PDF lacks horizontal lines between data rows.
        self.settings = settings or {
            "vertical_strategy": "lines", 
            "horizontal_strategy": "text",  # <--- CHANGED FROM "lines" TO "text"
            "snap_tolerance": 3,
            "intersection_x_tolerance": 5,
        }

    def extract(self, file_path: str) -> Dict[str, List[List[Any]]]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        extracted_content = {}

        try:
            with pdfplumber.open(file_path) as pdf:
                print(f"Debug: PDF opened. Total pages: {len(pdf.pages)}")
                
                for i, page in enumerate(pdf.pages):
                    page_label = f"Page {i + 1}"
                    
                    # Extract tables using the updated hybrid settings
                    tables = page.extract_tables(self.settings)
                    
                    if not tables:
                        print(f"Debug: No tables found on {page_label}. Trying fallback strategy...")
                        # Fallback: If lines strategy fails completely, try pure text strategy
                        # This helps if the PDF has NO lines at all (e.g., whitespace only)
                        fallback_settings = {
                            "vertical_strategy": "text",
                            "horizontal_strategy": "text",
                            "snap_tolerance": 3,
                        }
                        tables = page.extract_tables(fallback_settings)
                    
                    if not tables:
                        print(f"Debug: Still no tables found on {page_label}. Skipping.")
                        continue

                    page_rows = []
                    for table in tables:
                        cleaned_table = [[cell if cell is not None else "" for cell in row] for row in table]
                        page_rows.extend(cleaned_table)

                    extracted_content[page_label] = page_rows
                    
        except Exception as e:
            print(f"Error during extraction: {e}")
            raise

        return extracted_content