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
import service.marvel_service as marvel_service


class ComicController(object):
    """this controller contains functions to resolve marvel api comic searches and validations"""

    @jwt_required()
    def search_comics():
        """This route searches for a comic or character using a search string.
        we also can search only comics or characters."""
        search_string = request.args.get('search_string')
        solo_comics = True if request.args.get('solo_comics') == 'y' else False
        solo_personajes = True if request.args.get('solo_personajes') == 'y' else False

        data, status_code = marvel_service.search_comics_and_characters(search_string, solo_comics, solo_personajes)

        return data, status_code

    @jwt_required()
    def validate_comic():
        """This route validates if a commic id exists."""
        idcomic = request.args.get('idcomic') if request.args.get('idcomic') else None
        
        data, status_code = marvel_service.validate_comic(idcomic)

        return data, status_code