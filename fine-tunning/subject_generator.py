import asyncio
import json
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field

# Define output schema
class SubjectOutput(BaseModel):
    subject: str = Field(..., description="Subject name for the extraction task")
    description: str = Field(..., description="Description of what to extract")

# Define the prompt template
PROMPT_TEMPLATE = """
For the following sub-category of {{main_category}}:
{{sub_category}}

Description: {{description}}

Generate a specific subject for information extraction. The subject should:
1. Be focused and specific
2. Clearly define what information needs to be extracted
3. Be practical and business-relevant
4. Include clear extraction guidelines

Format your response EXACTLY as:
Subject: [specific subject name]
Description: [description of the information extraction task, the expected values to be extracted]
"""

# Create dataset
dataset = DriaDataset(
    name="subjects",
    description="A dataset of subjects for information extraction",
    schema=SubjectOutput
).reset()

# Read sub-categories from JSONL file
instructions = []
with open('datasets/sub_categories.jsonl', 'r') as file:
    for line in file:
        item = json.loads(line)
        # Check if main_category exists
        if "main_category" not in item or not item["main_category"].strip():
            continue
            
        # Process each sub-category (1-3)
        for i in range(1, 4):
            sub_cat_key = f"sub_category_{i}"
            desc_key = f"description_{i}"
            
            if all(key in item and item[key].strip() for key in [sub_cat_key, desc_key]):
                instructions.append({
                    "main_category": item["main_category"],
                    "sub_category": item[sub_cat_key],
                    "description": item[desc_key]
                })

# Create prompt
prompter = Prompt(prompt=PROMPT_TEMPLATE, schema=SubjectOutput)

generator = DatasetGenerator(dataset=dataset)

# Run generation
asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=prompter,
        models=[Model.GPT4O_MINI,Model.GPT4O,Model.ANTHROPIC_SONNET_3_5_OR]
    )
)

# Export results to JSON file
dataset.to_jsonl("datasets/subjects.jsonl")

# Print confirmation
print("Results have been exported to datasets/subjects.jsonl")