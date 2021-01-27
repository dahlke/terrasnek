Getting Started
===============

Recommended Env Var Usage
-------------------------

.. code:: python

   import os

   TFC_TOKEN = os.getenv("TFC_TOKEN", None)
   TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io

Using TLS
---------

.. code:: python

   from terrasnek.api import TFC

   api = TFC(TFC_TOKEN, url=TFC_URL)
   api.set_org("YOUR_ORGANIZATION")

Using Insecure TLS
------------------

.. code:: python

   from terrasnek.api import TFC

   api = TFC(TFC_TOKEN, url=TFC_URL, verify=False)
   api.set_org("YOUR_ORGANIZATION")
