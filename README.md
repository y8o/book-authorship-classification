# Book Authorship Classification

A machine learning project to classify book authorship based on writing style and content analysis.

## Project Structure

```
book-authorship-classification/
├── data/               # Data directory
│   ├── raw/           # Raw data files
│   └── processed/     # Processed data files
├── notebooks/         # Jupyter notebooks
│   └── exploratory_analysis.ipynb
├── src/              # Source code
│   ├── scraping.py   # Web scraping utilities
│   ├── preprocessing.py  # Data preprocessing
│   ├── vectorization.py  # Text vectorization
│   ├── model.py      # ML model implementation
│   └── app.py        # Web application
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Jupyter notebook for exploratory analysis:
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

2. Run the web application:
```bash
python src/app.py
```
