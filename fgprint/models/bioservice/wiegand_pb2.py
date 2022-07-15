# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wiegand.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import device_pb2 as device__pb2
import err_pb2 as err__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='wiegand.proto',
  package='wiegand',
  syntax='proto3',
  serialized_options=_b('\n\032com.supremainc.sdk.wiegandP\001Z\027biostar/service/wiegand'),
  serialized_pb=_b('\n\rwiegand.proto\x12\x07wiegand\x1a\x0c\x64\x65vice.proto\x1a\terr.proto\"Z\n\x0bParityField\x12\x11\n\tparityPos\x18\x01 \x01(\r\x12*\n\nparityType\x18\x02 \x01(\x0e\x32\x16.wiegand.WiegandParity\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\"o\n\rWiegandFormat\x12\x10\n\x08\x66ormatID\x18\x01 \x01(\r\x12\x0e\n\x06length\x18\x02 \x01(\r\x12\x10\n\x08IDFields\x18\x03 \x03(\x0c\x12*\n\x0cparityFields\x18\x04 \x03(\x0b\x32\x14.wiegand.ParityField\"\xa7\x02\n\rWiegandConfig\x12\"\n\x04mode\x18\x01 \x01(\x0e\x32\x14.wiegand.WiegandMode\x12\x18\n\x10useWiegandBypass\x18\x02 \x01(\x08\x12\x13\n\x0buseFailCode\x18\x03 \x01(\x08\x12\x10\n\x08\x66\x61ilCode\x18\x04 \x01(\r\x12\x15\n\routPulseWidth\x18\x05 \x01(\r\x12\x18\n\x10outPulseInterval\x18\x06 \x01(\r\x12\'\n\x07\x66ormats\x18\x07 \x03(\x0b\x32\x16.wiegand.WiegandFormat\x12,\n\x0cslaveFormats\x18\x08 \x03(\x0b\x32\x16.wiegand.WiegandFormat\x12)\n\tCSNFormat\x18\t \x01(\x0b\x32\x16.wiegand.WiegandFormat\"$\n\x10GetConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\";\n\x11GetConfigResponse\x12&\n\x06\x63onfig\x18\x01 \x01(\x0b\x32\x16.wiegand.WiegandConfig\"L\n\x10SetConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12&\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x16.wiegand.WiegandConfig\"\x13\n\x11SetConfigResponse\"R\n\x15SetConfigMultiRequest\x12\x11\n\tdeviceIDs\x18\x01 \x03(\r\x12&\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x16.wiegand.WiegandConfig\"B\n\x16SetConfigMultiResponse\x12(\n\x0c\x64\x65viceErrors\x18\x01 \x03(\x0b\x32\x12.err.ErrorResponse\"\\\n\x12WiegandTamperInput\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0c\n\x04port\x18\x02 \x01(\r\x12&\n\nswitchType\x18\x03 \x01(\x0e\x32\x12.device.SwitchType\"/\n\rWiegandOutput\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0c\n\x04port\x18\x02 \x01(\r\"\xe3\x01\n\x11WiegandDeviceInfo\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x30\n\x0btamperInput\x18\x02 \x01(\x0b\x32\x1b.wiegand.WiegandTamperInput\x12,\n\x0credLEDOutput\x18\x03 \x01(\x0b\x32\x16.wiegand.WiegandOutput\x12.\n\x0egreenLEDOutput\x18\x04 \x01(\x0b\x32\x16.wiegand.WiegandOutput\x12,\n\x0c\x62uzzerOutput\x18\x05 \x01(\x0b\x32\x16.wiegand.WiegandOutput\"-\n\x13SearchDeviceRequest\x12\x16\n\x0eparentDeviceID\x18\x01 \x01(\r\"0\n\x14SearchDeviceResponse\x12\x18\n\x10wiegandDeviceIDs\x18\x01 \x03(\r\"[\n\x10SetDeviceRequest\x12\x16\n\x0eparentDeviceID\x18\x01 \x01(\r\x12/\n\x0b\x64\x65viceInfos\x18\x02 \x03(\x0b\x32\x1a.wiegand.WiegandDeviceInfo\"\x13\n\x11SetDeviceResponse\"*\n\x10GetDeviceRequest\x12\x16\n\x0eparentDeviceID\x18\x01 \x01(\r\"D\n\x11GetDeviceResponse\x12/\n\x0b\x64\x65viceInfos\x18\x01 \x03(\x0b\x32\x1a.wiegand.WiegandDeviceInfo*L\n\x0bWiegandMode\x12\x13\n\x0fWIEGAND_IN_ONLY\x10\x00\x12\x14\n\x10WIEGAND_OUT_ONLY\x10\x01\x12\x12\n\x0eWIEGAND_IN_OUT\x10\x02*Y\n\rWiegandParity\x12\x17\n\x13WIEGAND_PARITY_NONE\x10\x00\x12\x16\n\x12WIEGAND_PARITY_ODD\x10\x01\x12\x17\n\x13WIEGAND_PARITY_EVEN\x10\x02\x32\xb9\x03\n\x07Wiegand\x12\x42\n\tGetConfig\x12\x19.wiegand.GetConfigRequest\x1a\x1a.wiegand.GetConfigResponse\x12\x42\n\tSetConfig\x12\x19.wiegand.SetConfigRequest\x1a\x1a.wiegand.SetConfigResponse\x12Q\n\x0eSetConfigMulti\x12\x1e.wiegand.SetConfigMultiRequest\x1a\x1f.wiegand.SetConfigMultiResponse\x12K\n\x0cSearchDevice\x12\x1c.wiegand.SearchDeviceRequest\x1a\x1d.wiegand.SearchDeviceResponse\x12\x42\n\tSetDevice\x12\x19.wiegand.SetDeviceRequest\x1a\x1a.wiegand.SetDeviceResponse\x12\x42\n\tGetDevice\x12\x19.wiegand.GetDeviceRequest\x1a\x1a.wiegand.GetDeviceResponseB7\n\x1a\x63om.supremainc.sdk.wiegandP\x01Z\x17\x62iostar/service/wiegandb\x06proto3')
  ,
  dependencies=[device__pb2.DESCRIPTOR,err__pb2.DESCRIPTOR,])

_WIEGANDMODE = _descriptor.EnumDescriptor(
  name='WiegandMode',
  full_name='wiegand.WiegandMode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WIEGAND_IN_ONLY', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WIEGAND_OUT_ONLY', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WIEGAND_IN_OUT', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1602,
  serialized_end=1678,
)
_sym_db.RegisterEnumDescriptor(_WIEGANDMODE)

WiegandMode = enum_type_wrapper.EnumTypeWrapper(_WIEGANDMODE)
_WIEGANDPARITY = _descriptor.EnumDescriptor(
  name='WiegandParity',
  full_name='wiegand.WiegandParity',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WIEGAND_PARITY_NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WIEGAND_PARITY_ODD', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WIEGAND_PARITY_EVEN', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1680,
  serialized_end=1769,
)
_sym_db.RegisterEnumDescriptor(_WIEGANDPARITY)

WiegandParity = enum_type_wrapper.EnumTypeWrapper(_WIEGANDPARITY)
WIEGAND_IN_ONLY = 0
WIEGAND_OUT_ONLY = 1
WIEGAND_IN_OUT = 2
WIEGAND_PARITY_NONE = 0
WIEGAND_PARITY_ODD = 1
WIEGAND_PARITY_EVEN = 2



_PARITYFIELD = _descriptor.Descriptor(
  name='ParityField',
  full_name='wiegand.ParityField',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parityPos', full_name='wiegand.ParityField.parityPos', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parityType', full_name='wiegand.ParityField.parityType', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='wiegand.ParityField.data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=141,
)


_WIEGANDFORMAT = _descriptor.Descriptor(
  name='WiegandFormat',
  full_name='wiegand.WiegandFormat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='formatID', full_name='wiegand.WiegandFormat.formatID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='length', full_name='wiegand.WiegandFormat.length', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='IDFields', full_name='wiegand.WiegandFormat.IDFields', index=2,
      number=3, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parityFields', full_name='wiegand.WiegandFormat.parityFields', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=254,
)


_WIEGANDCONFIG = _descriptor.Descriptor(
  name='WiegandConfig',
  full_name='wiegand.WiegandConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mode', full_name='wiegand.WiegandConfig.mode', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='useWiegandBypass', full_name='wiegand.WiegandConfig.useWiegandBypass', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='useFailCode', full_name='wiegand.WiegandConfig.useFailCode', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='failCode', full_name='wiegand.WiegandConfig.failCode', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='outPulseWidth', full_name='wiegand.WiegandConfig.outPulseWidth', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='outPulseInterval', full_name='wiegand.WiegandConfig.outPulseInterval', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='formats', full_name='wiegand.WiegandConfig.formats', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slaveFormats', full_name='wiegand.WiegandConfig.slaveFormats', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='CSNFormat', full_name='wiegand.WiegandConfig.CSNFormat', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=257,
  serialized_end=552,
)


_GETCONFIGREQUEST = _descriptor.Descriptor(
  name='GetConfigRequest',
  full_name='wiegand.GetConfigRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='wiegand.GetConfigRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=554,
  serialized_end=590,
)


_GETCONFIGRESPONSE = _descriptor.Descriptor(
  name='GetConfigResponse',
  full_name='wiegand.GetConfigResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='wiegand.GetConfigResponse.config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=592,
  serialized_end=651,
)


_SETCONFIGREQUEST = _descriptor.Descriptor(
  name='SetConfigRequest',
  full_name='wiegand.SetConfigRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='wiegand.SetConfigRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='wiegand.SetConfigRequest.config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=653,
  serialized_end=729,
)


_SETCONFIGRESPONSE = _descriptor.Descriptor(
  name='SetConfigResponse',
  full_name='wiegand.SetConfigResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=731,
  serialized_end=750,
)


_SETCONFIGMULTIREQUEST = _descriptor.Descriptor(
  name='SetConfigMultiRequest',
  full_name='wiegand.SetConfigMultiRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceIDs', full_name='wiegand.SetConfigMultiRequest.deviceIDs', index=0,
      number=1, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='wiegand.SetConfigMultiRequest.config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=752,
  serialized_end=834,
)


_SETCONFIGMULTIRESPONSE = _descriptor.Descriptor(
  name='SetConfigMultiResponse',
  full_name='wiegand.SetConfigMultiResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceErrors', full_name='wiegand.SetConfigMultiResponse.deviceErrors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=836,
  serialized_end=902,
)


_WIEGANDTAMPERINPUT = _descriptor.Descriptor(
  name='WiegandTamperInput',
  full_name='wiegand.WiegandTamperInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='wiegand.WiegandTamperInput.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='wiegand.WiegandTamperInput.port', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='switchType', full_name='wiegand.WiegandTamperInput.switchType', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=904,
  serialized_end=996,
)


_WIEGANDOUTPUT = _descriptor.Descriptor(
  name='WiegandOutput',
  full_name='wiegand.WiegandOutput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='wiegand.WiegandOutput.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='wiegand.WiegandOutput.port', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=998,
  serialized_end=1045,
)


_WIEGANDDEVICEINFO = _descriptor.Descriptor(
  name='WiegandDeviceInfo',
  full_name='wiegand.WiegandDeviceInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='wiegand.WiegandDeviceInfo.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tamperInput', full_name='wiegand.WiegandDeviceInfo.tamperInput', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='redLEDOutput', full_name='wiegand.WiegandDeviceInfo.redLEDOutput', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='greenLEDOutput', full_name='wiegand.WiegandDeviceInfo.greenLEDOutput', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buzzerOutput', full_name='wiegand.WiegandDeviceInfo.buzzerOutput', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1048,
  serialized_end=1275,
)


_SEARCHDEVICEREQUEST = _descriptor.Descriptor(
  name='SearchDeviceRequest',
  full_name='wiegand.SearchDeviceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parentDeviceID', full_name='wiegand.SearchDeviceRequest.parentDeviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1277,
  serialized_end=1322,
)


_SEARCHDEVICERESPONSE = _descriptor.Descriptor(
  name='SearchDeviceResponse',
  full_name='wiegand.SearchDeviceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='wiegandDeviceIDs', full_name='wiegand.SearchDeviceResponse.wiegandDeviceIDs', index=0,
      number=1, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1324,
  serialized_end=1372,
)


_SETDEVICEREQUEST = _descriptor.Descriptor(
  name='SetDeviceRequest',
  full_name='wiegand.SetDeviceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parentDeviceID', full_name='wiegand.SetDeviceRequest.parentDeviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='deviceInfos', full_name='wiegand.SetDeviceRequest.deviceInfos', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1374,
  serialized_end=1465,
)


_SETDEVICERESPONSE = _descriptor.Descriptor(
  name='SetDeviceResponse',
  full_name='wiegand.SetDeviceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1467,
  serialized_end=1486,
)


_GETDEVICEREQUEST = _descriptor.Descriptor(
  name='GetDeviceRequest',
  full_name='wiegand.GetDeviceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parentDeviceID', full_name='wiegand.GetDeviceRequest.parentDeviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1488,
  serialized_end=1530,
)


_GETDEVICERESPONSE = _descriptor.Descriptor(
  name='GetDeviceResponse',
  full_name='wiegand.GetDeviceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceInfos', full_name='wiegand.GetDeviceResponse.deviceInfos', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1532,
  serialized_end=1600,
)

_PARITYFIELD.fields_by_name['parityType'].enum_type = _WIEGANDPARITY
_WIEGANDFORMAT.fields_by_name['parityFields'].message_type = _PARITYFIELD
_WIEGANDCONFIG.fields_by_name['mode'].enum_type = _WIEGANDMODE
_WIEGANDCONFIG.fields_by_name['formats'].message_type = _WIEGANDFORMAT
_WIEGANDCONFIG.fields_by_name['slaveFormats'].message_type = _WIEGANDFORMAT
_WIEGANDCONFIG.fields_by_name['CSNFormat'].message_type = _WIEGANDFORMAT
_GETCONFIGRESPONSE.fields_by_name['config'].message_type = _WIEGANDCONFIG
_SETCONFIGREQUEST.fields_by_name['config'].message_type = _WIEGANDCONFIG
_SETCONFIGMULTIREQUEST.fields_by_name['config'].message_type = _WIEGANDCONFIG
_SETCONFIGMULTIRESPONSE.fields_by_name['deviceErrors'].message_type = err__pb2._ERRORRESPONSE
_WIEGANDTAMPERINPUT.fields_by_name['switchType'].enum_type = device__pb2._SWITCHTYPE
_WIEGANDDEVICEINFO.fields_by_name['tamperInput'].message_type = _WIEGANDTAMPERINPUT
_WIEGANDDEVICEINFO.fields_by_name['redLEDOutput'].message_type = _WIEGANDOUTPUT
_WIEGANDDEVICEINFO.fields_by_name['greenLEDOutput'].message_type = _WIEGANDOUTPUT
_WIEGANDDEVICEINFO.fields_by_name['buzzerOutput'].message_type = _WIEGANDOUTPUT
_SETDEVICEREQUEST.fields_by_name['deviceInfos'].message_type = _WIEGANDDEVICEINFO
_GETDEVICERESPONSE.fields_by_name['deviceInfos'].message_type = _WIEGANDDEVICEINFO
DESCRIPTOR.message_types_by_name['ParityField'] = _PARITYFIELD
DESCRIPTOR.message_types_by_name['WiegandFormat'] = _WIEGANDFORMAT
DESCRIPTOR.message_types_by_name['WiegandConfig'] = _WIEGANDCONFIG
DESCRIPTOR.message_types_by_name['GetConfigRequest'] = _GETCONFIGREQUEST
DESCRIPTOR.message_types_by_name['GetConfigResponse'] = _GETCONFIGRESPONSE
DESCRIPTOR.message_types_by_name['SetConfigRequest'] = _SETCONFIGREQUEST
DESCRIPTOR.message_types_by_name['SetConfigResponse'] = _SETCONFIGRESPONSE
DESCRIPTOR.message_types_by_name['SetConfigMultiRequest'] = _SETCONFIGMULTIREQUEST
DESCRIPTOR.message_types_by_name['SetConfigMultiResponse'] = _SETCONFIGMULTIRESPONSE
DESCRIPTOR.message_types_by_name['WiegandTamperInput'] = _WIEGANDTAMPERINPUT
DESCRIPTOR.message_types_by_name['WiegandOutput'] = _WIEGANDOUTPUT
DESCRIPTOR.message_types_by_name['WiegandDeviceInfo'] = _WIEGANDDEVICEINFO
DESCRIPTOR.message_types_by_name['SearchDeviceRequest'] = _SEARCHDEVICEREQUEST
DESCRIPTOR.message_types_by_name['SearchDeviceResponse'] = _SEARCHDEVICERESPONSE
DESCRIPTOR.message_types_by_name['SetDeviceRequest'] = _SETDEVICEREQUEST
DESCRIPTOR.message_types_by_name['SetDeviceResponse'] = _SETDEVICERESPONSE
DESCRIPTOR.message_types_by_name['GetDeviceRequest'] = _GETDEVICEREQUEST
DESCRIPTOR.message_types_by_name['GetDeviceResponse'] = _GETDEVICERESPONSE
DESCRIPTOR.enum_types_by_name['WiegandMode'] = _WIEGANDMODE
DESCRIPTOR.enum_types_by_name['WiegandParity'] = _WIEGANDPARITY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ParityField = _reflection.GeneratedProtocolMessageType('ParityField', (_message.Message,), dict(
  DESCRIPTOR = _PARITYFIELD,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.ParityField)
  ))
_sym_db.RegisterMessage(ParityField)

WiegandFormat = _reflection.GeneratedProtocolMessageType('WiegandFormat', (_message.Message,), dict(
  DESCRIPTOR = _WIEGANDFORMAT,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.WiegandFormat)
  ))
_sym_db.RegisterMessage(WiegandFormat)

WiegandConfig = _reflection.GeneratedProtocolMessageType('WiegandConfig', (_message.Message,), dict(
  DESCRIPTOR = _WIEGANDCONFIG,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.WiegandConfig)
  ))
_sym_db.RegisterMessage(WiegandConfig)

GetConfigRequest = _reflection.GeneratedProtocolMessageType('GetConfigRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETCONFIGREQUEST,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.GetConfigRequest)
  ))
_sym_db.RegisterMessage(GetConfigRequest)

GetConfigResponse = _reflection.GeneratedProtocolMessageType('GetConfigResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETCONFIGRESPONSE,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.GetConfigResponse)
  ))
_sym_db.RegisterMessage(GetConfigResponse)

SetConfigRequest = _reflection.GeneratedProtocolMessageType('SetConfigRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETCONFIGREQUEST,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.SetConfigRequest)
  ))
_sym_db.RegisterMessage(SetConfigRequest)

SetConfigResponse = _reflection.GeneratedProtocolMessageType('SetConfigResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETCONFIGRESPONSE,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.SetConfigResponse)
  ))
_sym_db.RegisterMessage(SetConfigResponse)

SetConfigMultiRequest = _reflection.GeneratedProtocolMessageType('SetConfigMultiRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETCONFIGMULTIREQUEST,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.SetConfigMultiRequest)
  ))
_sym_db.RegisterMessage(SetConfigMultiRequest)

SetConfigMultiResponse = _reflection.GeneratedProtocolMessageType('SetConfigMultiResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETCONFIGMULTIRESPONSE,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.SetConfigMultiResponse)
  ))
_sym_db.RegisterMessage(SetConfigMultiResponse)

WiegandTamperInput = _reflection.GeneratedProtocolMessageType('WiegandTamperInput', (_message.Message,), dict(
  DESCRIPTOR = _WIEGANDTAMPERINPUT,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.WiegandTamperInput)
  ))
_sym_db.RegisterMessage(WiegandTamperInput)

WiegandOutput = _reflection.GeneratedProtocolMessageType('WiegandOutput', (_message.Message,), dict(
  DESCRIPTOR = _WIEGANDOUTPUT,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.WiegandOutput)
  ))
_sym_db.RegisterMessage(WiegandOutput)

WiegandDeviceInfo = _reflection.GeneratedProtocolMessageType('WiegandDeviceInfo', (_message.Message,), dict(
  DESCRIPTOR = _WIEGANDDEVICEINFO,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.WiegandDeviceInfo)
  ))
_sym_db.RegisterMessage(WiegandDeviceInfo)

SearchDeviceRequest = _reflection.GeneratedProtocolMessageType('SearchDeviceRequest', (_message.Message,), dict(
  DESCRIPTOR = _SEARCHDEVICEREQUEST,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.SearchDeviceRequest)
  ))
_sym_db.RegisterMessage(SearchDeviceRequest)

SearchDeviceResponse = _reflection.GeneratedProtocolMessageType('SearchDeviceResponse', (_message.Message,), dict(
  DESCRIPTOR = _SEARCHDEVICERESPONSE,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.SearchDeviceResponse)
  ))
_sym_db.RegisterMessage(SearchDeviceResponse)

SetDeviceRequest = _reflection.GeneratedProtocolMessageType('SetDeviceRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETDEVICEREQUEST,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.SetDeviceRequest)
  ))
_sym_db.RegisterMessage(SetDeviceRequest)

SetDeviceResponse = _reflection.GeneratedProtocolMessageType('SetDeviceResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETDEVICERESPONSE,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.SetDeviceResponse)
  ))
_sym_db.RegisterMessage(SetDeviceResponse)

GetDeviceRequest = _reflection.GeneratedProtocolMessageType('GetDeviceRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETDEVICEREQUEST,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.GetDeviceRequest)
  ))
_sym_db.RegisterMessage(GetDeviceRequest)

GetDeviceResponse = _reflection.GeneratedProtocolMessageType('GetDeviceResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETDEVICERESPONSE,
  __module__ = 'wiegand_pb2'
  # @@protoc_insertion_point(class_scope:wiegand.GetDeviceResponse)
  ))
_sym_db.RegisterMessage(GetDeviceResponse)


DESCRIPTOR._options = None

_WIEGAND = _descriptor.ServiceDescriptor(
  name='Wiegand',
  full_name='wiegand.Wiegand',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1772,
  serialized_end=2213,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetConfig',
    full_name='wiegand.Wiegand.GetConfig',
    index=0,
    containing_service=None,
    input_type=_GETCONFIGREQUEST,
    output_type=_GETCONFIGRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetConfig',
    full_name='wiegand.Wiegand.SetConfig',
    index=1,
    containing_service=None,
    input_type=_SETCONFIGREQUEST,
    output_type=_SETCONFIGRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetConfigMulti',
    full_name='wiegand.Wiegand.SetConfigMulti',
    index=2,
    containing_service=None,
    input_type=_SETCONFIGMULTIREQUEST,
    output_type=_SETCONFIGMULTIRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SearchDevice',
    full_name='wiegand.Wiegand.SearchDevice',
    index=3,
    containing_service=None,
    input_type=_SEARCHDEVICEREQUEST,
    output_type=_SEARCHDEVICERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetDevice',
    full_name='wiegand.Wiegand.SetDevice',
    index=4,
    containing_service=None,
    input_type=_SETDEVICEREQUEST,
    output_type=_SETDEVICERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetDevice',
    full_name='wiegand.Wiegand.GetDevice',
    index=5,
    containing_service=None,
    input_type=_GETDEVICEREQUEST,
    output_type=_GETDEVICERESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_WIEGAND)

DESCRIPTOR.services_by_name['Wiegand'] = _WIEGAND

# @@protoc_insertion_point(module_scope)
