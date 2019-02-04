import pytest


@pytest.fixture()
def request_obj(mocker):
    class Request(object):
        client_accepts_json = True
        content_type = "application/json"
        method = None
        content_length = 100
        context = dict()
        params = dict()
        stream = mocker.Mock()

    return Request()


@pytest.fixture()
def resource():
    class Resource:
        sorting_fields = ["foo", "bar"]

    return Resource()
