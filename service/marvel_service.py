"""
@Author Marco A. Gallegos
@Date 2022/04/25
@Description
    marvel service
"""
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from config.config import APP_CONFIG
import requests

marvel_api_url:str = "https://gateway.marvel.com:443/v1/public/"

def search_comics_and_characters(search_string: str, solo_comics: bool, solo_personajes: bool):
    if solo_comics and solo_personajes:
        return {
            'error': 'No se puede buscar solo comics y personajes a la vez'
        }, 400

    apiurl = marvel_api_url
    apikey = APP_CONFIG["APIKEY"]
    timestamp = APP_CONFIG["TIMESTAMP"]
    hash = APP_CONFIG["HASH"]

    response = {
        "personajes": [

        ],
        "comics": [
        ]
    }

    buscar_todo = True if solo_comics is False and solo_personajes is False else False

    if solo_personajes or buscar_todo:
        request_characters = requests.get(
            f"{apiurl}characters",
            params={
                "nameStartsWith": search_string,
                "apikey": apikey,
                "ts": timestamp,
                "hash": hash,
            },
        )

        personaje = {
        }

        for character in request_characters.json()["data"]["results"]:
            personaje["id"] = character["id"]
            personaje["name"] = character["name"]
            personaje["image"] = character["thumbnail"]["path"] + "." + character["thumbnail"]["extension"]
            personaje["appearances"] = character["comics"]["available"]
            response["personajes"].append(personaje.copy())

    if solo_comics or buscar_todo:
        request_comics = requests.get(
            f"{apiurl}comics",
            params={
                "titleStartsWith": search_string,
                "apikey": apikey,
                "ts": timestamp,
                "hash": hash,
            },
        )

        comics = {
        }
        for comic in request_comics.json()["data"]["results"]:
            comics["id"] = comic["id"]
            comics["title"] = comic["title"]
            comics["image"] = comic["thumbnail"]["path"] + "." + comic["thumbnail"]["extension"]
            comics["onsaleDate"] = comic["dates"][0]["date"]
            response["comics"].append(comics.copy())
    return response, 200


def validate_comic(idcomic: str):
    """This function search a comic to calidate the existance."""
    apiurl = marvel_api_url
    apikey = APP_CONFIG["APIKEY"]
    timestamp = APP_CONFIG["TIMESTAMP"]
    hash = APP_CONFIG["HASH"]

    request_comic = requests.get(
        f"{apiurl}comics/{idcomic}",
        params={
            "apikey": apikey,
            "ts": timestamp,
            "hash": hash,
        }
    )
    
    if request_comic.status_code == 200:
        return {
            "exists": True,
            "data": request_comic.json()["data"]["results"][0]
        }, 200
    else:
        return {
            "exists": False
        }, 404