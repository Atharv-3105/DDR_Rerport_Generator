import time 
from extractor.batching import batch_pages
from parser.pdf_parser import PDFParser
from utils.cache import save_cache, load_cache
from utils.filter import filter_pages
from extractor.llm_extractor import LLMExtractor
from merger.merge_engine import MergeEngine
from generator.ddr_generator import DDRGenerator
from utils.report_save import save_report

def run_pipeline():
    
    inspection_pdf = "data/input/inspection/Sample Report.pdf"
    thermal_pdf = "data/input/thermal/Thermal Images.pdf"
    
    #Output Image Directory
    inspection_img_dir = "data/output/images/inspection"
    thermal_img_dir = "data/output/images/thermal"
    
    #Parse PDFs
    inspection_parser = PDFParser(inspection_pdf, inspection_img_dir)
    thermal_parser = PDFParser(thermal_pdf, thermal_img_dir)
    
    inspection_data = inspection_parser.parse()
    thermal_data = thermal_parser.parse()
    
    print("Inspection Pages:", len(inspection_data["pages"]))
    print("Thermal Pages: ", len(thermal_data["pages"]))
    
    #Extract Observations from Inspection and Thermal Report
    inspection_obs = extract_all(inspection_data, "inspection", "data/output/cache/inspection.json")
    thermal_obs = extract_all(thermal_data, "thermal", "data/output/cache/thermal.json")
    
    print("Inspection observations", len(inspection_obs))
    print("Thermal observations:", len(thermal_obs))
    
    #Merge the extracted observations into single observation
    merge_engine = MergeEngine(inspection_obs, thermal_obs)
    merged_data = merge_engine.merge()
    
    print("Merged Areas:", merged_data["area_summary"].keys())
    print("Thermal Signals: ", merged_data["thermal_signals"])
    
    #Get the DDR Report
    ddr_generator = DDRGenerator(merged_data)
    final_report = ddr_generator.generate_report()
    
    print("\n\n=======Final DDR Report=======\n")
    print(final_report)
    
    #Save the Final DDR Report
    save_report(final_report)
    return merged_data

def extract_all(parsed_data, source_type, cache_path):
    #Get Cached results if available
    cached = load_cache(cache_path)
    if cached:
        print(f"Loaded cached {source_type} data")
        return cached
    
    extractor = LLMExtractor(source_type)
    pages = filter_pages(parsed_data["pages"])
    batches = list(batch_pages(pages, batch_size=3))
    
    all_observations = []

    #Iterate over batch of pages and send to LLM
    for i, batch in enumerate(batches):
        print(f"Processing batch {i + 1} / {len(batches)}")
        result = extractor.extract_from_page(batch)
        all_observations.extend(result.get("observations", []))
        
        #For rate-limit safety
        time.sleep(2)
    
    #Save result to Cache
    save_cache(all_observations, cache_path)
    
    return all_observations

if __name__ == "__main__":
    run_pipeline()
    