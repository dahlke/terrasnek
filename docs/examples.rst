Examples
========

Configure the API Class
-----------------------

.. code:: python

   import os
   from terrasnek.api import TFC

   TFC_TOKEN = os.getenv("TFC_TOKEN", None)
   TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io

   api = TFC(TFC_TOKEN, url=TFC_URL)
   api.set_org("YOUR_ORGANIZATION")

Create a Workspace
------------------

.. code:: python

   create_workspace_payload = {
       # https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload
   }

   created_workspace = api.workspaces.create(create_workspace_payload)
   created_workspace_id = created_workspace["data"]["id"]

Add Variables to a Workspace [Deprecated]
-----------------------------------------

.. code:: python

   create_var_payload = {
       # https://www.terraform.io/docs/cloud/api/variables.html#sample-payload
   }

   api.vars.create(create_var_payload)

Add Workspace Variables
-----------------------

.. code:: python

   create_ws_var_payload = {
       # https://www.terraform.io/docs/cloud/api/variables.html#sample-payload
   }
   workspace_id = "ws-foo"

   api.workspace_vars.create(workspace_id, create_ws_var_payload)

Create a Run on a Workspace
---------------------------

.. code:: python

   create_run_payload = {
       # https://www.terraform.io/docs/cloud/api/run.html#sample-payload
   }

   run = api.runs.create(create_run_payload)
   run_id = self._run["data"]["id"]

Override a Failed Policy Check
------------------------------

.. code:: python

   pol_checks = api.pol_checks.list(run_id)
   api.pol_checks.override(pol_checks["data"][0]["id"])

Apply a Run on a Workspace
--------------------------

.. code:: python

   applied_run = api.runs.apply(run_id)

*For more examples, see the ``./test`` directory in the repository.*
