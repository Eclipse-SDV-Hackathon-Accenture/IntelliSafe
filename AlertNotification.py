import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import SensorNearData.Alert_pb2 as Alert_pb2
import geopy.distance
import pandas as pd

curr_latitude, curr_longitude = 48.12, 11.60
geo_locations = []

is_reported = []

def callback(topic_name, alert, time):
    print(type(alert))
    print(alert)
    print('Receciving Subscribed Messages')
    if alert.is_panic_braking and alert.car_id not in is_reported :
        geo_locations.append([alert.car_id, alert.latitude, alert.longitude , geopy.distance.geodesic((alert.latitude, alert.longitude ), (curr_latitude, curr_longitude))])
        is_reported.append(alert.car_id)
    df = pd.DataFrame(geo_locations, columns=['id', 'lat', 'lon', "sizes"])
    df.to_csv('out.csv')
    
ecal_core.initialize([], "InteliSafe")
sub = ProtoSubscriber("AlertNotification", Alert_pb2.Alert)
sub.set_callback(callback)
while ecal_core.ok():
    time.sleep(10)
ecal_core.finalize()