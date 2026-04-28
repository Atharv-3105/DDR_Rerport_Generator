from collections import defaultdict
import re 

class MergeEngine:
    def __init__(self, inspection_obs, thermal_obs):
        self.inspection_obs = inspection_obs
        self.thermal_obs = thermal_obs
        
    
    #======Area Normalization Function============
    def normalize_area(self, area):
        if not area:
            return "Unknown"
        
        area = area.lower()
        
        #Convert Area Names into Normalized Area Names
        if "hall" in area:
            return "Hall"
        if "bedroom" in area:
            return "Bedroom"
        if "kitchen" in area:
            return "Kitchen"
        if "bathroom" in area:
            return "Bathroom"
        if "parking" in area:
            return "Parking"
        if "external" in area:
            return "External Wall"
        
        if "flat no" in area:
            return "Unknown"
        
        return area.title()
    
    #========Issue Normalization Function==========
    def normalize_issue(self, issue):
        if not issue:
            return None 
        
        issue = issue.lower()
        
        if "damp" in issue:
            return "Dampness"
        if "crack" in issue:
            return "Cracks"
        if "leak" in issue:
            return "Leakage"
        if "gap" in issue:
            return "Tile Gaps"
        if "hollow" in issue:
            return "Tile Hollowness"
        if "plumbing" in issue:
            return "Plumbing issue"
        if "seepage" in issue:
            return "Seepage"
        
        return issue.title() 
    
    def clean_observations(self, observations):
        cleaned = []
        
        for obs in observations:
            raw_issue = obs.get("issue_type", "")
            
            #Remove Garbage/UseLess entries
            if not raw_issue or raw_issue.lower() in ["negative side description", "positive side description"]:
                continue
            
            area = self.normalize_area(obs.get("area", ""))
            issue = self.normalize_issue(raw_issue)
            
            if not issue:
                continue
            
            cleaned.append({
                "area" : area,
                "issue_type": issue,
                "description": obs.get("description", ""),
                "location_detail": obs.get("location_detail", ""),
                "source": obs.get("source", "inspection"),
                "page_number": obs.get("evidence", {}).get("page_number", "")
            })
            
        return cleaned
    
    
    def deduplicate(self, observations):
        seen = set()
        unique = []
        
        for obs in observations:
            #Consider AREA,ISSUE as main identifier of Unique Observations
            key = (obs["area"], obs["issue_type"])
            
            if key not in seen:
                seen.add(key)
                unique.append(obs)
        
        return unique
    
    
    #Function to group multiple observations together on the basis of AREA
    def group_by_area(self, observations):
        area_map = defaultdict(list)
        
        for obs in observations:
            area_map[obs["area"]].append(obs)
            
        return dict(area_map)
    
    def extract_thermal_signals(self):
        signals = []
        
        for obs in self.thermal_obs:
            
            text = obs.get("evidence", {}).get("text_excerpt", "")
            
            #Extraction temperature value from thermal observation
            temps = re.findall(r"\d+\.?\d*", text)
            
            if len(temps) >= 2:
                try:
                    high = float(temps[0])
                    low = float(temps[1])
                    
                    diff = high - low
                    
                    if diff >= 4:
                        signals.append({
                            "type": "Thermal Anomaly",
                            "description": f"Temperature variation detected (~{diff:.1f}°C), possible moisture presence"
                        })
                except:
                    continue
           
            return signals
        
    
    def assign_serverity(self, grouped_data):
        severity_map = {}
        
        for area, issues in grouped_data.items():
            score = 0
            
            for issue in issues:
                if issue["issue_type"] in ["Leakage", "Seepage"]:
                    score += 4
                elif issue["issue_type"] in ["Dampness"]:
                    score += 3
                elif issue["issue_type"] in ["Plumbing Issue"]:
                    score += 3
                elif issue["issue_type"] in ["Tile Gaps", "Tile Hollowness"]:
                    score += 2
                
            
            if score >= 6:
                severity = "High"
            elif score >= 3:
                severity = "Medium"
            else:
                severity = "Low"
                
            severity_map[area] = severity
            
        return severity_map
        
        
    def merge(self):
        #Step1: Clean the  Inspection Data
        cleaned = self.clean_observations(self.inspection_obs)
        
        #Step2: Deduplicate
        unique = self.deduplicate(cleaned)
        
        #Step3: Group By Area
        grouped = self.group_by_area(unique)
        
        #Step3.1: Remove Unkown Area
        grouped = {k:v for k, v in grouped.items() if k != "Unknown"}
        
        #Step4: Extract Thermal Signals
        thermal_signals = self.extract_thermal_signals()
        
        #Step5: Get Severity Map of Areas
        print("getting severity_map")
        severity_map = self.assign_serverity(grouped)
        print(severity_map)
        return {
            "area_summary": grouped,
            "thermal_signals": thermal_signals,
            "severity": severity_map
        }