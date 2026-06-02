import subprocess
import json
import os
from datetime import datetime

def run_scan(target_path="sample_code"):
    """Run Bandit scan and save results as JSON"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"reports/scan_{timestamp}.json"
    
    print(f"🔍 Scanning: {target_path}")
    
    command = [
        "bandit",
        "-r", target_path,
        "-f", "json",
        "-o", output_file
    ]
    
    subprocess.run(command, capture_output=True)
    
    print(f"✅ Scan complete. Report saved: {output_file}")
    return output_file

def load_latest_report():
    """Load the most recent scan report"""
    reports = sorted(os.listdir("reports"))
    
    if not reports:
        print("⚠️ No reports found. Run a scan first.")
        return None
    
    latest = f"reports/{reports[-1]}"
    
    with open(latest, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    run_scan()