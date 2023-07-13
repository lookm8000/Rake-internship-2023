import os
import json
from rake_nltk import Rake  # Import Rake, a keyword extraction algorithm
from collections import Counter  # Import Counter, a container that keeps track of how many times equivalent values are added
import plotly.graph_objects as go  # Import Plotly's graph_objects module for high-level plots
from nltk import ngrams  # Import ngrams from NLTK for creating bigrams
from nltk.corpus import stopwords  # Import stopwords from NLTK, these are common words like 'is', 'the', etc.
from nltk.tokenize import word_tokenize  # Import the word tokenizer from NLTK

# Specify the name of the folder where the JSON files are stored
folder_name = "folder"
# Create the full path to the folder
folder_path = f"./{folder_name}"

# Configure the Rake algorithm
r = Rake(
    stopwords=None,
    punctuations=None,
    max_length=5,
    min_length=3
)

# Create Counters to store keyword and bigram counts
all_keywords_count = Counter()
all_bigrams_count = Counter()

# Define a set of English stopwords. These are common words that we want to exclude from our keywords and bigrams
stop_words = set(stopwords.words('english'))

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):  # If the file is a JSON file
        file_path = os.path.join(folder_path, filename)  # Construct the full path to the file
        
        # Try to open and read the file
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)  # Load the JSON data from the file
                json_key = "text"
                text = data[json_key]  # Extract the text data
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:  # If an error occurs, print a message and skip this file
            print(f"Error in '{filename}': {str(e)}. Skipping...")
            continue
        
        # Use Rake to extract keywords from the text
        r.extract_keywords_from_text(text)  
        keywords = r.get_ranked_phrases()  # Get the ranked keywords
        
        # Filter the keywords to remove any non-alphabetic words
        keywords = [keyword for keyword in keywords if all(word.isalpha() for word in keyword.split())]
        # Count the occurrences of each keyword
        keywords_count = Counter(keywords)  
        
        # Remove any keywords that only appear once
        keywords_count = {k: v for k, v in keywords_count.items() if v > 1}
        
        # Add these counts to the total counts
        all_keywords_count.update(keywords_count)

        # Tokenize the text, converting it to lower case and removing non-alphabetic words and stopwords
        tokens = [token for token in word_tokenize(text.lower()) if token.isalpha() and token not in stop_words]

        # Generate and count bigrams from the tokens
        bigrams = ngrams(tokens, 2)
        bigram_count = Counter(bigrams)
        
        # Remove bigrams that only appear once
        bigram_count = {k: v for k, v in bigram_count.items() if v > 1}

        # Add these counts to the total counts
        all_bigrams_count.update(bigram_count)

# Calculate the total count of all keywords and bigrams
total_keyword_count = sum(all_keywords_count.values())
total_bigram_count = sum(all_bigrams_count.values())

# Sort the keywords and bigrams by their frequency
sorted_keywords = sorted({k: {'count': v, 'importance': round((v/total_keyword_count*100), 3)} for k, v in all_keywords_count.items()}.items(), key=lambda x: x[1]['importance'], reverse=True)
sorted_bigrams = sorted({f"{k[0]} {k[1]}": {'count': v, 'importance': round((v/total_bigram_count*100), 3)} for k, v in all_bigrams_count.items()}.items(), key=lambda x: x[1]['importance'], reverse=True)

# Importance is calculated as the frequency of the keyword or bigram divided by the total count of all keywords or bigrams, respectively.
# This gives the percentage of the total that each keyword or bigram represents.

# Write the results to info.json
with open('info.json', 'w') as f:
    json.dump({"keywords": dict(sorted_keywords), "bigrams": dict(sorted_bigrams)}, f, ensure_ascii=False, indent=4)

# Write all keywords and bigrams to separate files
with open('keywords.json', 'w') as f:
    json.dump(dict(sorted_keywords), f, ensure_ascii=False, indent=4)

with open('bigrams.json', 'w') as f:
    json.dump(dict(sorted_bigrams), f, ensure_ascii=False, indent=4)

# Print the total count and top 10 keywords and bigrams
print(f"Total keywords: {total_keyword_count}")
print(f"Top 10 keywords: {sorted_keywords[:10]}")
print(f"Total bigrams: {total_bigram_count}")
print(f"Top 10 bigrams: {sorted_bigrams[:10]}")

# Combine keywords and bigrams
combined_items = sorted_keywords + sorted_bigrams
# Sort by importance
sorted_combined_items = sorted(combined_items, key=lambda x: x[1]['importance'], reverse=True)

# Plot the top 20 keywords and bigrams
top_items = sorted_combined_items[:20]
items, item_data = zip(*top_items)
item_frequencies = [data['count'] for data in item_data]

fig = go.Figure(go.Bar(
            x=item_frequencies,
            y=items,
            orientation='h'))

fig.update_layout(
    title_text='Top 20 Items',
    xaxis_title="Frequencies",
    yaxis_title="Items",
    yaxis={'autorange': 'reversed'}
)

fig.show()
