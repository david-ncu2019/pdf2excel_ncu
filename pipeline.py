from interfaces import IExtractor, IExporter

class PDFTablePipeline:
    def __init__(self, extractor: IExtractor, exporter: IExporter):
        self.extractor = extractor
        self.exporter = exporter

    def run(self, input_path: str, output_path: str):
        print(f"--- Starting Pipeline for {input_path} ---")
        
        # 1. Extraction Phase
        data_dict = self.extractor.extract(input_path)
        
        if not data_dict:
            print("Pipeline aborted: No data extracted.")
            return

        print(f"Extraction successful. Found content for {len(data_dict)} pages.")

        # 2. Export Phase
        self.exporter.save(data_dict, output_path)
        
        print("--- Pipeline Completed ---")