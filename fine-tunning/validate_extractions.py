import asyncio
import json
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field

# Define output schema
class ValidationOutput(BaseModel):
    subject: str = Field(..., description="Original subject name")
    description: str = Field(..., description="Original extraction task description")
    context: str = Field(..., description="Original context")
    extracted_info: str = Field(..., description="Original extracted information")
    validation_result: str = Field(..., description="Validation analysis and feedback")

# Define the prompt template
PROMPT_TEMPLATE = """
Validate the following extraction result:

Subject: {{subject}}
Description: {{description}}
Context: {{context}}
Extracted Information: {{extracted_info}}

Your task is to validate the extraction by:
1. Checking if the extracted information matches the requirements in the description
2. Verifying if all required information was extracted from the context
3. Validating the JSON format and structure
4. Identifying any missing or incorrect information

Provide your validation analysis in a JSON format with the following structure:
{
    "is_complete": true/false,
    "is_accurate": true/false,
    "format_valid": true/false,
    "missing_fields": [],
    "incorrect_fields": [],
}
"""

# Create dataset
dataset = DriaDataset(
    name="extraction_validations",
    description="Validation results for extracted information",
    schema=ValidationOutput
).reset()

# Read extractions from JSONL file
instructions = []
with open('datasets/extractions.jsonl', 'r') as file:
    for line in file:
        if line.strip():  # Skip empty lines
            extraction = json.loads(line)
            if all(key in extraction for key in ["subject", "description", "context", "extracted_info"]):
                instructions.append(extraction)

# Create prompt
prompter = Prompt(prompt=PROMPT_TEMPLATE, schema=ValidationOutput)

generator = DatasetGenerator(dataset=dataset)

# Run generation
asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=prompter,
        models=[Model.GPT4O,Model.GPT4O_MINI,Model.ANTHROPIC_SONNET_3_5_OR]
    )
)

# Export results to JSONL file
dataset.to_jsonl("datasets/validations.jsonl")

# Print confirmation
print("Results have been exported to datasets/validations.jsonl") 