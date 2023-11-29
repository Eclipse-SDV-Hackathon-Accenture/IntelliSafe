import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import ros.sensor_msgs.CompressedImage_pb2 as CompressedImage_pb2

def callback(topic_name, compressed_image, time):
    print("Received CompressedImage:")
    print("Format:", compressed_image.format)
    print("Data Length:", len(compressed_image.data[7:]))

if __name__ == "__main__":

  ecal_core.initialize([], "CompressedImageSubscriber")
  sub = ProtoSubscriber("ROSFrontCenterImage", CompressedImage_pb2.CompressedImage)
  sub.set_callback(callback)

  while ecal_core.ok():
      time.sleep(1)
  ecal_core.finalize()
    
