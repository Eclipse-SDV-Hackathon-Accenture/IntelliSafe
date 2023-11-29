import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import SensorNearData.Alert_pb2 as Alert_pb2
import geopy.distance

curr_latitude, curr_longitude = 48.12, 11.60

def callback(topic_name, alert, time):
    print(type(alert))
    print('Receciving Subscribed Messages')
    # if alert.is_panic_braking:
    #     print(f"Probabale collision ahead at latitude {alert.latitude} and longitude {alert.longitude} approximate {geopy.distance.geodesic((alert.latitude, alert.longitude ), (curr_latitude, curr_longitude))}.km")

ecal_core.initialize([], "InteliSafe")
sub = ProtoSubscriber("AlertNotification", Alert_pb2.Alert)
sub.set_callback(callback)
while ecal_core.ok():
    time.sleep(10)
ecal_core.finalize()