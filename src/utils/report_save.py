def save_report(report, path = "data/output/reports/final_ddr.md"):
    import os 
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)
        
        