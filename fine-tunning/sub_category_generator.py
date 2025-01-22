import asyncio
import json
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field

# Define output schema
class SubCategoryOutput(BaseModel):
    main_category: str = Field(..., description="Main category name")
    sub_category_1: str = Field(..., description="Sub-category name")
    description_1: str = Field(..., description="Description of the sub-category")
    sub_category_2: str = Field(..., description="Sub-category name")
    description_2: str = Field(..., description="Description of the sub-category")
    sub_category_3: str = Field(..., description="Sub-category name")
    description_3: str = Field(..., description="Description of the sub-category")

# Define the prompt template
PROMPT_TEMPLATE = """
For the following main category:
{{category}}

Generate 3 specific sub-categories. Each sub-category should:
1. Be a specific subset of the main category
2. Have clear, defined boundaries
3. Be suitable for information extraction tasks
4. Have practical business applications

Return the response as a JSON with the following format:
Sub-Category_1: [name]
Description_1: [detailed description]

Sub-Category_2: [name]
Description_2: [detailed description]

Sub-Category_3: [name]
Description_3: [detailed description]

Generate exactly a unique sub-category, without any numbering or prefixes.
"""

# Create dataset
dataset = DriaDataset(
    name="sub_categories",
    description="A dataset of sub-categories for information extraction",
    schema=SubCategoryOutput
).reset()

# Read categories from JSONL file
categories = []
with open('datasets/categories.jsonl', 'r') as file:
    for line in file:
        category_data = json.loads(line)
        if 'main_category' in category_data and category_data['main_category'].strip():
            categories.append(category_data['main_category'])

print(f"Loaded {len(categories)} categories for processing")

# Create instructions for all categories
instructions = [{"category": category} for category in categories]

# Create prompt
prompter = Prompt(prompt=PROMPT_TEMPLATE, schema=SubCategoryOutput)

generator = DatasetGenerator(dataset=dataset)

# Run generation
asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=prompter,
        models=[Model.GPT4O_MINI,Model.GPT4O,Model.ANTHROPIC_SONNET_3_5_OR]
    )
)

# Export results to JSONL file
dataset.to_jsonl("datasets/sub_categories.jsonl")

# Print confirmation
print("Results have been exported to datasets/sub_categories.jsonl") 