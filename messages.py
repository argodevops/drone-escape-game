
import requests

def win():
    """_summary_
        Call endpoint to signal a game win
    """
    requests.post('http://localhost:80')
