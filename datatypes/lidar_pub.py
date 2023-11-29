import time
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
from ros.sensor_msgs import PointCloud2_pb2
from ros.std_msgs import Header_pb2

if __name__ == "__main__":
    ecal_core.initialize([], "PointCloud2Publisher")
    ecal_core.set_process_state(1, 1, "I feel good")

    pub = ProtoPublisher("ROSVLS128CenterCenterRoof", PointCloud2_pb2.PointCloud2)
    point_cloud = PointCloud2_pb2.PointCloud2()
    point_cloud.height = 1
    point_cloud.width = 100
    field = point_cloud.fields.add()
    field.name = "x"
    field.offset = 0
    field.datatype = 7 
    field.count = 1

    point_cloud.is_bigendian = False
    point_cloud.point_step = 4  
    point_cloud.row_step = point_cloud.point_step * point_cloud.width
    point_cloud.is_dense = True

    point_cloud.data = b'abcd'

    while ecal_core.ok():
        pub.send(point_cloud)
        time.sleep(1)
    ecal_core.finalize()
