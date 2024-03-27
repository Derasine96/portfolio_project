import requests
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()


class ThemeOption(BaseModel):
    """Model for getting user interface theme"""
    name: str
    color: str


def fetch_theme_options():
    """Function to fetch theme options"""
    access_key = 'irA9Q-uhVFnAd1Upu_WNpLaUUiWYVpxBkBic2VUBfwE'
    collection_id = '206'
    per_page = 10
    page = 1

    url = f'https://api.unsplash.com/collections/{collection_id}/photos'
    headers = {'Authorization': f'Client-ID {access_key}'}
    params = {'per_page': per_page, 'page': page}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            photos = response.json()
            return photos
        else:
            print(
                f"Failed to fetch theme options from API: {response.status_code}")
            return []
    except Exception as e:
        print(f"Failed to fetch theme options from API: {str(e)}")
        return []


@router.get("/themes", response_model=List[ThemeOption])
async def read_themes():
    """Returns a list of available themes."""
    data = fetch_theme_options()
    items = []
    for item in data:
        if 'name' in item:
            items.append(ThemeOption(**item))
        else:
            pass
    return items

