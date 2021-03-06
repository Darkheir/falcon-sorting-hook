falcon-sorting-hook
======================

.. image:: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square
    :target: LICENSE
.. image:: https://travis-ci.org/Darkheir/falcon-sorting-hook.svg?branch=master
    :target: https://travis-ci.org/Darkheir/falcon-sorting-hook
.. image:: https://codecov.io/gh/Darkheir/falcon-sorting-hook/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Darkheir/falcon-sorting-hook
.. image:: https://api.codacy.com/project/badge/Grade/a8a34e89d34b4a928e988fe1624e2eae
    :target: https://www.codacy.com/app/Darkheir/falcon-sorting-hook?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Darkheir/falcon-sorting-hook&amp;utm_campaign=Badge_Grade
.. image:: https://pyup.io/repos/github/Darkheir/falcon-sorting-hook/shield.svg
    :target: https://pyup.io/repos/github/Darkheir/falcon-sorting-hook/
    :alt: Updates


A small falcon hook to parse sorting elements from the request.

Usage
-----

The easiest way to use this hook is the following:

.. code:: python

    class Resource:
        sorting_fields = ("foo", "bar")  # List of fields allowed for sorting

        @falcon.before(SortingHook())
        def on_get(self, req, resp, user):
            # Here req['context']['sort'] is set

The Hook will look in the query parameters for parameters looking like :code:`sort=value`.

The default sorting order is ascending.
To sort in a descending order a minus (:code:`-`) sign needs to be specified before the value.
i.e. :code:`sort=-value`

It is possible to specify multiple sorting values by separating them with a comma.
i.e. :code:`sort=-value1,value2`

It will create a list in the request context accessible at :code:`req.context['sort']`.
This list consists of tuples where the first element is the name of the field to sort on
and the second the order to follow (either :code:`ASC` or :code:`DESC`)

i.e. :code:`[('foo', 'ASC'), ('bar', 'DESC')]`.


Configuration options
---------------------

Allowing fields for sorting
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For security reasons, the fields allowed for sorting must be specified in
the :code:`sorting_fields` attribute of the resource.

All the fields not defined in it will be discarded by the hook.


Default sorting order
~~~~~~~~~~~~~~~~~~~~~

It is possible to specify a default sorting order by setting the :code:`default_sorting` attribute in the resource.

This attribute must be a string or a tuple that respects the convention we have for the request parameter.

The attributes specified as the default order must also be part of :code:`sorting_fields`.

Examples:

.. code:: python

    default_sorting = '-foo'
    # or
    default_sorting = ('foo', '-bar')

Hook configuration
~~~~~~~~~~~~~~~~~~

One parameter can be passed to the hook:

* sort_query_key : The name of the key used in the query to sort data. Default: :code:`sort`.

Example:

.. code:: python

    @falcon.before(PaginationFromRequestHook(
        sort_query_key='order',
    ))
    def on_get(self, req, resp, user):
        # Get request

