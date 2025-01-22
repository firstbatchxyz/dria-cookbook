import asyncio
import json
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field

# Define output schema
class ExtractionOutput(BaseModel):
    subject: str = Field(..., description="Original subject name")
    description: str = Field(..., description="Original extraction task description")
    context: str = Field(..., description="Context to extract from")
    extracted_info: str = Field(..., description="Extracted information in JSON format")

# Define the prompt template
PROMPT_TEMPLATE = """
Based on the following subject and task, extract the relevant information from the document and format it as a JSON object.

Subject: {{subject}}
Extraction Task: {{description}}

Document:
{{context}}

Format your response EXACTLY as:
Extracted_data: [data_label_1: data_value_1, data_label_2: data_value_2, ...]
If the information is not present in the document, write "null" for the corresponding data_label.
"""

# Create dataset
dataset = DriaDataset(
    name="extractions",
    description="A dataset of extracted structured information from documents",
    schema=ExtractionOutput
).reset()

# Read instructions from JSONL file
instructions = []
with open('datasets/contexts.jsonl', 'r') as file:
    for line in file:
        context_data = json.loads(line)
        if all(key in context_data and context_data[key].strip() for key in ["subject", "description", "context"]):
            instructions.append({
                "subject": context_data["subject"],
                "description": context_data["description"],
                "context": context_data["context"]
            })

print(f"Loaded {len(instructions)} contexts for processing")

# Create prompt and generator
prompter = Prompt(prompt=PROMPT_TEMPLATE, schema=ExtractionOutput)
generator = DatasetGenerator(dataset=dataset)

# Run generation
asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=prompter,
        models=[Model.GPT4O_MINI, Model.GPT4O, Model.ANTHROPIC_SONNET_3_5_OR]
    )
)

# Export results to JSONL file
dataset.to_jsonl("datasets/extractions.jsonl")

print("Results have been exported to datasets/extractions.jsonl")