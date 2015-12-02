import json
import webapp2
import numpy as np
import datetime as dt

from time import time
from itertools import chain
from logging import error, info

from location_service.utils.decorators import jsonify
from location_service import USER_ID, ORDINAL_DATE, LATITUDE, LONGITUDE, ACCURACY, POI, TIME_STAMP, distance


class LocationHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self._locations = self.app.config.get('locations')
        self._locations_iterator_random = self.app.config.get('locations_iterator_random')
        self._sorted_user_date_pairs = self.app.config.get('sorted_user_date_pairs')
        self._poi = self.app.config.get('POI')

    def _bad_request(self):
        """
        Sent a 400 error as response.
        :return: None
        """
        self.response.set_status(400)
        self.response.write('ERROR 400: bad request')

    @jsonify
    def _get_locations(self, uid, d):
        locations_index = np.all(self._locations[:, (USER_ID, ORDINAL_DATE)] == (int(uid), d), axis=1)
        user_date_locations = self._locations[locations_index, :]
        locations = user_date_locations[:, (LATITUDE, LONGITUDE, ACCURACY, POI,TIME_STAMP)]
        locindex= list(a for a in locations[:,4])
        sorted_locindex = sorted(range(len(locindex)), key=lambda k: locindex[0])
        for i in range(locations.shape[0]):
            locations[i,4]=sorted_locindex[i]
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
            
        arrow=[]
        alpha1=6.0/9.0
        alpha2=4.0/9.0
        for i in range(locations.shape[0]-1):
            if distance(np.array([[locations[i,0],locations[i,1]]]),np.array([[locations[i+1,0],locations[i+1,1]]]))>50:
                a0=alpha1*locations[i,0]+(1.0-alpha1)*locations[i+1,0]
                a1=alpha1*locations[i,1]+(1.0-alpha1)*locations[i+1,1]
                a2=alpha2*locations[i,0]+(1.0-alpha2)*locations[i+1,0]
                a3=alpha2*locations[i,1]+(1.0-alpha2)*locations[i+1,1]
                arrow.append((a0,a1,a2,a3))
        datedisp=dt.datetime.fromordinal(int(d))
        week=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
        month=['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
        datetodisp=week[datedisp.weekday()]+" "+str(datedisp.day)+" "+month[datedisp.month-1]+" "+str(datedisp.year)

        if arrow!=[]:

            return {"user": uid,
                    "date": d,
                    "datedisp": datetodisp,
                    "locations": [{"latitude": latitude, 
                                   "longitude": longitude,
                                   "accuracy": accuracy,
                                   "poi_id": poi_id,
                                   "position_daily_id": position_daily_id} for latitude, longitude, accuracy, poi_id, position_daily_id in locations],
                    "POI": [{"poi_id": poi_id,
                            "lat_poi": lat_poi,
                            "long_poi": long_poi,
                            "acc_poi": acc_poi
                            } for poi_id,lat_poi,long_poi,acc_poi in poi_user],
                    "arrow": [{"lat1": lat1,
                            "long1": long1,
                            "lat2": lat2,
                            "long2": long2
                            } for lat1, long1, lat2, long2 in arrow]
                                   
                    }
        else:
            return {"user": uid,
                    "date": d,
                    "datedisp": datetodisp,
                    "locations": [{"latitude": latitude, 
                                   "longitude": longitude,
                                   "accuracy": accuracy,
                                   "poi_id": poi_id,
                                   "position_daily_id": position_daily_id} for latitude, longitude, accuracy, poi_id, position_daily_id in locations],
                    "POI": [{"poi_id": poi_id,
                            "lat_poi": lat_poi,
                            "long_poi": long_poi,
                            "acc_poi": acc_poi
                            } for poi_id,lat_poi,long_poi,acc_poi in poi_user],
                    "arrow": []
                    }

    def post(self):
        self.get()

    def get(self):
        try:
            next=int(self.request.get('next', default_value=0))
            if next==0:
                user_id = self.request.get('user_id', default_value=None)
                fromlist=int(self.request.get('fromlist', default_value=0))
                if not (fromlist):
                    print('coucou')
                    str_date = self.request.get('date', default_value=None)
                    year, month, day = (int(c) for c in str_date.split('-'))
                    ordinal_date = dt.date(year=year, month=month, day=day).toordinal()
                else:
                    print("hello")
                    ordinal_date=int(self.request.get('date', default_value=None))

            else:
                last_user_id = int(self.request.get('last_user_id'))
                last_date = int(self.request.get('last_date'))
                id_pair=self._sorted_user_date_pairs.index((last_user_id,last_date))
                user_id=self._sorted_user_date_pairs[id_pair+next][0]
                ordinal_date =self._sorted_user_date_pairs[id_pair+next][1]

        except AttributeError:
            ordinal_date = None

        if user_id is None or ordinal_date is None:
            # Get the next (user,date) pair to be displayed
            user_id, ordinal_date = self._locations_iterator_random.next()
            error(ordinal_date)

        self.response.write(self._get_locations(user_id, ordinal_date))