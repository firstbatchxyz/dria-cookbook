import json

def should_keep_entry(validation_result):
    # Skip empty validation results
    if not validation_result:
        return False
        
    try:
        # Parse the validation_result string into a dictionary
        validation = json.loads(validation_result.strip())
        return (validation["is_accurate"] == True and 
                validation["format_valid"] == True and
                len(validation["missing_fields"]) == 0 and
                len(validation["incorrect_fields"]) == 0)
    except json.JSONDecodeError:
        # If we can't parse the JSON, skip this entry
        return False

def filter_validations(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            entry = json.loads(line)
            
            # Skip entries that don't have validation_result
            if "validation_result" not in entry:
                continue
                
            if should_keep_entry(entry["validation_result"]):
                outfile.write(line)

# Run the filter
filter_validations('datasets/validations.jsonl', 'datasets/filtered_validations.jsonl') 