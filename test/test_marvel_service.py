from config.config import APP_CONFIG
import service.marvel_service as marvel_service
# run this inside the docker container or set up a .env file
# very basic test for now, not a lot of time,
# objective test the main features on this service
# i dont need test jwt or framework because they are tested already
# * db string setup
# * db conection


def test_marvel_api_config():
    marvel_apikey = True if APP_CONFIG['APIKEY'] is not None else False
    marvel_timestamp = True if APP_CONFIG['TIMESTAMP'] is not None else False
    marvel_hash = True if APP_CONFIG['HASH'] is not None else False

    marvel_check = marvel_apikey and marvel_timestamp and marvel_hash
    assert marvel_check is True, "Marvel API config is not set"


def test_marvel_service_good_search_only_comics():
    marvel_result, status_code = marvel_service.search_comics_and_characters("spider", True, False)
    assert marvel_result is not None, "Marvel API call failed"
    assert len(marvel_result["personajes"]) == 0, "Marvel service returns personajes with out searching for them"
    assert len(marvel_result["comics"]) > 0, "Marvel service does not return comics"
    assert status_code == 200, "Marvel service returns a status code different than 200"


def test_marvel_service_bad_search_only_comics():
    marvel_result, status_code = marvel_service.search_comics_and_characters("calcetin con rombos man", True, False)
    assert marvel_result is not None, "Marvel API call failed"
    assert len(marvel_result["personajes"]) == 0, "Marvel service returns personajes with out searching for them"
    assert len(marvel_result["comics"]) == 0, "Marvel service returns comics on a mot existant title comics"
    assert status_code == 200, "Marvel service returns a status code different than 200"


def test_marvel_service_bad_search_on_only_both_params():
    marvel_result, status_code = marvel_service.search_comics_and_characters("calcetin con", True, True)
    assert marvel_result is not None, "Marvel API call failed"
    assert status_code == 400, "Marvel service returns a status code different than 400"
    assert len(marvel_result["error"]) > 0, "Marvel service does not return an error message"


def test_marvel_service_good_search_only_characters():
    marvel_result, status_code = marvel_service.search_comics_and_characters("spider", False, True)
    assert marvel_result is not None, "Marvel API call failed"
    assert len(marvel_result["comics"]) == 0, "Marvel service returns personajes with out searching for them"
    assert len(marvel_result["personajes"]) > 0, "Marvel service does not return comics"
    assert status_code == 200, "Marvel service returns a status code different than 200"


def test_marvel_service_identifyes_a_good_comic():
    # this comic comes from marvel's api
    mocked_marvel_api_comic = {
        "id": 59539,
        "image": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg",
        "onsaleDate": "2029-12-31T00:00:00-0500",
        "title": "Doctor Strange (2015) #10 (Henderson Mighty Men Variant)"
    }
    marvel_result, status_code = marvel_service.validate_comic(mocked_marvel_api_comic["id"])
    assert status_code == 200, "marvel api does not identyfies a valid comic"
    assert marvel_result["exists"] is True, "marvel api does not identyfies a valid comic"
    assert marvel_result["data"]["id"] == mocked_marvel_api_comic["id"], "marvel service does not return the correct comic"


def test_marvel_service_fails_on_a_bad_comic():
    marvel_result, status_code = marvel_service.validate_comic("no existo :c")
    assert status_code == 404, "marvel service identifyes a bad id."
    assert marvel_result["exists"] is False, "marvel service identifyes a bad id."