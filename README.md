# emotion_classifier_repo
# Tweet Emotion Classification Project

This project is a submission for the [Name of your Course/Competition - e.g., AI/ML Analytics IE Kaggle Competition] on emotion classification of tweets. It includes a pip-installable Python package with a command-line interface (CLI) tool to predict the primary emotion expressed in a given text.

## Features

* Predicts emotions from text input (e.g., joy, sadness, anger, fear, love, surprise).
* Command-line interface for easy use.
* Utilizes a fine-tuned Transformer model (RoBERTa-base) for high accuracy.
* Model assets (weights, label encoder) are downloaded automatically on first run if not found locally.

## Project Structure

tweet_emotion_predictor_project/
├── emotion_classifier/            # Main package
│   ├── init.py
│   ├── cli.py                     # CLI logic
│   ├── predictor.py               # Prediction class
│   ├── model_loader.py            # Handles model/asset loading & downloading
│   ├── preprocess.py              # Text preprocessing
│   └── assets/                    # For downloaded assets (created at runtime)
├── setup.py                       # Package installation definition
├── README.md                      # This file
└── .gitignore                     # Specifies intentionally untracked files


## Installation

To install this package from its private GitHub repository, you will need a Personal Access Token (PAT) with `repo` (or at least read access to this repository) scope.

1.  **Clone the Repository (Optional - for development):**
    ```bash
    git clone [https://YOUR_PAT_TOKEN@github.com/YOUR_USERNAME/YOUR_PROJECT_REPO_NAME.git](https://YOUR_PAT_TOKEN@github.com/YOUR_USERNAME/YOUR_PROJECT_REPO_NAME.git)
    cd YOUR_PROJECT_REPO_NAME
    ```

2.  **Install via pip (Recommended for evaluation):**
    Create and activate a new virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    Then install the package:
    ```bash
    pip install git+[https://YOUR_PAT_TOKEN@github.com/YOUR_USERNAME/YOUR_PROJECT_REPO_NAME.git](https://YOUR_PAT_TOKEN@github.com/YOUR_USERNAME/YOUR_PROJECT_REPO_NAME.git)
    ```
    Replace `YOUR_PAT_TOKEN`, `YOUR_USERNAME`, and `YOUR_PROJECT_REPO_NAME` with your actual GitHub Personal Access Token, username, and repository name.

## Usage

The package provides a command-line tool called `inference`.

### 1. Predict Emotion

To predict the emotion of a given text:
```bash
inference --input "I am feeling incredibly happy and excited today!"
Example Output:

joy 
(The actual output will be one of the trained emotion labels.)

2. Display Kaggle ID
To display the Kaggle ID associated with this project:

Bash

inference --kaggle
Example Output:

your_kaggle_id 
(This will display the Kaggle ID you've set in the cli.py file.)

Model Details
Base Model: roberta-base (from Hugging Face Transformers)
Fine-tuning: The model was fine-tuned on the provided tweet emotion dataset for [Number] classes.
Key Metric: Optimization was primarily focused on maximizing the validation macro F1-score.
Overfitting Prevention: Early stopping based on validation macro F1-score, weight decay (AdamW), and dropout inherent in the Transformer architecture were used to prevent overfitting.
Model Asset Storage
The trained model weights (.pt file) and the label encoder (.pkl file) are hosted externally due to their size. The emotion_classifier/model_loader.py script will automatically download these assets to the emotion_classifier/assets/ directory the first time the prediction tool is run if they are not already present. Please ensure you have an internet connection for the initial download.
