import asyncio
import subprocess
import os
import time
from pathlib import Path
import shutil
import json

class Pipeline:
    def __init__(self):
        self.initial_data = "datasets/categories.jsonl"  # Simplified to just the path
        
        self.scripts = [
            {
                "name": "Sub-category Generation",
                "file": "sub_category_generator.py",
                "input": "datasets/categories.jsonl",
                "output": "datasets/sub_categories.jsonl",
                "required": True
            },
            {
                "name": "Subject Generation",
                "file": "subject_generator.py",
                "input": "datasets/sub_categories.jsonl",
                "output": "datasets/subjects.jsonl",
                "required": True
            },
            {
                "name": "Context Generation",
                "file": "context_generator.py",
                "input": "datasets/subjects.jsonl",
                "output": "datasets/contexts.jsonl",
                "required": True
            },
            {
                "name": "Extraction Generation",
                "file": "extracted_data_generator.py",
                "input": "datasets/contexts.jsonl",
                "output": "datasets/extractions.jsonl",
                "required": True
            },
            {
                "name": "Validation Generation",
                "file": "validate_extractions.py",
                "input": "datasets/extractions.jsonl",
                "output": "datasets/validations.jsonl",
                "required": True
            },
            {
                "name": "Filter Validations",
                "file": "filter_validations.py",
                "input": "datasets/validations.jsonl",
                "output": "datasets/filtered_validations.jsonl",
                "required": True
            }
        ]
        
        self.data_prep = {
            "name": "Data Conversion",
            "file": "data_formatter.py",
            "input": "datasets/filtered_validations.jsonl",
            "output": "datasets/conversation_format_dataset.json"
        }
        

    def check_file_exists(self, filepath):
        path = Path(filepath)
        exists = path.exists()
        if exists:
            size = path.stat().st_size
            print(f"File {filepath} exists with size: {size} bytes")
        else:
            print(f"File {filepath} does not exist")
        return exists and size > 0

    def check_initial_data(self):
        if not self.check_file_exists(self.initial_data):
            print(f"\n❌ Initial data file not found: {self.initial_data}")
            return False
        print(f"\n✅ Initial data file verified: {self.initial_data}")
        return True

    def run_script(self, script_info):
        print(f"\n{'='*50}")
        print(f"Running: {script_info['name']}")
        print(f"{'='*50}")
        
        try:
            # Run the script
            result = subprocess.run(['python', script_info['file']], check=True)
            
            # Wait a bit and check if the output file was created
            time.sleep(2)
            if 'output' in script_info and not self.check_file_exists(script_info['output']):
                raise Exception(f"Output file {script_info['output']} was not created or is empty")
            
            print(f"\n✅ {script_info['name']} completed successfully")
            return True
            
        except Exception as e:
            print(f"\n❌ Error in {script_info['name']}: {str(e)}")
            return False

    def run_pipeline(self):
        print("\nStarting Data Generation Pipeline")
        print("================================")
        
        # First, verify the initial data file exists
        if not self.check_initial_data():
            return False
        
        # Run each script in sequence
        for script in self.scripts:
            # Skip if file exists and not required
            if not script['required'] and self.check_file_exists(script['output']):
                print(f"\nSkipping {script['name']} - output file already exists")
                continue
                
            # Check if previous output exists if needed
            if script != self.scripts[0]:  # Not the first script
                prev_script = self.scripts[self.scripts.index(script) - 1]
                if not self.check_file_exists(prev_script['output']):
                    print(f"\n❌ Required input file {prev_script['output']} not found")
                    return False
            
            # Run the script
            if not self.run_script(script):
                return False
                
            # Wait between scripts
            time.sleep(5)
        
        # Run the data conversion script
        if self.check_file_exists(self.data_prep['input']):
            if self.run_script(self.data_prep):
                print("\n✅ Pipeline completed successfully!")
                return True
        else:
            print(f"\n❌ Required input file {self.data_prep['input']} not found")
        
        return False

if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run_pipeline() 