# Information Extraction Dataset Generator

This repository contains a pipeline for generating synthetic training data for fine-tuning models on information extraction tasks. The pipeline creates a hierarchical dataset starting from high-level categories down to specific extraction scenarios, complete with realistic contexts and extracted information.

## Overview

The pipeline generates training data through multiple stages:
1. Sub-category generation from main categories
2. Specific subject generation from sub-categories
3. Context generation for each subject
4. Information extraction from generated contexts
5. Validation generation for extracted information
6. Validation filtering for quality standards
7. Data formatting for fine-tuning

## Project Structure
.
├── README.md
├── run_pipeline.py              # Main pipeline orchestrator
├── sub_category_generator.py    # Generates sub-categories from main categories
├── subject_generator.py         # Generates specific subjects for extraction
├── context_generator.py         # Creates realistic contexts
├── extracted_data_generator.py  # Generates extracted information
├── validate_extractions.py      # Validates extractions
├── filter_validations.py        # Filters valid entries
├── data_formatter.py           # Formats data for fine-tuning
├── Fine_Tuning.ipynb           # Fine-tuning notebook
└── datasets/
    ├── categories.jsonl         # Input main categories
    ├── sub_categories.jsonl     # Generated sub-categories
    ├── subjects.jsonl          # Generated subjects
    ├── contexts.jsonl          # Generated contexts
    ├── extractions.jsonl       # Generated extractions
    ├── validations.jsonl        # Validation results
    ├── filtered_validations.jsonl # Filtered validations
    └── conversation_format_dataset.json # Final formatted dataset

## Prerequisites

- Python 3.8+
- `dria` library for data synthesis

## Installation

pip install dria pydantic

## Usage

1. Prepare your initial categories in datasets/categories.jsonl with the format:
   {"main_category": "Your Category Name"}

2. Run the complete pipeline:
   python run_pipeline.py

## Pipeline Stages

### 1. Sub-category Generation
- Input: Main categories from categories.jsonl
- Output: sub_categories.jsonl
- Generates 3 specific sub-categories for each main category

### 2. Subject Generation
- Input: Sub-categories from sub_categories.jsonl
- Output: subjects.jsonl
- Creates specific subjects with extraction task descriptions

### 3. Context Generation
- Input: Subjects from subjects.jsonl
- Output: contexts.jsonl
- Generates realistic contexts (500-1000 words) containing information to be extracted

### 4. Information Extraction
- Input: Contexts from contexts.jsonl
- Output: extractions.jsonl
- Generates structured extracted information from the contexts

### 5. Validation Generation
- Input: extractions.jsonl
- Output: validations.jsonl
- Validates the quality and completeness of extracted information
- Checks for accuracy, format validity, and missing fields

### 6. Validation Filtering
- Input: validations.jsonl
- Output: filtered_validations.jsonl
- Filters out entries that don't meet quality standards
- Only keeps entries with complete, accurate, and properly formatted data

### 7. Data Formatting
- Input: filtered_validations.jsonl
- Output: conversation_format_dataset.json
- Formats the data into conversation format suitable for fine-tuning

## Fine-tuning

The repository includes a Jupyter notebook (`Fine_Tuning.ipynb`) for fine-tuning a Llama 3.2 1B model on the generated dataset. 

### Prerequisites for Fine-tuning
- Unsloth library (`pip install unsloth`)
- Ollama for running the base model

### Fine-tuning Process
1. Install required dependencies
2. Load the conversation format dataset
3. Configure training parameters
4. Fine-tune the model
5. Compare base model vs fine-tuned model performance

### Running the Notebook
```bash
jupyter notebook Fine_Tuning.ipynb
```

Or you can run the notebook from [here](https://colab.research.google.com/drive/1OnGmdurzwj-5COcobPx5no2YA2_O7iBA?usp=sharing)

## Output Format

The final dataset in fine_tuning_dataset.json follows this conversation format:

[
  {
    "role": "system",
    "content": "You are an AI assistant that helps with information extraction tasks."
  },
  {
    "role": "user",
    "content": "Your goal is [description]\nHere is the context to extract information from: [context]"
  },
  {
    "role": "assistant",
    "content": "Here is the extracted information:\n<extracted_info>\n[extracted_info]\n</extracted_info>"
  }
]

## Error Handling

The pipeline includes:
- File existence checks
- Size validation
- Error logging
- Continuation capability (can skip completed stages)
- Validation of extraction quality
- Filtering of low-quality entries

## Contributing

Feel free to submit issues and enhancement requests!

## Examples

### Input Category Example (categories.jsonl)
```json
{"main_category": "Real Estate"}
{"main_category": "Healthcare"}
{"main_category": "Finance"}
```

### Generated Sub-categories Example (sub_categories.jsonl)
```json
{
  "main_category": "Real Estate",
  "sub_category_1": "Digital Home Buying",
  "description_1": "This sub-category covers digital platforms where homes are sold to clients through virtual interactions...",
  "sub_category_2": "Affordable Housing Development",
  "description_2": "This sub-category includes residential buildings designed to provide homes for low-income families...",
  "sub_category_3": "Real Estate Analytics",
  "description_3": "This sub-category focuses on the use of data-driven tools and models to appraise property value..."
}
```

### Generated Subject Example (subjects.jsonl)
```json
{
  "subject": "User Engagement Metrics in Digital Home Buying Platforms",
  "description": "Extract key metrics that reflect user engagement with digital home buying platforms, including average time spent on virtual tours, percentage of leads converting to signed contracts, and customer satisfaction ratings post-purchase..."
}
```

### Generated Context Example (contexts.jsonl)
```json
{
  "subject": "User Engagement Metrics in Digital Home Buying Platforms",
  "description": "Extract key metrics...",
  "context": "In a recent analysis of digital home buying trends, Sarah Martinez, Head of Digital Operations at HomeConnect, shared insights from their Q3 performance review. 'Our virtual tour engagement has seen remarkable growth,' she noted, reviewing the latest metrics..."
}
```

### Generated Extraction Example (extractions.jsonl)
```json
{
  "subject": "User Engagement Metrics in Digital Home Buying Platforms",
  "description": "Extract key metrics...",
  "context": "In a recent analysis...",
  "extracted_info": {
    "virtual_tour_engagement": {
      "average_time_spent": "12 minutes",
      "completion_rate": "78%"
    },
    "lead_conversion": {
      "virtual_tour_to_contract": "15%",
      "overall_satisfaction": "4.2/5"
    }
  }
}
```

### Final Output Example (fine_tuning_dataset.json)
```json
[
  {
    "role": "system",
    "content": "You are an AI assistant that helps with information extraction tasks."
  },
  {
    "role": "user",
    "content": "Your goal is to extract key metrics that reflect user engagement with digital home buying platforms...\nHere is the context to extract information from: In a recent analysis of digital home buying trends..."
  },
  {
    "role": "assistant",
    "content": "Here is the extracted information:\n<extracted_info>\n{\"virtual_tour_engagement\": {\"average_time_spent\": \"12 minutes\", \"completion_rate\": \"78%\"}, \"lead_conversion\": {\"virtual_tour_to_contract\": \"15%\", \"overall_satisfaction\": \"4.2/5\"}}\n</extracted_info>"
  }
]
```


