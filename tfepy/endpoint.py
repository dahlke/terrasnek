import logging

class TFEEndpoint():

    def __init__(self, base_url, headers):
        # TODO: Bring in the TFE Api class here unless I want to manage all that state in a session.
        self._base_url = base_url
        self._headers = headers
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)