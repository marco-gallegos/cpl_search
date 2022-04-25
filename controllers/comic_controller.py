"""
@Author Marco A. Gallegos
@Date 2022/04/25
@Description
    comic  controller
"""
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from config.config import APP_CONFIG
import requests


class ComicController(object):
    """this controller contains functions to resolve marvel api comic searches and validations"""

    @jwt_required()
    def search_comics():
        """This route searches for a comic or character using a search string.
        we also can search only comics or characters."""
        search_string = request.args.get('search_string')
        solo_comics = True if request.args.get('solo_comics') == 'y' else False
        solo_personajes = True if request.args.get('solo_personajes') == 'y' else False

        if solo_comics and solo_personajes:
            return {
                'error': 'No se puede buscar solo comics y personajes a la vez'
            }, 400

        personaje = {
            "id": "",
            "name": "",
            "image": "", # url
            "appearances": 0, # apariciones en comics
        }
        comics = {
            "id": "",
            "title": "",
            "image": "", # url
            "onsaleDate": "", # fecha lanzamiento
        }
        apiurl = "https://gateway.marvel.com:443/v1/public/"
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

            for comic in request_comics.json()["data"]["results"]:
                comics["id"] = comic["id"]
                comics["title"] = comic["title"]
                comics["image"] = comic["thumbnail"]["path"] + "." + comic["thumbnail"]["extension"]
                comics["onsaleDate"] = comic["dates"][0]["date"]
                response["comics"].append(comics.copy())
        return response, 200

    @jwt_required()
    def validate_comic():
        """This route validates if a commic id exists."""
        idcomic = request.args.get('idcomic') if request.args.get('idcomic') else None
        apiurl = "https://gateway.marvel.com:443/v1/public/"
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
        # print(request_comic)
        # print(request_comic.json())
        if request_comic.status_code == 200:
            return {
                "exists": True,
                "data": request_comic.json()["data"]["results"][0]
            }, 200
        else:
            return {
                "exists": False
            }, 404