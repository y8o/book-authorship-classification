import os
import requests
from bs4 import BeautifulSoup

def read_author_list(filename):
    """
    Reads the list of authors and their book counts from a text file.

    Args:
        filename (str): The file containing the list of authors.

    Returns:
        list: A list of author names.
    """
    authors = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                # Only read lines containing author info
                if line.strip() and "books" in line:
                    parts = line.strip().split(" - ")
                    author_name = parts[0].strip()
                    authors.append(author_name)
    except Exception as e:
        print(f"Error reading the author list: {e}")
    return authors

def create_author_folder(author_name, base_dir):
    """
    Creates a folder for an author based on their name.

    Args:
        author_name (str): The name of the author.
        base_dir (str): The base directory where author folders are created.

    Returns:
        str: Path to the created author's folder.
    """
    # Format name as "lastname_firstinitial" or "lastname_firstname" if needed
    name_parts = author_name.split(", ")
    if len(name_parts) == 2:
        last_name = name_parts[0]
        first_name = name_parts[1]
        folder_name = f"{last_name}_{first_name[0]}"
    else:
        # Handle case where name doesn't split as expected
        folder_name = author_name.replace(" ", "_").replace(",", "").lower()

    author_folder = os.path.join(base_dir, folder_name)
    os.makedirs(author_folder, exist_ok=True)
    
    return author_folder

def download_book(book_url, output_file):
    """
    Downloads a book from Project Gutenberg and saves it to a file.

    Args:
        book_url (str): URL of the book on Project Gutenberg.
        output_file (str): Filename to save the book content to.

    Returns:
        bool: True if download was successful, False otherwise.
    """
    try:
        print(f"Downloading from {book_url}")
        response = requests.get(book_url)
        response.raise_for_status()

        # Look for plain text link in the page
        soup = BeautifulSoup(response.text, "html.parser")
        download_table = soup.find("table", class_="files")
        
        if download_table:
            text_link = None
            for row in download_table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) >= 2:
                    file_format = cells[0].text.strip().lower()
                    if "plain text" in file_format and "utf-8" in file_format:
                        links = cells[1].find_all("a")
                        if links:
                            text_link = links[0].get("href")
                            break

            if not text_link:
                print("No suitable plain text link found.")
                return False

            # Construct full URL if necessary
            if not text_link.startswith("http"):
                text_link = "https://www.gutenberg.org" + text_link

            # Download the book
            book_response = requests.get(text_link)
            book_response.raise_for_status()

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(book_response.text)

            print(f"Book saved to {output_file}")
            return True
        else:
            print("Download table not found.")
            return False

    except Exception as e:
        print(f"Error downloading book: {e}")
        return False

def download_books_for_author(author_name, books, base_dir):
    """
    Downloads all books for a given author.

    Args:
        author_name (str): The name of the author.
        books (list): A list of book URLs and titles to download.
        base_dir (str): The base directory where author folders are created.

    Returns:
        int: Number of books successfully downloaded.
    """
    # Create the author folder
    author_folder = create_author_folder(author_name, base_dir)
    successful_downloads = 0

    for book in books:
        book_url = book["url"]
        book_title = book["title"]
        filename = os.path.join(author_folder, f"{book_title}.txt")

        if download_book(book_url, filename):
            successful_downloads += 1

    return successful_downloads

def main():
    # Input: Read the txt file with the author list
    list_filename = input("Enter the filename of the prolific author list (e.g., 'english_10books.txt'): ")
    authors = read_author_list(list_filename)

    # Create base directory for saving the downloaded books
    base_dir = "data/raw/"
    os.makedirs(base_dir, exist_ok=True)

    # For each author, get the books and download them
    for author_name in authors:
        print(f"Downloading books for author: {author_name}")
        books = []  # This would normally come from an API or a database of book URLs for each author
        
        # Example: Here we add some placeholder URLs for each author
        # In a real application, you would gather these from Project Gutenberg
        books.append({
            "title": "Example Book 1",
            "url": "https://www.gutenberg.org/ebooks/12345"  # Replace with real URLs
        })
        books.append({
            "title": "Example Book 2",
            "url": "https://www.gutenberg.org/ebooks/67890"  # Replace with real URLs
        })

        download_books_for_author(author_name, books, base_dir)

if __name__ == "__main__":
    main()
