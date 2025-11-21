import os
import sys

# Ensure the current directory is in the python path
# This fixes "ModuleNotFoundError" when running the script directly
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from extractor import PlumberGridExtractor
from exporter import PandasMultiSheetExporter
from pipeline import PDFTablePipeline

def main():
    # Configuration
    # You can change this to match your actual file name
    input_pdf = "groundwater_report.pdf"
    output_xlsx = "groundwater_report.xlsx"

    # Command line argument support
    if len(sys.argv) > 1:
        input_pdf = sys.argv[1]
        if input_pdf.lower().endswith('.pdf'):
            output_xlsx = input_pdf[:-4] + ".xlsx"

    if not os.path.exists(input_pdf):
        print(f"Error: The file '{input_pdf}' was not found.")
        print("Usage: python main.py <your_file.pdf>")
        return

    # Initialize the components
    extractor = PlumberGridExtractor()
    exporter = PandasMultiSheetExporter()

    # Run the pipeline
    pipeline = PDFTablePipeline(extractor, exporter)
    pipeline.run(input_pdf, output_xlsx)

if __name__ == "__main__":
    main()