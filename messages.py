
"""Messages module."""
import requests

def win():
    """
        Call endpoint to signal a game win
    """
    requests.post('http://localhost:80')
