import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import nltk


def extract_text_from_epub(file_path):
    book = epub.read_epub(file_path)
    content = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        content.append(soup.get_text())
    return "\n".join(content)


def clean_and_tokenize(text):
    # Remove extra spaces and punctuation
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation

    # Tokenize
    tokens = nltk.word_tokenize(text)
    return tokens


def preprocess_books(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through EPUB files
    for file_name in os.listdir(input_folder):
        if file_name == 'The Books of Earthsea.epub' or file_name == 'The Wheel of Time Books 1-10.epub':
            print(f'{file_name} is a collection')
            continue
        if file_name.endswith('.epub'):
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing: {file_name}")

            # Extract and clean text
            raw_text = extract_text_from_epub(file_path)
            tokens = clean_and_tokenize(raw_text)

            # Save processed tokens to a new file
            output_file = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_processed.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(" ".join(tokens))


def main():
    nltk.download('punkt_tab')

    input_folder = 'Data/raw'
    output_folder = 'Data/processed'
    preprocess_books(input_folder, output_folder)


if __name__ == '__main__':
    main()