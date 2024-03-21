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
    """Function to request themes for user interface from an external API"""
    theme_api_url = "https://source.unsplash.com/300x200/?nature"
    try:
        response = requests.get(theme_api_url)
        if response.status_code == 200:
            theme_options = response.json()
            return [ThemeOption(name=option['name'], color=option['color'])
                    for option in theme_options]
        else:
            print(f"Failed to fetch theme options: {response.status_code}")
            return []
    except Exception as e:
        print(f"Failed to fetch theme options from API: {str(e)}")
        return []

@router.get("/theme-options", response_model=List[ThemeOption])
async def get_theme_options():
    """FastAPI endpoint to fetch theme options"""
    return fetch_theme_options()

