# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SensorNearData/Brake.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from SensorNearData import header_pb2 as SensorNearData_dot_header__pb2
from SensorNearData import SensorStates_pb2 as SensorNearData_dot_SensorStates__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aSensorNearData/Brake.proto\x12\x0eSensorNearData\x1a\x1bSensorNearData/header.proto\x1a!SensorNearData/SensorStates.proto\"\xe3\x02\n\x05\x42rake\x12&\n\x06header\x18\x01 \x01(\x0b\x32\x16.SensorNearData.Header\x12(\n\x04\x65rrs\x18\x03 \x01(\x0b\x32\x1a.SensorNearData.Brake.Errs\x12.\n\x07signals\x18\x04 \x01(\x0b\x32\x1d.SensorNearData.Brake.Signals\x1a\x8f\x01\n\x04\x45rrs\x12\x42\n\x0f\x64river_pressure\x18\x01 \x01(\x0e\x32\x1c.SensorNearData.SensorStates:\x0bSTATE_FAULT\x12\x43\n\x10is_brake_applied\x18\x02 \x01(\x0e\x32\x1c.SensorNearData.SensorStates:\x0bSTATE_FAULT\x1a\x46\n\x07Signals\x12\x1a\n\x0f\x64river_pressure\x18\x02 \x01(\x02:\x01\x30\x12\x1f\n\x10is_brake_applied\x18\x03 \x01(\x08:\x05\x66\x61lse')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'SensorNearData.Brake_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BRAKE._serialized_start=111
  _BRAKE._serialized_end=466
  _BRAKE_ERRS._serialized_start=251
  _BRAKE_ERRS._serialized_end=394
  _BRAKE_SIGNALS._serialized_start=396
  _BRAKE_SIGNALS._serialized_end=466
# @@protoc_insertion_point(module_scope)