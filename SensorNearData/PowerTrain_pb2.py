# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SensorNearData/PowerTrain.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from SensorNearData import header_pb2 as SensorNearData_dot_header__pb2
from SensorNearData import SensorStates_pb2 as SensorNearData_dot_SensorStates__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fSensorNearData/PowerTrain.proto\x12\x0eSensorNearData\x1a\x1bSensorNearData/header.proto\x1a!SensorNearData/SensorStates.proto\"\xaa\x04\n\nPowerTrain\x12&\n\x06header\x18\x01 \x01(\x0b\x32\x16.SensorNearData.Header\x12-\n\x04\x65rrs\x18\x03 \x01(\x0b\x32\x1f.SensorNearData.PowerTrain.Errs\x12\x33\n\x07signals\x18\x04 \x01(\x0b\x32\".SensorNearData.PowerTrain.Signals\x1a\x81\x01\n\x04\x45rrs\x12\x37\n\x04gear\x18\x01 \x01(\x0e\x32\x1c.SensorNearData.SensorStates:\x0bSTATE_FAULT\x12@\n\rgas_pedal_pos\x18\x02 \x01(\x0e\x32\x1c.SensorNearData.SensorStates:\x0bSTATE_FAULT\x1aZ\n\x07Signals\x12\x18\n\rgas_pedal_pos\x18\x03 \x01(\x02:\x01\x30\x12\x35\n\x04gear\x18\x07 \x01(\x0e\x32\x1f.SensorNearData.PowerTrain.Gear:\x06GEAR_N\"\xaf\x01\n\x04Gear\x12\n\n\x06GEAR_N\x10\x00\x12\n\n\x06GEAR_R\x10\x01\x12\n\n\x06GEAR_P\x10\x02\x12\n\n\x06GEAR_D\x10\x03\x12\x0b\n\x07GEAR_D1\x10\x04\x12\x0b\n\x07GEAR_D2\x10\x05\x12\x0b\n\x07GEAR_D3\x10\x06\x12\x0b\n\x07GEAR_D4\x10\x07\x12\x0b\n\x07GEAR_D5\x10\x08\x12\x0b\n\x07GEAR_D6\x10\t\x12\x0b\n\x07GEAR_D7\x10\n\x12\x0c\n\x08GEAR_SNA\x10\x0b\x12\x0e\n\nGEAR_UNDEF\x10\x0c')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'SensorNearData.PowerTrain_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _POWERTRAIN._serialized_start=116
  _POWERTRAIN._serialized_end=670
  _POWERTRAIN_ERRS._serialized_start=271
  _POWERTRAIN_ERRS._serialized_end=400
  _POWERTRAIN_SIGNALS._serialized_start=402
  _POWERTRAIN_SIGNALS._serialized_end=492
  _POWERTRAIN_GEAR._serialized_start=495
  _POWERTRAIN_GEAR._serialized_end=670
# @@protoc_insertion_point(module_scope)
