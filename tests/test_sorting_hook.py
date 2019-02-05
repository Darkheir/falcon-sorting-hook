from falcon_sorting.sorting_hook import SortingHook


def test_empty_request_empty_resource(request_obj, mocker):
    hook = SortingHook()

    class EmptyResource(object):
        sorting_fields = []

    hook(request_obj, mocker.Mock(), EmptyResource(), dict())

    assert isinstance(request_obj.context.get("sort"), list)


def test_request_with_sort_asc_empty_sort_fields(request_obj, mocker):
    request_obj.params["sort"] = "foo"
    hook = SortingHook()

    class EmptyResource(object):
        sort_fields = []

    hook(request_obj, mocker.Mock(), EmptyResource(), dict())

    assert request_obj.context["sort"] == []


def test_request_with_sort_asc(request_obj, resource, mocker):
    request_obj.params["sort"] = "foo"
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), resource, dict())

    assert request_obj.context["sort"] == [("foo", "ASC")]


def test_request_with_sort_desc(request_obj, resource, mocker):
    request_obj.params["sort"] = "-foo"
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), resource, dict())

    assert request_obj.context["sort"] == [("foo", "DESC")]


def test_request_with_multiple_sorts(request_obj, resource, mocker):
    request_obj.params["sort"] = ["foo", "-bar"]
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), resource, dict())

    assert request_obj.context["sort"] == [("foo", "ASC"), ("bar", "DESC")]


def test_request_with_multiple_sorts_disallowed_field(request_obj, resource, mocker):
    request_obj.params["sort"] = ["foos", "-bar"]
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), resource, dict())

    assert request_obj.context["sort"] == [("bar", "DESC")]


def test_request_with_sort_default_empty_request(request_obj, mocker):
    hook = SortingHook()

    class Resource(object):
        sorting_fields = ["foo"]
        default_sorting = "-foo"

    hook(request_obj, mocker.Mock(), Resource(), dict())

    assert request_obj.context["sort"] == [("foo", "DESC")]


def test_request_with_sort_default_and_param(request_obj, mocker):
    request_obj.params["sort"] = ["bar"]
    hook = SortingHook()

    class Resource(object):
        sorting_fields = ["foo", "bar"]
        default_sorting = "-foo"

    hook(request_obj, mocker.Mock(), Resource(), dict())

    assert request_obj.context["sort"] == [("bar", "ASC")]


def test_request_with_sort_empty_request(request_obj, resource, mocker):
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), resource, dict())

    assert request_obj.context["sort"] == []
