import cv2
import torch
import numpy as np
import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import SensorNearData.VehicleDynamics_pb2 as VehicleDynamics_pb2


def callback(topic_name, vehicle_dynamics, time):
    print('Rececived Vehicle Dynamics')
    print(vehicle_dynamics.signals.speed)

ecal_core.initialize([], "InteliSafe")
sub = ProtoSubscriber("VehicleDynamicsInPb", VehicleDynamics_pb2.VehicleDynamics)
sub.set_callback(callback)
cv2.destroyAllWindows()
while ecal_core.ok():
    time.sleep(10)
ecal_core.finalize()
