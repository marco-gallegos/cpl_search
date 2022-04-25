from flask_restful import Api
import controllers

def setup_routes(app, APP_CONFIG):
    """
    Setup the routes for the flask app
    :param app: flask app
    :return:
    """

    # default flask routes
    @app.route("/searchComics", methods=["GET"])
    def search_comics():
        return controllers.ComicController.search_comics()


    @app.route("/comicexist", methods=["GET"])
    def comic_exist():
        return controllers.ComicController.comic_exist()


    # Setup the flask restful api
    api = Api(app)

    # rutas resource de flask restful
    # api.add_resource(controllers.HelloWorld, '/')

    return True
