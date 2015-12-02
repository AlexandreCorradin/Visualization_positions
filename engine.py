import logging
import webapp2
import numpy as np
import joblib as jb
import random as rd

from location_service import USER_ID, ORDINAL_DATE,TIME_STAMP
from location_service.handlers.location_handler import LocationHandler
from location_service.handlers.users_handler import UsersHandler
from location_service.handlers.date_handler import DateHandler
from location_service.handlers.date_zone_handler import DateZoneHandler
from location_service.handlers.POI_user_handler import POIHandler

try:
  logging.getLogger().setLevel(logging.DEBUG)
  L = np.load('./locations_matrix.npy')
  user_date_pairs = set(tuple(line) for line in L[:,(USER_ID, ORDINAL_DATE)])
  sorted_user_date_pairs = sorted(user_date_pairs, key=lambda element: (element[0], element[1]))
  
  date_as_user_func={}
  user_list=[]
  current_u=-1
  for ud in sorted_user_date_pairs:
    if current_u!=ud[0]:
      current_u=ud[0]
      date_as_user_func[current_u]=[]
      user_list.append(current_u)
    date_as_user_func[current_u].append(ud[1])
  
  user_date_pairs=list(user_date_pairs) 
  rd.shuffle(user_date_pairs)
  locations_iterator_random = iter(user_date_pairs)
  POI=jb.load('poi_per_user.jbl')


except Exception, e:
    locations = None
    logging.error('Failed to retrieve the locations, error is %s', repr(e))
finally:
    routes = [('/', LocationHandler),
              ('/users',UsersHandler),
              ('/date',DateHandler),
              ('/dateingivenzone',DateZoneHandler),
              ('/POI_given_user',POIHandler)]
    application = webapp2.WSGIApplication(routes=routes,
                                          debug=True,
                                          config={'locations': L,
                                                  'locations_iterator_random': locations_iterator_random,
                                                  'sorted_user_date_pairs': sorted_user_date_pairs,
                                                  'date_as_user_func': date_as_user_func,
                                                  'user_list': user_list,
                                                  'POI':POI })