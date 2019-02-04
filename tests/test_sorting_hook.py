from falcon_sorting.sorting_hook import SortingHook


def test_empty_request(request_obj, mocker):
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), mocker.Mock(), dict())

    assert isinstance(request_obj.context.get("sort"), list)


def test_request_with_sort_default(request_obj, mocker):
    request_obj.params["sort"] = 'foo'
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), mocker.Mock(), dict())

    assert request_obj.context["sort"] == [('foo', 'ASC')]


def test_request_with_sort_desc(request_obj, mocker):
    request_obj.params["sort"] = '-foo'
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), mocker.Mock(), dict())

    assert request_obj.context["sort"] == [('foo', 'DESC')]


def test_request_with_multiple_sorts(request_obj, mocker):
    request_obj.params["sort"] = ['foo', '-bar']
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), mocker.Mock(), dict())

    assert request_obj.context["sort"] == [('foo', 'ASC'), ('bar', 'DESC')]
