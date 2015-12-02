import json
import webapp2
import numpy as np
import datetime as dt

from time import time
from itertools import chain
from logging import error, info

from location_service.utils.decorators import jsonify
from location_service import USER_ID, ORDINAL_DATE, LATITUDE, LONGITUDE, ACCURACY, POI

class LocationHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self._locations = self.app.config.get('locations')
        self._locations_iterator = self.app.config.get('locations_iterator')

    def _bad_request(self):
        """
        Sent a 400 error as response.
        :return: None
        """
        self.response.set_status(400)
        self.response.write('ERROR 400: bad request')
        self._librato_queue.add('routing.bad_request', 1, source=CURNT_APP_NAME)


    def _locations(self, user_id, date):


    def _next_locations(self, way_points, motor_vehicle, list_vertices=False):


    def post(self):
        self.get()

    @jsonify
    def get(self):
        try:
            user_id = self.request.get(parameter_name, default_value=None)
            str_date = self.request.get(parameter_name, default_value=None)
            year, month, day = str_date.split('-') 
            ordinal_date = dt.date(year=year, month=month, day=day).toordinal()
        except AttributeError:
            ordinal_date = None

        if user_id is None or ordinal_date is None:
            # Get the next (user,date) pair to be displayed
            user_id, ordinal_date = locations_iterator.next()

        locations_index = np.all(self._locations[:, (USER_ID, ORDINAL_DATE)] == (user_id, ordinal_date), axis=1)
        user_date_locations = self._locations[locations_index, (LATITUDE, LONGITUDE, ACCURACY, POI)]

        return {"user": user_id,
                "date": ordinal_date,
                "locations": [tuple(location) for location in user_date_locations]}
