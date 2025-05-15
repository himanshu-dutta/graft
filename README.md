# GRAFT: Graph-based Framework for Document-Level Machine Translation

This repository contains the official codebase for the GRAFT research paper. GRAFT is a graph-based framework designed for document-level machine translation (MT), leveraging discourse-level and memory-based agents for improved contextual translations. The code is designed for modularity and extensibility, enabling experimentation with various agents and datasets.

## Features

* **Document-level MT agents:** Includes discourse, memory, edge, and translation agents.
* **Dataset support:** Handles multilingual datasets, including IWSLT2017, WMT2022, and Guofeng.
* **Evaluation:** Provides utilities for automated evaluation of translation quality.
* **Experiment scripts:** Preconfigured scripts to reproduce the results presented in the paper.

## Datasets

The repository supports multiple datasets for document-level MT across various language pairs:

* **IWSLT2017:** Available for language pairs such as English-German (en-de), English-French (en-fr), English-Japanese (en-ja), and English-Chinese (en-zh).
* **WMT2022:** Contains news and social media data for English-Chinese (en-zh).
* **Guofeng:** Features English-Chinese literary translations.
* **MZPRT:** Includes fiction and question-answer datasets for English-Chinese.

Datasets should be placed in the `data/document_level` directory. For example:

```
├── data
│   └── document_level
│       ├── en-de
│       │   └── iwslt2017
│       ├── en-zh
│       │   └── wmt2022
```

## Installation

1. Clone the repository:
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running Experiments

Preconfigured scripts for experiments are located in the `experiments` directory:

* **Book translation:** Evaluates GRAFT on long-form literary translations.
* **Discourse agent analysis:** Measures the impact of discourse agents.
* **Edge agent analysis:** Analyzes edge agents in translation graphs.
* **Memory agent analysis:** Studies the effects of memory agents.
* **LLM-based experiments:** Integrates large language models into the framework.

Example:

```bash
bash experiments/experiments_book_translation.sh
```

## Usage

### Translation

Run the `main.py` script for translating documents:

```bash
python src/main.py -h
```

### Evaluation

Evaluate translations using the `evaluation.py` script:

```bash
bash scripts/evaluation.sh
```

### Server

Launch the server for interactive translation:

```bash
bash scripts/run_server.sh
```

## Code Overview

* **src/agents:** Implements the core agents for document-level translation.
* **src/data.py:** Contains utilities for loading, processing, and saving data.
* **src/prompts:** Stores prompt templates for agents, organized by language pairs.
* **src/evaluation.py:** Scripts for evaluating the quality of translations.
* **src/workflow\.py:** Defines the overall workflow for translation tasks.

## Reproducing Results

1. Download the datasets and place them in the appropriate directories.
2. Run the desired experiment script from the `experiments` folder.
3. Use the evaluation scripts to calculate metrics such as BLEU and METEOR.
