import logging

from falcon.request import Request
from falcon.response import Response


class SortingHook(object):
    """
    Falcon Hook to extract sorting information from request.

    It return a list of tuple for each fields that must be sorted.
    Each tuple contains:
        * The name of the field
        * The sorting order (ASC ord DESC)

    The extracted information are set in the request context dict
    under the context_key value.
    """

    def __init__(self, sort_query_key="sort"):
        self._sort_query_key = sort_query_key
        self._logger = logging.getLogger(__name__)

    def __call__(
        self,
        request: Request,
        response: Response = None,
        resource: object = None,
        params: dict = None,
    ) -> None:
        """
        :param request: Falcon Request
        :param response: Falcon response
        :param resource: Reference to the resource class instance associated with the request
        :param params: dict of URI Template field names
        """
        if not hasattr(resource, "sorting_fields") or not resource.sorting_fields:
            self._logger.debug("sorting_fields is not defined in resource, skipping")
            request.context["sort"] = []
            return
        if self._sort_query_key not in request.params.keys():
            self._logger.debug("Sorting key is not in query, skipping")
            request.context["sort"] = []
            return

        sort_params = request.params[self._sort_query_key]
        if not isinstance(sort_params, list):
            sort_params = [sort_params]
        sort_params = self._remove_invalid_fields(sort_params, resource.sorting_fields)

        sort_list = [self._get_sql_sort(sort) for sort in sort_params]
        request.context["sort"] = sort_list
        self._logger.debug("Sorting set in request.context['sort']")

    @staticmethod
    def _remove_invalid_fields(sort_params, allowed_fields):
        return [f for f in sort_params if f.lstrip("-") in allowed_fields]

    @staticmethod
    def _get_sql_sort(sort):
        if sort[0:1] == "-":
            return sort[1:], "DESC"
        return sort, "ASC"
