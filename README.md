# Individual Assignment 1: Risks and Mitigations

## Overview

This repository contains an LLM-assisted stakeholder-centered hazard analysis for an ML-enabled dashcam system designed to help locate missing children.

The workflow uses LLM assistance to:

1. identify direct and indirect stakeholders,
2. identify stakeholder goals, losses, and requirements,
3. analyze requirements to generate environmental assumptions and software specifications,
4. generate a comprehensive analysis report.

Human review is performed between stages so that generated results can be corrected, filtered, or curated before continuing.

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Graphviz

On macOS with Homebrew:

```bash
brew install graphviz
```

### 4. Configure the OpenAI API key

Create a `.env` file in the repository root:

```text
OPENAI_API_KEY=your_api_key_here
```

The `.env` file is excluded from version control and should not be included in the submitted archive.

## Usage

Run the analysis scripts from the repository root.

### 1. Generate stakeholders

```bash
python code/generate_stakeholders.py
```

Output:

```text
data/stakeholders.json
```

Review and modify the generated stakeholder list before continuing if needed.

### 2. Generate goals, losses, and requirements

```bash
python code/analyze_hazards.py
```

Output:

```text
data/hazards.json
```

Review the generated requirements to ensure that requirements describe desired environmental outcomes rather than implementation details.

### 3. Generate assumptions and specifications

```bash
python code/analyze_requirements.py
```

Output:

```text
data/requirements.json
```

Review the generated assumptions and specifications before using them in the final reports.

### 4. Generate the comprehensive report

```bash
python code/generate_report.py
```

Output:

```text
analysis_results.md
```

### 5. Generate fault tree diagrams

```bash
python code/generate_fault_trees.py
```

Outputs:

```text
figures/fault_tree.png
figures/fault_tree_mitigated.png
```

## Human-in-the-Loop Review

The workflow intentionally includes manual review between stages.

Developers can:

- edit `data/stakeholders.json` before running hazard analysis,
- review `data/hazards.json` before generating assumptions and specifications,
- review `data/requirements.json` before generating the comprehensive report,
- manually select and refine the four findings in `key_results.md`.

This helps reduce shallow or irrelevant LLM-generated results and ensures that the final analysis reflects developer judgment.

## Repository Structure

```text
.
├── README.md
├── goals.md
├── analysis_results.md
├── key_results.md
├── fault_tree.md
├── requirements.txt
├── code/
│   ├── generate_stakeholders.py
│   ├── analyze_hazards.py
│   ├── analyze_requirements.py
│   ├── generate_report.py
│   └── generate_fault_trees.py
├── data/
│   ├── stakeholders.json
│   ├── hazards.json
│   └── requirements.json
└── figures/
    ├── fault_tree.png
    └── fault_tree_mitigated.png
```

## Deliverables

- `goals.md`: organizational, system, user, and model goals with measurements
- `analysis_results.md`: comprehensive stakeholder-centered risk analysis
- `key_results.md`: four curated important or surprising findings
- `fault_tree.md`: fault tree analysis and system-level mitigations
- `code/`: LLM-assisted automation scripts
- `data/`: intermediate generated results
- `figures/`: fault tree diagrams
