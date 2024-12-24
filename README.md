# Dria RAG Evaluation Cookbook

This repository contains a comprehensive guide and set of tools for evaluating AI agents using Dria's QA pipeline. The notebook provided in this repository demonstrates how to generate an evaluation set for your AI agents and assess their performance using various tools and datasets.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
  - [Step 1: Initialization](#step-1-initialization)
  - [Step 2: Setting Environmental Variables](#step-2-setting-environmental-variables)
  - [Step 3: Scraping Content](#step-3-scraping-content)
  - [Step 4: Combining Data](#step-4-combining-data)
  - [Step 5: Evaluation](#step-5-evaluation)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Importance of Evaluation

Evaluating Retrieval-Augmented Generation (RAG) agents is crucial for ensuring their effectiveness and reliability across diverse datasets and scenarios. By testing these agents with detailed questions and varied personas, you can better understand their strengths and weaknesses. This process helps in refining the agents to perform optimally in real-world applications.

Moreover, evaluating different models with various RAG methodologies allows for a comprehensive comparison of their capabilities. It highlights the nuances in performance and adaptability, guiding the selection of the most suitable model for specific tasks. This evaluation is essential for advancing AI technologies and ensuring they meet the desired standards of accuracy and efficiency.


## Introduction

This notebook shows how to generate an evaluation set for your AI agents by using [Dria](https://docs.dria.co/). In the end, you can evaluate these agents with [promptfoo](https://www.promptfoo.dev/) and see the evaluation and assessment results.

## Installation

To get started, clone this repository and install the necessary dependencies. We recommend using a Python virtual environment to manage dependencies.

## Usage

### Step 1: Initialization

Begin by installing the necessary dependencies. This can be done by running the provided code block in the notebook. It is recommended to use your local machine instead of Google Colab due to potential incompatibilities.

### Step 2: Setting Environmental Variables

To run and use external applications in this notebook, you need to have API keys from various providers such as Firecrawl, Jina Reader, Upstash, Cohere, and OpenAI. Create an `.env` file with the required API keys.

### Step 3: Scraping Content

Utilize the command-line interface provided in the notebook to scrape content from web domains. You can choose to scrape an entire domain or a single URL.

### Step 4: Combining Data

The notebook demonstrates how to combine scraped content with personas to create a comprehensive dataset for evaluation.

### Step 5: Evaluation

Finally, use the combined data to evaluate your AI agents. The notebook provides guidance on how to perform this evaluation using the Dria QA pipeline and other tools.

## Dependencies

The project requires several Python packages, including but not limited to:
- requests
- openai
- pandas
- nltk
- matplotlib
- firecrawl
- upstash_vector
- cohere
- python-dotenv

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.


