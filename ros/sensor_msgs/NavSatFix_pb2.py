# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ros/sensor_msgs/NavSatFix.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ros.sensor_msgs import NavSatStatus_pb2 as ros_dot_sensor__msgs_dot_NavSatStatus__pb2
from ros.std_msgs import Header_pb2 as ros_dot_std__msgs_dot_Header__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fros/sensor_msgs/NavSatFix.proto\x12\x0fros.sensor_msgs\x1a\"ros/sensor_msgs/NavSatStatus.proto\x1a\x19ros/std_msgs/Header.proto\"\xd6\x01\n\tNavSatFix\x12$\n\x06header\x18\x01 \x01(\x0b\x32\x14.ros.std_msgs.Header\x12-\n\x06status\x18\x02 \x01(\x0b\x32\x1d.ros.sensor_msgs.NavSatStatus\x12\x10\n\x08latitude\x18\x03 \x01(\x01\x12\x11\n\tlongitude\x18\x04 \x01(\x01\x12\x10\n\x08\x61ltitude\x18\x05 \x01(\x01\x12\x1b\n\x13position_covariance\x18\x06 \x03(\x01\x12 \n\x18position_covariance_type\x18\x07 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ros.sensor_msgs.NavSatFix_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NAVSATFIX._serialized_start=116
  _NAVSATFIX._serialized_end=330
# @@protoc_insertion_point(module_scope)
