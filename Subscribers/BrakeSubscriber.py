import cv2
import torch
import numpy as np
import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import SensorNearData.Brake_pb2 as Brake_pb2


def callback(topic_name, brake, time):
    print('Rececived Nav Sat Fix')
    print(brake.signals.is_panic_braking)

ecal_core.initialize([], "InteliSafe")
sub = ProtoSubscriber("BrakeInPb", Brake_pb2.Brake)
sub.set_callback(callback)
cv2.destroyAllWindows()
while ecal_core.ok():
    time.sleep(10)
ecal_core.finalize()