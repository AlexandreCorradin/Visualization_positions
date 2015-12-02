import json
import webapp2
import numpy as np

from itertools import chain
from logging import error, info

from location_service.utils.decorators import jsonify


class UsersHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self._user_list= self.app.config.get('user_list')

    def _bad_request(self):
        """
        Sent a 400 error as response.
        :return: None
        """
        self.response.set_status(400)
        self.response.write('ERROR 400: bad request')

    @jsonify
    def _user(self):
        return {
                "availableOptionsforUser": [{"id": identifiant} for identifiant in self._user_list],
                "selectedOptionforUser": {"id":1055}
                }

    def post(self):
        self.get()

    def get(self):
        self.response.write(self._user())