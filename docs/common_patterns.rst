Common Patterns
===============

There are some common patterns across many endpoints in `terrasnek` that can all be addressed the same way, but
are a bit volatile to document directly in the docstrings. For any endpoint that supports a `filters` query
parameter, or an `include` query parameter, use the below format as inputs.

Example Filters
----------------

Some of the API's endpoints can filter the returned data by adding a `filters` query
parameter. There is an
`example filter endpoint <https://www.terraform.io/cloud-docs/api-docs/variables#query-parameters>`_
which demonstrates example filters on an endpoint.

You can find an example of the format your `filters` parameter should be in below.

.. code:: python

   example_filters = [
	  {
			"keys": ["workspace", "name"], # ends up as ["workspace"]["name"]
			"value": "foo"
	  },
	  {
			"keys": ["organization", "name"], # ends up as ["organization"]["name"]
			"value": "bar"
	  }
   ]

Example Include
---------------

Some of the API's `GET` endpoints can return additional information about nested resources by adding an `include` query
parameter, whose value is a comma-separated list of resource types.

The related resource options are listed in each endpoint's documentation where available.

The related resources will appear in an `included` section of the response.

There is an
`example related resources endpoint <https://www.terraform.io/cloud-docs/api-docs/run#available-related-resources>`_
which demonstrates example related resources endpoints.

You can find an example of the format your `includes` parameter should be in below.

.. code:: python

   example_include = ["plan", "created_by", "cost_estimate"]

*For more examples, see the ``./test`` directory in the repository.*
