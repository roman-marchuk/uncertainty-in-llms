# Uncertainty in LLMs
This repository sets out on a task of understanding the current state of quantifying and interpreting uncertainty in large language models.

Uncerainty Quantification (UQ) is important for high-fields like finance and medicine to understand when to trust the model and when to bring the human professional in the loop.

## Project Setup
### Survey of SotA UQ Methods

First, we will begin by surveying the current state-of-the-art UQ methods.
Modern approaches for uncertainty quantification for LLMs can be divided into two distinct categories:
white-box methods and black-box methods. 

White-box methods utilize their access to the model's
internal information, such as token probabilities or weights, while black-box methods rely entirely on the output
of the model. Black-box methods are ideal for models that are closed source, but this often requires
extensive amounts of sampling.

- **Model Selection:**
    - In order to get interpretable results, we will use the same models across all methods. This project is being run on local Apple Silicon hardware with 48GB of Unified Memory available. This main constraint will dictate what models are used throughout the project. We start with a diverse selection of different models of different architecutres and sizes. The current contenders are:
    1. openai/gpt-oss-20b
    2. Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
    3. mistralai/Mistral-Small-3.2-24B-Instruct-2506
- Data Selection
