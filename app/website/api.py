import requests
from django.utils.translation import get_language

API_DOMAIN = "https://jsonplaceholder.typicode.com/"


def get_posts(page=1):
    """Get posts from API"""
    response = requests.get(
        API_DOMAIN + get_language() + "/posts/", params={"page": page}
    )
    return response.json()


def get_post(slug):
    """Get post from API"""
    response = requests.get(API_DOMAIN + get_language() + "/post/" + slug + "/")
    return response.json()
