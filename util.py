import logging
import sys
from bs4 import BeautifulSoup

def extract_text(input):
    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(input, 'html.parser')

    # Extract all text from the HTML document
    text = soup.get_text()

    return text

    # Request was not successful, return None
    return None