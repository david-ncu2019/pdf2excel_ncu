import pdfplumber
import os
from interfaces import IExtractor
from typing import List, Any, Dict

class PlumberGridExtractor(IExtractor):
    """
    Extracts tables from PDFs using pdfplumber's grid detection strategies.
    Iterates through all pages in the PDF.
    """
    def __init__(self, settings: Dict[str, Any] = None):
        # Default settings tuned for the groundwater report grid structure
        self.settings = settings or {
            "vertical_strategy": "lines", 
            "horizontal_strategy": "lines",
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
                    
                    # Extract tables using the strict grid settings
                    tables = page.extract_tables(self.settings)
                    
                    if not tables:
                        print(f"Debug: No tables found on {page_label}. Skipping.")
                        continue

                    # Consolidate all tables on this page into one list
                    page_rows = []
                    for table in tables:
                        # Clean 'None' values which pdfplumber produces for empty cells
                        cleaned_table = [[cell if cell is not None else "" for cell in row] for row in table]
                        page_rows.extend(cleaned_table)
                        
                        # CRITICAL FIX: Removed the spacer row that corrupted data analysis
                        # page_rows.append([]) <-- DELETED

                    extracted_content[page_label] = page_rows
                    
        except Exception as e:
            print(f"Error during extraction: {e}")
            raise

        return extracted_content