from typing import Any
import cv2
import torch
import numpy as np
import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import ros.sensor_msgs.CompressedImage_pb2 as CompressedImage_pb2
from PIL import Image
import io
import matplotlib.pyplot as plt
import cv2
import torch
import numpy as np
import matplotlib.image as mpimg
import os
from ecal.core.publisher import ProtoPublisher
import subprocess
from brakeassist import BrakeAssist
import SensorNearData.VehicleDynamics_pb2 as VehicleDynamics_pb2
import SensorNearData.Brake_pb2 as Brake_pb2
import ros.sensor_msgs.NavSatFix_pb2 as NavSatFix_pb2
import SensorNearData.Alert_pb2 as Alert_pb2

# Suppress OpenMP related warning
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

class Attributes():
    def __init__(self):
        self.car_id = 'Car2'
        self.latitude = 0.0
        self.longitude = 0.0
        self.is_panic_braking = False
        self.timestamp = int(time.time())

def update_alert():
    alert_.car_id = attr.car_id
    alert_.timestamp = int(time.time())
    alert_.latitude = attr.latitude
    alert_.longitude = attr.longitude
    alert_.is_panic_braking = attr.is_panic_braking

def callback_image(topic_name, compressed_image, time):
    img = mpimg.imread(io.BytesIO(compressed_image.data), format=compressed_image.format)
    processor.process_video(img)
    cv2.waitKey(1)

def callback_speed(topic_name, vehicle_dynamics, time):
    processor.speed = vehicle_dynamics.signals.speed


def callback_gps(topic_name, gps, time):
    # if alert.is_panic_braking:
    attr.latitude = gps.latitude
    attr.longitude = gps.longitude
    update_alert()

    pub.send(alert_)
    # else:
    #     alert.latitude = 0.0
    #     alert.longitude = 0.0
def callback_brake(topic_name, brake, time):
    attr.is_panic_braking = brake.signals.is_panic_braking
    update_alert()

ecal_core.initialize([], "IntelliSafe")
sub_image = ProtoSubscriber("ROSFrontCenterImage", CompressedImage_pb2.CompressedImage)
processor = BrakeAssist('yolov5s.pt', '20231128-1516-56.7048286.mp4', 'intelli_safe_output.mp4')
attr = Attributes()
processor.video.release()
processor.output.release()
cv2.destroyAllWindows()

sub_gps = ProtoSubscriber("ROSGlobalPosition", NavSatFix_pb2.NavSatFix)
sub_speed = ProtoSubscriber("VehicleDynamicsInPb", VehicleDynamics_pb2.VehicleDynamics)
sub_brake = ProtoSubscriber("BrakeInPb", Brake_pb2.Brake)

# alerts = Alert_pb2.Alerts()
alert_ = Alert_pb2.Alert()
alert_.car_id = attr.car_id
alert_.timestamp = int(time.time())
alert_.latitude = attr.latitude
alert_.longitude = attr.longitude
alert_.is_panic_braking = attr.timestamp

pub = ProtoPublisher("AlertNotification", Alert_pb2.Alert)
sub_brake.set_callback(callback_brake)
sub_gps.set_callback(callback_gps)
sub_speed.set_callback(callback_speed)
sub_image.set_callback(callback_image)


# alerts.alert.extend([alert_])

while ecal_core.ok():
    time.sleep(1)
ecal_core.finalize()
