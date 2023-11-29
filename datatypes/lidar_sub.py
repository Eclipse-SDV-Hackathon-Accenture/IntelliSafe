import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
from ros.sensor_msgs import PointCloud2_pb2

def callback(topic_name, point_cloud, time):
    print("Received PointCloud2:")
    print("Header:", point_cloud.header)
    print("Height:", point_cloud.height)
    print("Width:", point_cloud.width)
    print("Fields:", point_cloud.fields)
    print("Is Big Endian:", point_cloud.is_bigendian)
    print("Point Step:", point_cloud.point_step)
    print("Row Step:", point_cloud.row_step)
    print("Data Length:", len(point_cloud.data))
    print("Is Dense:", point_cloud.is_dense)


def main():
    ecal_core.initialize([], "PointCloud2Subscriber")
    ecal_core.set_process_state(1, 1, "I feel good")
    sub = ProtoSubscriber("ROSVLS128CenterCenterRoof", PointCloud2_pb2.PointCloud2)
    sub.set_callback(callback)

    while ecal_core.ok():
        time.sleep(1)  

    ecal_core.finalize()

if __name__ == "__main__":
    main()
