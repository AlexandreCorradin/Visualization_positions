import json
import webapp2
import numpy as np
import datetime as dt

from time import time
from itertools import chain
from logging import error, info

from location_service.utils.decorators import jsonify

from location_service import USER_ID,LATITUDE, LONGITUDE,ORDINAL_DATE


class DateZoneHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self._locations = self.app.config.get('locations')

    def _bad_request(self):
        """
        Sent a 400 error as response.
        :return: None
        """
        self.response.set_status(400)
        self.response.write('ERROR 400: bad request')

    def _inside(self,lim,lat,longi):
        if lat>lim[0,0] and lat<lim[0,1] and longi>lim[1,0] and longi<lim[1,1]:
            return 1
        else:
            return 0



    @jsonify
    def _get_dates(self, uid,lim):

        locations_index = np.transpose(self._locations[:, USER_ID] == int(uid))
        date_locations = self._locations[locations_index, :]
        user_locations = date_locations[:, (LATITUDE, LONGITUDE,ORDINAL_DATE)]
        user_location_size=np.shape(user_locations)
        datedanszone=[]
        for i in range(int(user_location_size[0])):
            contains= self._inside(lim,user_locations[i,0],user_locations[i,1])
            if contains:
                datedanszone.append(user_locations[i,2])
        datedanszone=list(set(datedanszone))

        if len(datedanszone)==0:
            return {}

        datematrix=np.chararray((len(datedanszone),2),itemsize=30)
        week=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
        month=['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
        i=0
        for d in datedanszone:
            datematrix[i,0]=int(d)
            datedisp=dt.datetime.fromordinal(int(d))
            datematrix[i,1]=week[datedisp.weekday()]+" "+str(datedisp.day)+" "+month[datedisp.month-1]+" "+str(datedisp.year)
            i=i+1
        
        return {
                "availableOptionsForDate": [{"date":d,"datedisp":dd} for d,dd in datematrix ],
                "selectedOptionfordate": {"date":datedanszone[0]}
                }

    def post(self):
        self.get()

    def get(self):
        user_id = self.request.get('user_id', default_value=None)
        p=[]
        for i in range(4):
            l1=float(self.request.get('p'+str(i)+'lat', default_value=None))
            l2=float(self.request.get('p'+str(i)+'long', default_value=None))
            p.append((l1,l2))
        p=np.array([(a, b) for (a,b) in p])
        lim=np.zeros((2,2))
        m=np.min(p,axis=0)
        M=np.max(p,axis=0)
        lim[0,0]=m[0] #lat min
        lim[0,1]=M[0]
        lim[1,0]=m[1]
        lim[1,1]=M[1]
        self.response.write(self._get_dates(user_id,lim))