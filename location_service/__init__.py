import numpy as np

USER_ID, LOCATION_ID, LATITUDE, LONGITUDE, ACCURACY, ACTIVITY_CODE, ACTIVITY_CONFIDENCE, ORDINAL_DATE, TIME_STAMP, ECEF_X, ECEF_Y, ECEF_Z, POI, WEEKDAY, DAILY_TIME_STAMP, NB_STILL_LOCATIONS,POSITION_DAILY_ID = range(17)

def distance(origins, destinations):
    """
    Compute the great-circle distance for two series of <lat,lon> coordinates.

    :param origins: a numpy array of shape (n,2) that contains a <lat,lon> pair per line.
    :param destinations: a numpy array of shape (n,2) that contains a <lat,lon> pair per line.
    :return: D a numpy array of shape (n,) such that D[n] = dist(origins[n,:], destinations[n,:])
    """
    if type(origins) != np.ndarray:
        origins = np.array(origins, ndmin=2)
    if type(destinations) != np.ndarray:
        destinations = np.array(destinations, ndmin=2)
    o = np.radians(origins)
    d = np.radians(destinations)
    delta = d - o
    a = np.square(np.sin(delta[:, 0] / 2)) + np.cos(o[:, 0]) * np.cos(d[:, 0]) * np.square(np.sin(delta[:, 1] / 2))
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371000 * c