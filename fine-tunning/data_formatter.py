import json
import os
from pathlib import Path

def create_conversation(data):
    """Convert a single data entry into a conversation format"""
    return [
        {
            "role": "system",
            "content": "You are an AI assistant that helps with information extraction tasks."
        },
        {
            "role": "user",
            "content": f"{data['description']}\n Here is the context to extract information from: {data['context']}"
        },
        {
            "role": "assistant",
            "content": f"<{data['extracted_info']}"
        }
    ]

def convert_data():
    """Convert the dataset into fine-tuning format"""
    try:
        # Read the extractions data line by line (JSONL format)
        data_array = []
        with open('datasets/filtered_validations.jsonl', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    data_array.append(json.loads(line))
        
        # Convert to fine-tuning format
        conversations = []
        processed_count = 0
        
        for entry in data_array:
            try:
                # Skip empty or invalid entries
                if not isinstance(entry, dict):
                    continue
                
                # Check if all required fields exist
                if all(field in entry for field in ["subject", "description", "context", "extracted_info"]):
                    conversation = create_conversation(entry)
                    conversations.append(conversation)
                    processed_count += 1
                
            except Exception as e:
                print(f"Error processing entry: {str(e)}")
        
        # Save the conversations
        with open('datasets/conversation_format_dataset.json', 'w', encoding='utf-8') as out:
            json.dump(conversations, out, indent=2)
        
        print(f"\nSuccessfully processed and saved {processed_count} conversations to datasets/conversation_format_dataset.json")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        # Create datasets directory if it doesn't exist
        Path("datasets").mkdir(parents=True, exist_ok=True)
        
        # Define input and output paths
        input_file = "datasets/filtered_validations.jsonl"
        output_file = "datasets/conversation_format_dataset.json"  # Changed to match pipeline
        
        print(f"Starting conversion from {input_file} to {output_file}")
        convert_data()
        
    except Exception as e:
        print(f"Failed to convert data: {e}")
        raise