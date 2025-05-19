# Rake-internship-2023
# Keyword & Bigram Extraction with Visualization

This project processes a collection of `.json` files containing text data, extracts meaningful keywords and bigrams using NLP techniques, and visualizes the most important terms across the dataset.

## Features
- Extracts keywords using the RAKE algorithm
- Tokenizes and generates bigrams using NLTK
- Filters and ranks keywords/bigrams by importance
- Outputs results into organized JSON files:
  - `info.json` – Combined keyword and bigram data with counts and importance
  - `keywords.json` – Sorted keywords with metadata
  - `bigrams.json` – Sorted bigrams with metadata
  - `everydoc.json` – Top 3 keywords and bigrams for each processed document
- Interactive Plotly visualization of top 20 terms

## Requirements
Make sure the following Python packages are installed:
```bash
pip install rake-nltk nltk plotly
```
You will also need to download NLTK resources:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Usage
1. Place your `.json` files inside a folder (default: `folder`). Each file should include a `"text"` field.
2. Run the script:
```bash
python your_script.py
```
3. Enter the number of documents to process (e.g., `5`, or `all` to process everything).

## Output
- JSON files with keyword/bigram stats saved in the working directory
- Top 20 items visualized in a horizontal bar chart (via Plotly)

## Example JSON Format
Each document should follow this format:
```json
{
  "text": "Your text content here."
}
```

## Author
Maile Look  
Oregon State University – Computer Science | Business Information Systems  
LinkedIn: [maile-look](https://www.linkedin.com/in/maile-look/)

---
*This project was created for analyzing patterns in textual data using NLP pipelines.*

