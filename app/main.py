import requests
from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates

from typing import Optional, Any
from pathlib import Path

"""
mes from&import
"""

from app.schemas import Points
from math import sqrt
from typing import List

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request},
    )

# Nouvelle Route
# Pokemon ID
@api_router.get("/pokemon", status_code=200)
def search_pokemon(request: Request, pokemon_id: int):
    """
    Super recherche Pokemon return nom+image
    """
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    data = r.json()
    pokemon_name = data["name"]
    pokemon_img_url = data["sprites"]["front_default"]

    # lister les types
    pokemon_types = []
    # A mettre a jour utiliser range & len pour data[types]
    for i in range(len(data["types"])) :
        pokemon_types.append(data["types"][i]["type"]["name"])
    pokemon = {"name": pokemon_name, "image_url": pokemon_img_url,"type":pokemon_types}

    return TEMPLATES.TemplateResponse("index.html", {"request": request, "pokemon": pokemon})



@api_router.post("/compute_distance/",status_code=200)
def compute_distance(points: List[Points] = [{"x": 0, "y": 0}, {"x": 0, "y": 0}]) -> dict: # defini un exemple
    """
    calculer les coordonnées
    """

    distance = 0.0

    # recup la taille de la list
    for i in range(len(points) - 1) : # i = 0 || ici on sait que seul 2 point sont utiliser
        # mettre les valeurs dans 2 variables p1&p2
        p1 = points[i]
        p2 = points[i+1]
    distance = sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

    return {"resultat" : distance}



app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
