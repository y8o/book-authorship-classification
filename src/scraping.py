import requests
from bs4 import BeautifulSoup
import re
import time
import os

def get_authors_from_letter(letter='a', language='english'):
    """
    Extracts authors from Project Gutenberg for a specific letter and language.
    
    Args:
        letter (str): The letter to extract authors for.
        language (str): The language of books to filter (e.g., 'english', 'french').
        
    Returns:
        list: List of dictionaries containing author information.
    """
    print(f"Scraping authors for letter: {letter} and language: {language}")
    
    # The correct URL format based on your sample
    url = f"https://www.gutenberg.org/browse/authors/{letter}.html.utf8"
    print(f"Fetching {url}")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            # Try alternative URL format if the first one fails
            url = f"https://www.gutenberg.org/browse/authors/{letter}"
            print(f"Trying alternative URL: {url}")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch alternative URL. Status code: {response.status_code}")
                return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the div containing author listings
        author_div = soup.find("div", class_="pgdbbyauthor")
        if not author_div:
            print("Could not find author listings div")
            return []

        authors = []
        
        # Find all h2 elements (author headings)
        author_headings = author_div.find_all("h2")
        
        for heading in author_headings:
            # Skip "See:" references
            if "See:" in heading.text:
                continue

            # Get author name - extract from heading text or anchor
            author_name = None
            author_id = None

            # Look for anchor with name attribute
            anchor = heading.find("a", attrs={"name": True})
            if anchor:
                author_id = anchor.get("name")
                # Clean up the author name by removing the permalink symbol
                author_name = heading.text.replace("¶", "").strip()
            else:
                # If no anchor with name, just use the heading text
                author_name = heading.text.strip()

            if not author_name:
                continue

            # Find the ul that follows this heading
            author_ul = heading.find_next("ul")
            if not author_ul:
                print(f"No book list found for {author_name}")
                continue

            # Count books in the specified language where the author is listed as "Author"
            book_count = 0
            books = []

            # Find all li elements with class pgdbetext (etext entries)
            book_items = author_ul.find_all("li", class_="pgdbetext")
            
            for item in book_items:
                book_link = item.find("a")
                if not book_link:
                    continue
                
                book_title = book_link.text.strip()
                book_url = book_link.get("href")

                # Check if book is in the specified language and author is listed as Author
                item_text = item.text.lower()
                if f"({language})" in item_text and "(as author)" in item_text:
                    book_count += 1
                    books.append({
                        "title": book_title,
                        "url": f"https://www.gutenberg.org{book_url}" if book_url.startswith("/") else book_url
                    })

            # Only add authors who meet the minimum books requirement
            if book_count >= min_books:
                authors.append({
                    "name": author_name,
                    "book_count": book_count
                })
        
        return authors

    except Exception as e:
        print(f"Error scraping letter {letter}: {e}")
        return []

def get_prolific_authors(min_books=7, language='english', letters=None):
    """
    Gets a list of authors with at least the specified number of books.
    
    Args:
        min_books (int): Minimum number of books an author must have.
        language (str): Language to filter by.
        letters (list): List of letters to scrape. If None, all letters are scraped.
        
    Returns:
        list: List of dictionaries containing author information.
    """
    if letters is None:
        # All lowercase letters plus 'other'
        letters = list('abcdefghijklmnopqrstuvwxyz') + ['other']
    
    prolific_authors = []

    for letter in letters:
        authors = get_authors_from_letter(letter, language)
        
        # Filter for prolific authors
        letter_prolific = [author for author in authors if author['book_count'] >= min_books]
        prolific_authors.extend(letter_prolific)

        print(f"Found {len(letter_prolific)} prolific authors for letter '{letter}'")

        # Be nice to the server
        time.sleep(1)

    # Sort by book count (descending)
    prolific_authors.sort(key=lambda x: x['book_count'], reverse=True)

    return prolific_authors

def save_author_list(authors, filename="prolific_authors.txt"):
    """
    Saves the list of authors to a text file.
    
    Args:
        authors (list): List of author dictionaries.
        filename (str): Name of the file to save to.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Found {len(authors)} prolific authors:\n\n")
            
            for i, author in enumerate(authors):
                # Print only the author name, time period (if available), and book count
                f.write(f"{i+1}. {author['name']} - {author['book_count']} books\n")
                
        print(f"Author list saved to {filename}")
        return True

    except Exception as e:
        print(f"Error saving author list: {e}")
        return False

if __name__ == "__main__":
    # Get inputs from the user
    language = input("Enter language (e.g., 'english'): ").lower()
    min_books = int(input("Enter minimum number of books per author: "))

    # Get authors from specific letters
    letters_to_scrape = ['a']  # For testing, we scrape only the letter 'a'
    
    print("Starting to scrape prolific authors...")
    prolific_authors = get_prolific_authors(min_books=min_books, language=language, letters=letters_to_scrape)
    
    print(f"\nFound {len(prolific_authors)} prolific authors:")
    for i, author in enumerate(prolific_authors):
        # Print only the author name and book count
        print(f"{i+1}. {author['name']} - {author['book_count']} books")

    # Save the author list to a file
    save_author_list(prolific_authors)
