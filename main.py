import os
import sys
from pdf_processor.extractors import PlumberGridExtractor
from pdf_processor.exporters import PandasMultiSheetExporter
from pdf_processor.pipeline import PDFTablePipeline

def main():
    # Configuration
    input_pdf = "groundwater_report.pdf"
    output_xlsx = "groundwater_report.xlsx"

    # Command line argument support (Optional)
    if len(sys.argv) > 1:
        input_pdf = sys.argv[1]
        output_xlsx = input_pdf.replace(".pdf", ".xlsx")

    if not os.path.exists(input_pdf):
        print(f"Error: The file '{input_pdf}' was not found.")
        print("Please ensure the file exists or pass the filename as an argument.")
        return

    # Initialize the components
    # We use the GridExtractor for table-heavy PDFs
    extractor = PlumberGridExtractor()
    
    # We use the MultiSheetExporter to map Pages -> Sheets
    exporter = PandasMultiSheetExporter()

    # Run the pipeline
    pipeline = PDFTablePipeline(extractor, exporter)
    pipeline.run(input_pdf, output_xlsx)

if __name__ == "__main__":
    main()