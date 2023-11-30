import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import SensorNearData.Alert_pb2 as Alert_pb2
import geopy.distance
import pandas as pd

curr_latitude, curr_longitude = 48.12, 11.60
geo_locations = []

is_reported = []

def callback(topic_name, alerts, time):
    print(type(alerts))
    print(alerts.alert[0])
    print('Receciving Subscribed Messages')
    if alerts.alert[0].is_panic_braking and alerts.alert[0].car_id not in is_reported :
        geo_locations.append([alerts.alert[0].car_id, alerts.alert[0].latitude, alerts.alert[0].longitude , geopy.distance.geodesic((alerts.alert[0].latitude, alerts.alert[0].longitude ), (curr_latitude, curr_longitude))])
        is_reported.append(alerts.alert[0].car_id)
    df = pd.DataFrame(geo_locations, columns=['id', 'lat', 'lon', "sizes"])
    df.to_csv('out.csv')
    
ecal_core.initialize([], "InteliSafe")
sub = ProtoSubscriber("AlertNotification", Alert_pb2.Alerts)
sub.set_callback(callback)
while ecal_core.ok():
    time.sleep(10)
ecal_core.finalize()