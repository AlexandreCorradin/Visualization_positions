import json
import webapp2
import numpy as np
import datetime as dt

from time import time
from itertools import chain
from logging import error, info

from location_service.utils.decorators import jsonify
from location_service import USER_ID, ORDINAL_DATE, LATITUDE, LONGITUDE, ACCURACY, POI, TIME_STAMP, distance


class POIHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self._poi = self.app.config.get('POI')

    def _bad_request(self):
        """
        Sent a 400 error as response.
        :return: None
        """
        self.response.set_status(400)
        self.response.write('ERROR 400: bad request')

    @jsonify
    def _get_locations(self, uid):
        dict_poi=self._poi[int(uid)]
        n_poi=len(dict_poi)
        poi_user=np.zeros((n_poi,4))
        for z in range(n_poi):
            latlg0=dict_poi[z]['WGS84'][0]
            for i in range(3):
                lati=dict_poi[z]['WGS84'][i][0]
                longi=dict_poi[z]['WGS84'][i][1]
                if (lati!=latlg0[0] and longi!=latlg0[1]):
                    latpoi=(lati+latlg0[0])/2.0
                    longpoi=(longi+latlg0[1])/2.0
                    accpoi=distance(np.array([[lati,longi]]),np.array([[latlg0[0],latlg0[1]]]))/2.0
                    break
            poi_user[z,:]=np.array([z,latpoi,longpoi,accpoi])
            
        return {"POI": [{"poi_id": poi_id,
                        "lat_poi": lat_poi,
                        "long_poi": long_poi,
                        "acc_poi": acc_poi
                        } for poi_id,lat_poi,long_poi,acc_poi in poi_user]
                }

    def post(self):
        self.get()

    def get(self):
        user_id = self.request.get('user_id', default_value=None)
        self.response.write(self._get_locations(user_id))