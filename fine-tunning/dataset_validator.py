import asyncio
import json
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field
from typing import List

# Define simplified output schema for scoring
class EntryScore(BaseModel):
    subject: str = Field(..., description="Original subject")
    context: str = Field(..., description="Original context")
    extracted_info: str = Field(..., description="Extracted information")
    quality_score: float = Field(..., ge=0, le=1, description="Overall quality score (0-1)")

# Define simplified prompt template
PROMPT_TEMPLATE = """
You are an expert at evaluating information extraction results. Evaluate the following extraction:

Subject: {{subject}}
Context: {{context}}
Extracted Information: {{extracted_info}}

Provide:
1. A single quality score (0-1) based on:
   - JSON formatting
   - Data completeness
   - Extraction accuracy
   - Relevance to subject
   
Keep your response focused and concise.
"""

# Create dataset
dataset = DriaDataset(
    name="validated_extractions",
    description="Validated information extraction results",
    schema=EntryScore
).reset()

# Read extractions from JSONL file
instructions = []
with open('datasets/extractions.jsonl', 'r') as f:
    for line in f:
        if line.strip():  # Skip empty lines
            extraction = json.loads(line)
            if extraction["subject"] and extraction["context"]:  # Skip empty entries
                instructions.append({
                    "subject": extraction["subject"],
                    "context": extraction["context"],
                    "extracted_info": extraction["extracted_info"]
                })

print(f"Loaded {len(instructions)} extractions for processing")

# Create prompt and generator
prompter = Prompt(prompt=PROMPT_TEMPLATE, schema=EntryScore)
generator = DatasetGenerator(dataset=dataset)

# Run validation
asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=prompter,
        models=[Model.GPT4O_MINI, Model.GPT4O, Model.ANTHROPIC_SONNET_3_5_OR]
    )
)

# Export results
dataset.to_jsonl("datasets/validated_extractions_0.jsonl")

# Print confirmation
print("Results have been exported to datasets/validated_extractions_0.jsonl") 