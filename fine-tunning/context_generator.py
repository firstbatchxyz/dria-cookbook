import asyncio
import json
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field

# Define output schema
class ContextOutput(BaseModel):
    subject: str = Field(..., description="Original subject name")
    description: str = Field(..., description="Original extraction task description")
    context: str = Field(..., description="Generated context containing information")

# Define the prompt template
PROMPT_TEMPLATE = """

Your task is to generate a realistic context that will be used for information extraction tasks.
Generate a realistic context that contains information related to:
Subject: {{subject}}
Extraction Task: {{description}}

Requirements:
1. Make it realistic and detailed
2. Do not include ALL information needed for the extraction task, but include most of it
3. Add some irrelevant information to make it more natural
4. Length should be 500-1000 words
5. Format appropriately for the type of content
6. Shape the context as a story, a conversation between two people, a financial report, a blog post, etc. based on the subject and extraction task
"""

# Create dataset
dataset = DriaDataset(
    name="contexts",
    description="A dataset of realistic contexts for information extraction",
    schema=ContextOutput
).reset()

# Read subjects from JSONL file
instructions = []
with open('datasets/subjects.jsonl', 'r') as file:
    for line in file:
        subject_data = json.loads(line)
        if all(key in subject_data and subject_data[key].strip() for key in ["subject", "description"]):
            instructions.append({
                "subject": subject_data["subject"],
                "description": subject_data["description"]
            })

# Create prompt
prompter = Prompt(prompt=PROMPT_TEMPLATE, schema=ContextOutput)

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
dataset.to_jsonl("datasets/contexts.jsonl")

# Print confirmation
print("Results have been exported to datasets/contexts.jsonl") 