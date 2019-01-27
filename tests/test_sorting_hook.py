from falcon_sorting.sorting_hook import SortingHook


def test_empty_request(request_obj, mocker):
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), mocker.Mock(), dict())

    assert isinstance(request_obj.context.get("order"), list)


def test_request_with_sort_default(request_obj, mocker):
    request_obj.params["sort"] = 'foo'
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), mocker.Mock(), dict())

    assert request_obj.context["order"] == [('foo', 'ASC')]


def test_request_with_sort_desc(request_obj, mocker):
    request_obj.params["sort"] = '-foo'
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), mocker.Mock(), dict())

    assert request_obj.context["order"] == [('foo', 'DESC')]


def test_request_with_multiple_sorts(request_obj, mocker):
    request_obj.params["sort"] = ['foo', '-bar']
    hook = SortingHook()
    hook(request_obj, mocker.Mock(), mocker.Mock(), dict())

    assert request_obj.context["order"] == [('foo', 'ASC'), ('bar', 'DESC')]
