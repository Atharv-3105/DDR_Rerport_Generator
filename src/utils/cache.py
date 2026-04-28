import json 
import os 

def save_cache(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent = 2)
        
def load_cache(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None 