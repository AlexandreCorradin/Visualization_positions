import json
import webapp2
import numpy as np
import datetime as dt

from time import time
from itertools import chain
from logging import error, info

from location_service.utils.decorators import jsonify


class DateHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self._date_as_user_func = self.app.config.get('date_as_user_func')

    def _bad_request(self):
        """
        Sent a 400 error as response.
        :return: None
        """
        self.response.set_status(400)
        self.response.write('ERROR 400: bad request')

    @jsonify
    def _get_dates(self, uid):
        dateui=self._date_as_user_func[int(uid)]
        datematrix=np.chararray((len(dateui),2),itemsize=30)
        week=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
        month=['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
        i=0
        for d in dateui:
            datematrix[i,0]=int(d)
            datedisp=dt.datetime.fromordinal(int(d))
            datematrix[i,1]=week[datedisp.weekday()]+" "+str(datedisp.day)+" "+month[datedisp.month-1]+" "+str(datedisp.year)
            i=i+1
        
        return {
                "availableOptionsForDate": [{"date":d,"datedisp":dd} for d,dd in datematrix ],
                "selectedOptionfordate": {"date":dateui[0]}
                }

    def post(self):
        self.get()

    def get(self):
        user_id = self.request.get('user_id', default_value=None)
        self.response.write(self._get_dates(user_id))