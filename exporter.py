import pandas as pd
from .interfaces import IExporter
from typing import List, Any, Dict

class PandasMultiSheetExporter(IExporter):
    """
    Exports data to Excel, creating a new sheet for every entry in the data dictionary.
    """
    def save(self, data: Dict[str, List[List[Any]]], output_path: str) -> None:
        if not data:
            print("Warning: No data provided to exporter.")
            return

        try:
            # The 'engine="openpyxl"' is required for writing .xlsx files
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, rows in data.items():
                    # Create DataFrame from the list of lists
                    df = pd.DataFrame(rows)
                    
                    # Sanitize sheet name (Excel limits: 31 chars, no special symbols)
                    # We take the first 31 chars to be safe.
                    safe_name = str(sheet_name)[:31]

                    # Cleaning: Replace newlines in data with spaces for readability
                    df = df.replace(r'\n', ' ', regex=True)

                    # Write to the specific sheet
                    # header=False and index=False because the PDF likely contains the headers in the first few rows
                    df.to_excel(writer, sheet_name=safe_name, header=False, index=False)
            
            print(f"Success: Data written to {output_path} ({len(data)} sheets).")

        except Exception as e:
            print(f"Error during export: {e}")
            raise