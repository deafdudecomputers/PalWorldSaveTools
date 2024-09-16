from internal_libs.import_libs import *
from palworld_save_tools.archive import *
from palworld_save_tools.paltypes import *
import palworld_save_tools.rawdata.group as palworld_save_group
try:
    from setproctitle import setproctitle
except ImportError:
    def setproctitle(name):
        pass
module_dir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists("%s/resources/gui.json" % module_dir) and getattr(sys, 'frozen', False):
    module_dir = os.path.dirname(sys.executable)
class GvasPrettyPrint(pprint.PrettyPrinter):
    _dispatch = pprint.PrettyPrinter._dispatch.copy()
    def _pprint_dict(self, object, stream, indent, allowance, context, level):
        write = stream.write
        write('{')
        if self._indent_per_level > 1:
            write((self._indent_per_level - 1) * ' ')
        length = len(object)
        if length:
            if self._sort_dicts:
                items = sorted(object.items(), key=pprint._safe_tuple)
            else:
                items = object.items()
            fmtValue = False
            rep = ""
            dict_type = set(object.keys())
            if {'id', 'type', 'value'}.issubset(dict_type) and object['id'] is None:
                dict_type -= {'id', 'type', 'value', 'custom_type', 'skip_type'}
                if dict_type == set() and object['type'] in ["Int64Property", "NameProperty", "EnumProperty",
                                                             "IntProperty", "BoolProperty",
                                                             "FloatProperty", "StrProperty"]:
                    fmtValue = True
                    rep = object['type'][:-8]
                elif dict_type == {'struct_id', 'struct_type'} and object['type'] == "StructProperty" and str(
                        object['struct_id']) == '00000000-0000-0000-0000-000000000000':
                    rep = f"Struct:{object['struct_type']}"
                    fmtValue = True
                elif dict_type == {'array_type'} and object['type'] == "ArrayProperty":
                    rep = f"Array:{object['array_type']}"
                    fmtValue = True
            if fmtValue:
                repr = self._repr('value', context, level)
                if 'custom_type' in object:
                    write(f"{tcl(92)}{rep}{tcl(0)}=")
                else:
                    write(f"{tcl(36)}{rep}{tcl(0)}=")
                if rep == "Struct:Guid":
                    write(
                        tcl('43;31') if str(
                            object['value']) == "00000000-0000-0000-0000-000000000000" else tcl(93))
                    self._format(str(object['value']), stream, indent + len(repr) + 1, allowance,
                                 context, level)
                    write(tcl(0))
                else:
                    if 'skip_type' in object:
                        write(f"{tcl(91)}**Skip Load Size: {len(object['value'])}**{tcl(0)}")
                    elif rep == "Array:ByteProperty" and 'values' in object['value'] and isinstance(
                            object['value']['values'], tuple):
                        write(f"{tcl(91)}**Unparsed Size: {len(object['value']['values'])}**{tcl(0)}")
                    else:
                        self._format(object['value'], stream, indent + len(repr) + 1, allowance,
                                     context, level)
            else:
                self._format_dict_items(items, stream, indent, allowance + 1,
                                        context, level)
        write('}')
    def _pprint_UUID(self, object, stream, indent, allowance, context, level):
        stream.write(
            f"{tcl(36)}UUID:{tcl(0)}{tcl('43;31')}" if str(
                object) == "00000000-0000-0000-0000-000000000000" else tcl(93))
        self._format(str(object), stream, indent, allowance,
                     context, level)
        stream.write(tcl(0))
    def _pprint_tk(self, object, stream, indent, allowance, context, level):
        stream.write(f"{tcl(36)}{object.__class__.__name__}:{tcl(93)}")
        self._format(str(object.get()), stream, indent, allowance,
                     context, level)
        stream.write(tcl(0))
    _dispatch[dict.__repr__] = _pprint_dict
    _dispatch[UUID.__repr__] = _pprint_UUID
    _dispatch[tkinter.StringVar.__repr__] = _pprint_tk
    _dispatch[tkinter.BooleanVar.__repr__] = _pprint_tk
    _dispatch[tkinter.DoubleVar.__repr__] = _pprint_tk
    _dispatch[tkinter.IntVar.__repr__] = _pprint_tk
def tcl(cl):
    if ('TERM' in os.environ and 'color' in os.environ['TERM']) or 'WT_PROFILE_ID' in os.environ:
        return f"\033[{cl}m"
    return ""
pp = pprint.PrettyPrinter(width=80, compact=True, depth=6)
gvas_pp = GvasPrettyPrint(width=1, compact=True, depth=6)
gp = gvas_pp.pprint
def toUUID(uuid_str):
    if isinstance(uuid_str, UUID):
        return uuid_str
    return UUID.from_str(str(uuid_str))
def u32(value):
    return int.from_bytes((value & 0xffffffff).to_bytes(8, 'little', signed=True), byteorder='little',
                          signed=False)
def PlayerUid2NoSteam(unrealHashType):
    a = u32(u32(unrealHashType << 8) ^ u32(2654435769 - unrealHashType))
    b = u32((a >> 13) ^ u32(-(unrealHashType + a)))
    c = u32((b >> 12) ^ u32(unrealHashType - a - b))
    d = u32(u32(c << 16) ^ u32(a - c - b))
    e = u32((d >> 5) ^ (b - d - c))
    f = u32((e >> 3) ^ (c - d - e))
    result = u32(
        (u32(u32(f << 10) ^ u32(d - f - e)) >> 15) ^ (e - (u32(f << 10) ^ u32(d - f - e)) - f)
      )
    return "%08X" % result
def steamIdToPlayerUid(uid):
    from cityhash import CityHash64
    hash = CityHash64(str(uid).encode("utf-16-le"))
    return UUID(int(u32(u32(hash) + (hash >> 32) * 23)).to_bytes(4, byteorder="little", signed=False) + b"\x00" * 12)
class PalObject:
    EmptyUUID = toUUID("00000000-0000-0000-0000-000000000000")
    debug_wsd = None
    @staticmethod
    def toUUID(uuid_str):
        if isinstance(uuid_str, UUID):
            return uuid_str
        return UUID.from_str(str(uuid_str))
    @staticmethod
    def IntProperty(val):
        return {'id': None, 'type': 'IntProperty', 'value': val}
    @staticmethod
    def StrProperty(val):
        return {'id': None, 'type': 'StrProperty', 'value': val}
    @staticmethod
    def EnumProperty(type, val):
        return {'id': None, 'type': 'EnumProperty', 'value': {
            'type': type,
            'value': val
        }}
    @staticmethod
    def BoolProperty(val):
        return {'id': None, 'type': 'BoolProperty', 'value': val}
    @staticmethod
    def FloatProperty(val):
        return {'id': None, 'type': 'FloatProperty', 'value': val}
    @staticmethod
    def NameProperty(val):
        return {'id': None, 'type': 'NameProperty', 'value': val}
    @staticmethod
    def ArrayProperty(array_type, val, custom_type=None):
        rc = {'id': None, 'type': 'ArrayProperty', "array_type": array_type, 'value': val}
        if custom_type is not None:
            rc['custom_type'] = custom_type
        return rc
    @staticmethod
    def ArrayStructProperty(prop_name, struct_type, val=[]):
        return {
            'id': None,
            'type': 'ArrayProperty',
            "array_type": "StructProperty",
            "value": {
                'id': toUUID('00000000-0000-0000-0000-000000000000'),
                'prop_name': prop_name,
                'prop_type': 'StructProperty',
                'type_name': struct_type,
                'values': val
            }
        }
    @staticmethod
    def Guid(guid):
        return {'id': None,
                'struct_id': toUUID('00000000-0000-0000-0000-000000000000'),
                'struct_type': 'Guid',
                'type': 'StructProperty',
                'value': toUUID(guid)
                }
    @staticmethod
    def FixedPoint64(value):
        return {
            "struct_type": "FixedPoint64",
            "struct_id": PalObject.toUUID("00000000-0000-0000-0000-000000000000"),
            "id": None,
            "value": {
                "Value": {
                    "id": None,
                    "value": value,
                    "type": "Int64Property"
                }
            },
            "type": "StructProperty"
        }
    @staticmethod
    def Vector(x, y, z):
        return {
            "struct_type": "Vector",
            "struct_id": PalObject.toUUID("00000000-0000-0000-0000-000000000000"),
            "id": None,
            "value": {
                "x": x,
                "y": y,
                "z": z
            },
            "type": "StructProperty"
        }
    @staticmethod
    def PalContainerId(container_id):
        return {"id": None,
                "type": "StructProperty",
                "struct_id": toUUID('00000000-0000-0000-0000-000000000000'),
                "struct_type": "PalContainerId",
                "value": {
                    'ID': PalObject.Guid(container_id)
                }
                }
    @staticmethod
    def PalInstanceID(InstanceId, PlayerUId):
        return {"id": None,
                "type": "StructProperty",
                "struct_id": toUUID('00000000-0000-0000-0000-000000000000'),
                "struct_type": "PalInstanceID",
                "value": {
                    "DebugName": PalObject.StrProperty(""),
                    "InstanceId": PalObject.Guid(InstanceId),
                    "PlayerUId": PalObject.Guid(PlayerUId),
                }
                }
    @staticmethod
    def PalCharacterSlotId(container_id, slotIndex):
        return {
            "id": None,
            "type": "StructProperty",
            "struct_id": toUUID('00000000-0000-0000-0000-000000000000'),
            "struct_type": "PalCharacterSlotId",
            "value": {
                "ContainerId": PalObject.PalContainerId(container_id),
                "SlotIndex": PalObject.IntProperty(slotIndex)
            }
        }
    @staticmethod
    def PalCharacterSlotSaveData_Array(InstanceId, PlayerUId, characterInstanceId):
        return {
            'IndividualId': PalObject.PalInstanceID(InstanceId, PlayerUId),
            'PermissionTribeID': PalObject.EnumProperty('EPalTribeID', 'EPalTribeID::None'),
            'RawData': PalObject.ArrayProperty("ByteProperty", {
                'instance_id': toUUID(characterInstanceId),
                'permission_tribe_id': 0,
                'player_uid': toUUID(PlayerUId)
            }, ".worldSaveData.CharacterContainerSaveData.Value.Slots.Slots.RawData")
        }
    @staticmethod
    def PalItemContainerBelongInfo(GroupID):
        return {
            "id": None,
            "type": "StructProperty",
            "struct_id": toUUID('00000000-0000-0000-0000-000000000000'),
            "struct_type": "PalItemContainerBelongInfo",
            "value": {
                "GroupID": PalObject.Guid(GroupID)
            }
        }
    @staticmethod
    def PalItemId():
        return {
            'id': None,
            'struct_id': toUUID('00000000-0000-0000-0000-000000000000'),
            'struct_type': 'PalItemId',
            'type': 'StructProperty',
            'value': {
                'DynamicId': {
                    'id': None,
                    'struct_id': toUUID('00000000-0000-0000-0000-000000000000'),
                    'struct_type': 'PalDynamicItemId',
                    'type': 'StructProperty',
                    'value': {
                        'CreatedWorldId': {
                            'id': None,
                            'struct_id': toUUID('00000000-0000-0000-0000-000000000000'),
                            'struct_type': 'Guid',
                            'type': 'StructProperty',
                            'value': toUUID('00000000-0000-0000-0000-000000000000')
                        },
                        'LocalIdInCreatedWorld': {
                            'id': None,
                            'struct_id': toUUID('00000000-0000-0000-0000-000000000000'),
                            'struct_type': 'Guid',
                            'type': 'StructProperty',
                            'value': toUUID('00000000-0000-0000-0000-000000000000')
                        }
                    }
                },
                'StaticId': {
                    'id': None,
                    'type': 'NameProperty',
                    'value': 'None'
                }
            }
        }
    @staticmethod
    def PalItemSlotSaveData_Array(SlotIndex):
        return {'ItemId': PalObject.PalItemId(),
                'RawData': PalObject.ArrayProperty("ByteProperty", {'corruption_progress_value': 0.0,
                                                                    'permission': {'item_static_ids': [],
                                                                                   'type_a': [],
                                                                                   'type_b': []}},
                                                   ".worldSaveData.ItemContainerSaveData.Value.Slots.Slots.RawData"),
                'SlotIndex': PalObject.IntProperty(SlotIndex),
                'StackCount': PalObject.IntProperty(0)
                }
    @staticmethod
    def PalItemSlotSaveData_Slots(EmptySlots):
        c = {
            'id': toUUID('00000000-0000-0000-0000-000000000000'),
            'prop_name': 'Slots',
            'prop_type': 'StructProperty',
            'type_name': 'PalItemSlotSaveData',
            'values': []
        }
        for n in range(EmptySlots):
            c['values'].append(PalObject.PalItemSlotSaveData_Array(n))
        return c
    @staticmethod
    def ItemContainerSaveData_Array(InstanceId, EmptySlots):
        return {
            'key': {
                'ID': PalObject.Guid(InstanceId)
            },
            'value': {
                'BelongInfo': PalObject.PalItemContainerBelongInfo("00000000-0000-0000-0000-000000000000"),
                "RawData": PalObject.ArrayProperty("ByteProperty", {
                    'permission': {'item_static_ids': [],
                                   'type_a': [],
                                   'type_b': []}
                }, ".worldSaveData.ItemContainerSaveData.Value.RawData"),
                "Slots": PalObject.ArrayProperty("StructProperty", PalObject.PalItemSlotSaveData_Slots(EmptySlots))
            }
        }
    @staticmethod
    def CharacterContainerSaveData_Array(InstanceId, EmptySlots, assign_slot=[]):
        emptySlotArray = []
        if isinstance(EmptySlots, int):
            for n in range(EmptySlots):
                emptySlotArray.append(PalObject.PalCharacterSlotSaveData_Array(
                    "00000000-0000-0000-0000-000000000000",
                    "00000000-0000-0000-0000-000000000000",
                    "00000000-0000-0000-0000-000000000000" if n >= len(assign_slot) else
                    assign_slot[n]))
        return {
            'key': {
                'ID': PalObject.Guid(InstanceId)
            },
            'value': {
                "bReferenceSlot": PalObject.BoolProperty(False),
                "Slots": PalObject.ArrayStructProperty('Slots', "PalCharacterSlotSaveData", emptySlotArray),
                "RawData": PalObject.ArrayProperty('ByteProperty', {'values': ()}),
            }
        }
    @staticmethod
    def GroupSaveData(group_id, group_name, admin_player_uid, admin_nickname):
        return {
            'key': toUUID(group_id),
            'value': {
                "GroupType": {
                    "id": None,
                    "value": {
                        "type": "EPalGroupType",
                        "value": "EPalGroupType::Guild"
                    },
                    "type": "EnumProperty"
                },
                "RawData": PalObject.ArrayProperty('ByteProperty', {
                    'admin_player_uid': toUUID(admin_player_uid),
                    "base_camp_level": 1,
                    "base_ids": [],
                    "group_id": toUUID(group_id),
                    "group_name": "",
                    'group_type': 'EPalGroupType::Guild',
                    "guild_name": group_name,
                    "individual_character_handle_ids": [],
                    "map_object_instance_ids_base_camp_points": [],
                    "org_type": 0,
                    "players": [
                        {
                            'player_uid': toUUID(admin_player_uid),
                            'player_info': {'last_online_real_time': 0,
                                            'player_name': admin_nickname}
                        }
                    ]
                })
            }
        }
class MPMapValue(dict):
    def __init__(self, obj):
        self.obj = obj
    def load(self):
        _data = pickle.loads(self.obj)
        self.__getitem__ = super().__getitem__
        self.update(_data)
        self.__iter__ = super().__iter__
        self.__setitem__ = super().__setitem__
    def __getitem__(self, key):
        self.load()
        return super().__getitem__(key)
    def __setitem__(self, key, value):
        self.load()
        return super().__setitem__(key, value)
    def __iter__(self):
        self.load()
        return super().__iter__()
def decode_uuid(obj):
    if '__uuid__' in obj:
        obj = UUID(obj['__uuid__'])
    return obj
def encode_uuid(obj):
    if isinstance(obj, UUID):
        return {'__uuid__': obj.raw_bytes}
    return obj
class MPMapObject(dict):
    def __init__(self, key, obj):
        self.parsed_key = False
        self.parsed_value = False
        self.key = key
        self.value = obj
        self.update({
            'key': None,
            'value': None
        })
    def __getitem__(self, key):
        if key == 'key':
            if not self.parsed_key:
                self.parsed_key = True
                self.key = msgpack.unpackb(self.key, object_hook=decode_uuid, raw=False)
                self.update({
                    'key': self.key
                })
            if self.parsed_value:
                self.__getitem__ = super().__getitem__
                self.__iter__ = super().__iter__
            return self.key
        if key == 'value':
            if not self.parsed_value:
                self.parsed_value = True
                self.value = msgpack.unpackb(self.value, object_hook=decode_uuid, raw=False)
                self.update({
                    'value': self.value
                })
            if self.parsed_key:
                self.__getitem__ = super().__getitem__
                self.__iter__ = super().__iter__
            return self.value
        return super().__getitem__(key)
    def __iter__(self):
        for key in super().__iter__():
            yield key
        if 'key' not in self:
            yield 'key'
        if 'value' not in self:
            yield 'value'
class MMapProperty(ctypes.Structure):
    _fields_ = [("current", ctypes.c_ulong),
                ("last", ctypes.c_ulong),
                ("count", ctypes.c_ulong),
                ("parsed_count", ctypes.c_ulong),
                ("size", ctypes.c_ulong),
                ("datasize", ctypes.c_ulong)]
class MPMapProperty(list):
    WithKeys = True
    def __init__(self, *args, **kwargs):
        super().__init__()
        count = kwargs.get("count", 0)
        data = kwargs.get("data", None)
        self.data = None
        if data is None:
            size = kwargs.get("size", 0)
        else:
            size = len(data) * 3
        intsize = ctypes.sizeof(ctypes.c_ulong)
        self.closed = False
        self.loaded = False
        if kwargs.get("name", None) is not None:
            self.shm = shared_memory.SharedMemory(name=kwargs.get("name", None))
        else:
            self.shm = shared_memory.SharedMemory(create=True, size=size)
        self.memaddr = ctypes.addressof(ctypes.c_void_p.from_buffer(self.shm.buf.obj))
        self.prop = MMapProperty.from_address(self.memaddr)
        struct_head_size = ctypes.sizeof(MMapProperty)
        struct_content_size = intsize * count * (3 if self.__class__.WithKeys else 2)
        if kwargs.get("name", None) is None:
            ctypes.memset(self.memaddr, 0, struct_head_size + struct_content_size)
            self.prop.count = count
            self.prop.size = size
            self.prop.datasize = len(kwargs.get("data", ()))
            self.prop.last = struct_head_size + struct_content_size
        self.index = (ctypes.c_ulong * self.prop.count).from_address(self.memaddr + struct_head_size)
        self.value_size = (ctypes.c_ulong * self.prop.count).from_address(
            self.memaddr + struct_head_size + intsize * self.prop.count)
        if self.__class__.WithKeys:
            self.key_size = (ctypes.c_ulong * self.prop.count).from_address(
                self.memaddr + struct_head_size + intsize * self.prop.count * 2)
        else:
            self.key_size = None
        if kwargs.get("name", None) is None and not data is None:
            ctypes.memmove(self.memaddr + self.prop.size - self.prop.datasize, data, self.prop.datasize)
            self.data = ((ctypes.c_byte * self.prop.datasize).
                         from_address(self.memaddr + self.prop.size - self.prop.datasize))
        elif kwargs.get("name", None) is not None:
            self.data = ((ctypes.c_byte * self.prop.datasize).
                         from_address(self.memaddr + self.prop.size - self.prop.datasize))
        super().extend([None] * self.prop.count)
    def close(self):
        if self.closed:
            return
        self.closed = True
        del self.prop
        del self.index
        del self.key_size
        del self.value_size
        self.shm.buf.release()
        self.shm.close()
    def release(self):
        self.shm.unlink()
    def append(self, obj):
        if self.closed and not self.loaded:
            raise ValueError("Share Memory closed")
        if not self.closed and self.prop.current < self.prop.count:
            self.index[self.prop.current] = self.prop.last
            if self.__class__.WithKeys:
                key = msgpack.packb(obj['key'], default=encode_uuid, use_bin_type=True)
                val = msgpack.packb(obj['value'], default=encode_uuid, use_bin_type=True)
                self.key_size[self.prop.current] = len(key)
                ctypes.memmove(self.memaddr + self.prop.last, key, len(key))
            else:
                key = ()
                val = msgpack.packb(obj, default=encode_uuid, use_bin_type=True)
            self.value_size[self.prop.current] = len(val)
            ctypes.memmove(self.memaddr + self.prop.last + len(key), val, len(val))
            self.prop.last += len(key) + len(val)
            self.prop.current += 1
        else:
            super().append(obj)
    def __iter__(self):
        for i in range(len(self)):
            yield self.__getitem__(i)
    def __getitem__(self, item):
        result = super().__getitem__(item)        
        if result is None:
            if self.closed:
                raise ValueError("Share Memory closed")            
            k_s = self.index[item]            
            if self.__class__.WithKeys:
                v_s = k_s + self.key_size[item]
                key_bytes = bytearray(self.shm.buf[k_s:v_s])
                value_bytes = bytearray(self.shm.buf[v_s:v_s + self.value_size[item]])
                result = MPMapObject(key_bytes, value_bytes)
            else:
                v_e = k_s + self.value_size[item]
                value_bytes = bytearray(self.shm.buf[k_s:v_e])
                result = msgpack.unpackb(value_bytes, object_hook=decode_uuid, raw=False)            
            self[item] = result
            self.prop.parsed_count += 1            
            if self.prop.parsed_count == self.prop.count:
                self.loaded = True
                self.close()        
        return result
    def load_all_items(self):
        if self.loaded:
            return
        if self.closed:
            raise ValueError("Share Memory closed")
        for i in range(self.prop.current):
            self.__getitem__(i)
    def __delitem__(self, item):
        self.load_all_items()
        if not self.loaded:
            self.prop.current -= 1
        return super().__delitem__(item)
class MPArrayProperty(MPMapProperty):
    WithKeys = False
def skip_decode(
        reader: FArchiveReader, type_name: str, size: int, path: str
) -> dict[str, Any]:
    if type_name == "ArrayProperty":
        array_type = reader.fstring()
        value = {
            "skip_type": type_name,
            "array_type": array_type,
            "id": reader.optional_guid(),
            "value": reader.read(size)
        }
    elif type_name == "MapProperty":
        key_type = reader.fstring()
        value_type = reader.fstring()
        _id = reader.optional_guid()
        value = {
            "skip_type": type_name,
            "key_type": key_type,
            "value_type": value_type,
            "id": _id,
            "value": reader.read(size),
        }
    elif type_name == "StructProperty":
        value = {
            "skip_type": type_name,
            "struct_type": reader.fstring(),
            "struct_id": reader.guid(),
            "id": reader.optional_guid(),
            "value": reader.read(size),
        }
    else:
        raise Exception(
            f"Expected ArrayProperty or MapProperty or StructProperty, got {type_name} in {path}"
        )
    return value
def skip_encode(
        writer: FArchiveWriter, property_type: str, properties: dict[str, Any]
) -> int:
    if "skip_type" not in properties:
        if properties['custom_type'] in PALWORLD_CUSTOM_PROPERTIES is not None:
            return PALWORLD_CUSTOM_PROPERTIES[properties["custom_type"]][1](
                writer, property_type, properties
            )
        else:
            return writer.property_inner(writer, property_type, properties)
    if property_type == "ArrayProperty":
        del properties["custom_type"]
        del properties["skip_type"]
        writer.fstring(properties["array_type"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    elif property_type == "MapProperty":
        del properties["custom_type"]
        del properties["skip_type"]
        writer.fstring(properties["key_type"])
        writer.fstring(properties["value_type"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    elif property_type == "StructProperty":
        del properties["custom_type"]
        del properties["skip_type"]
        writer.fstring(properties["struct_type"])
        writer.guid(properties["struct_id"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    else:
        raise Exception(
            f"Expected ArrayProperty or MapProperty or StructProperty, got {property_type}"
        )
class MPMapPropertyProcess(multiprocessing.Process):
    def __init__(self, reader, properties, count, path):
        super().__init__()
        self.type_hints = reader.type_hints
        self.custom_properties = reader.custom_properties
        self.allow_nan = reader.allow_nan
        self.properties = properties
        self.count = count
        self.path = path
    def run(self) -> None:
        setproctitle(f"{self.__class__.__name__}:{self.path}")
        prop_val = MPMapProperty(name=self.properties['value'])
        key_type = self.properties['key_type']
        key_struct_type = self.properties['key_struct_type']
        value_type = self.properties['value_type']
        value_struct_type = self.properties['value_struct_type']
        key_path = self.path + ".Key"
        value_path = self.path + ".Value"
        with FArchiveReader(
                bytes(prop_val.data),
                type_hints=self.type_hints,
                custom_properties=self.custom_properties,
                allow_nan=self.allow_nan,
        ) as reader:
            for _ in range(self.count):
                key = reader.prop_value(key_type, key_struct_type, key_path)
                value = reader.prop_value(value_type, value_struct_type, value_path)
                prop_val.append({
                    "key": key,
                    "value": value
                })
        prop_val.close()
        os._exit(0)
class MPArrayPropertyProcess(multiprocessing.Process):
    def __init__(self, reader, properties, count, size, path):
        super().__init__()
        self.type_hints = reader.type_hints
        self.custom_properties = reader.custom_properties
        self.allow_nan = reader.allow_nan
        self.properties = properties
        self.count = count
        self.size = size
        self.path = path
    def run(self) -> None:
        setproctitle(f"{self.__class__.__name__}:{self.path}")
        prop_values = MPArrayProperty(name=self.properties['value']['values'])
        with FArchiveReader(
                bytes(prop_values.data),
                type_hints=self.type_hints,
                custom_properties=self.custom_properties,
                allow_nan=self.allow_nan,
        ) as reader:
            array_type = self.properties['array_type']
            if array_type == "StructProperty":
                type_name = self.properties['value']['type_name']
                prop_path = f"{self.path}.{self.properties['value']['prop_name']}"
                for _ in range(self.count):
                    prop_values.append(reader.struct_value(type_name, prop_path))
            else:
                decode_func: Callable
                if array_type == "EnumProperty":
                    decode_func = reader.fstring
                elif array_type == "NameProperty":
                    decode_func = reader.fstring
                elif array_type == "Guid":
                    decode_func = reader.guid
                elif array_type == "ByteProperty":
                    if self.size == self.count:
                        return reader.byte_list(self.count)
                    else:
                        raise Exception("Labelled ByteProperty not implemented")
                else:
                    raise Exception(f"Unknown array type: {array_type} ({self.path})")
                for _ in range(self.count):
                    prop_values.append(decode_func())
        prop_values.close()
        os._exit(0)
class FProgressArchiveReader(FArchiveReader):
    def __init__(self, *args, **kwargs):
        reduce_memory = False
        self.raise_error = False
        self.processlist = {}
        self.progresslist = {}
        if 'reduce_memory' in kwargs:
            reduce_memory = kwargs['reduce_memory']
            del kwargs['reduce_memory']
        if 'check_err' in kwargs:
            self.raise_error = kwargs['check_err']
            del kwargs['check_err']
        super().__init__(*args, **kwargs)
        self.fallbackData = None
        self.mp_loading = False
        if getattr(sys, 'frozen', False):
            pass
        elif sys.platform == 'linux':
            with open("/proc/meminfo", "r", encoding='utf-8') as f:
                for line in f:
                    if 'MemFree:' == line[0:8]:
                        remain = line.split(": ")[1].strip().split(" ")
                        if remain[1] == 'kB' and int(remain[0]) > 1048576 > 4:
                            self.mp_loading = False if reduce_memory else True
        elif sys.platform == 'darwin' or sys.platform == 'win32':
            self.mp_loading = False if reduce_memory else True
    def internal_copy(self, data, debug: bool) -> "FProgressArchiveReader":
        return FProgressArchiveReader(
            data,
            self.type_hints,
            self.custom_properties,
            debug=debug,
            allow_nan=self.allow_nan,
            check_err=self.raise_error
        )
    def fstring(self) -> str:
        reader = self.data
        (size,) = FArchiveReader.unpack_i32(reader.read(4))
        if size == 0:
            return ""
        data: bytes
        encoding: str
        if size < 0:
            size = -size
            data = reader.read(size * 2)[:-2]
            encoding = "utf-16-le"
        else:
            data = reader.read(size)[:-1]
            encoding = "ascii"
        try:
            return data.decode(encoding)
        except Exception as e:
            if self.raise_error:
                raise Exception(
                    f"Error decoding {encoding} string of length {size}: {bytes(data)!r}"
                ) from e
            else:
                try:
                    escaped = data.decode(encoding, errors="surrogatepass")
                    print(
                        f"Error decoding {encoding} string of length {size}, data loss may occur! {bytes(data)!r}"
                    )
                    return escaped
                except Exception as e:
                    raise Exception(
                        f"Error decoding {encoding} string of length {size}: {bytes(data)!r}"
                    ) from e
    def progress_eof(self):
        try:
            return self.eof() and len(self.processlist) == 0
        except ValueError:
            return len(self.progresslist) == 0
    def progress(self):
        reduce_size = 0
        del_path = []
        for mp_path in self.progresslist:
            reduce_size += self.progresslist[mp_path]['size']
            prop = getattr(self.progresslist[mp_path]['share_mp'], "prop", None)
            if prop is not None:
                loaded_size = int(self.progresslist[mp_path]['size'] * (prop.current / prop.count))
                reduce_size -= loaded_size
                if reduce_size == 0:
                    del_path.append(mp_path)
            else:
                del_path.append(mp_path)
        for mp_path in del_path:
            del self.progresslist[mp_path]
        try:
            if self.eof():
                return self.size - reduce_size
            return self.data.tell() - reduce_size
        except ValueError:
            return self.size - reduce_size
    def load_mp_map(self, properties, path, size):
        key_type = self.fstring()
        value_type = self.fstring()
        _id = self.optional_guid()
        ext_data_offset = self.data.tell()
        self.u32()
        count = self.u32()
        key_path = path + ".Key"
        if key_type == "StructProperty":
            key_struct_type = self.get_type_or(key_path, "Guid")
        else:
            key_struct_type = None
        value_path = path + ".Value"
        if value_type == "StructProperty":
            value_struct_type = self.get_type_or(value_path, "StructProperty")
        else:
            value_struct_type = None
        data = self.read(size - (self.data.tell() - ext_data_offset))
        share_mp = MPMapProperty(data=data, count=count)
        properties.update({
            "type": "MapProperty",
            "key_type": key_type,
            "value_type": value_type,
            "key_struct_type": key_struct_type,
            "value_struct_type": value_struct_type,
            "id": _id,
            "value": share_mp.shm.name
        })
        self.progresslist[path] = {
            "share_mp": share_mp,
            "count": count,
            "size": size
        }
        p = MPMapPropertyProcess(self, properties, count, path)
        p.start()
        properties.update({
            'value': share_mp
        })
        return p
    def load_mp_array(self, properties, path, size):
        array_type = self.fstring()
        _id = self.optional_guid()
        ext_data_offset = self.data.tell()
        count = self.u32()
        properties.update({
            "type": "ArrayProperty",
            "array_type": array_type,
            "id": _id,
            "value": {
                "values": None
            }
        })
        if array_type == "StructProperty":
            prop_name = self.fstring()
            prop_type = self.fstring()
            self.u64()
            type_name = self.fstring()
            _id = self.guid()
            self.skip(1)
            properties['value'].update({
                "prop_name": prop_name,
                "prop_type": prop_type,
                "type_name": type_name,
                "id": _id
            })
        data = self.read(size - (self.data.tell() - ext_data_offset))
        mp_ctx = MPArrayProperty(data=data, count=count)
        properties['value']['values'] = mp_ctx.shm.name
        p = MPArrayPropertyProcess(self, properties, count, size, path)
        p.start()
        properties['value'].update({
            'values': mp_ctx
        })
        self.progresslist[path] = {
            "share_mp": mp_ctx,
            "count": count,
            "size": size
        }
        return p
    def property(
            self, type_name: str, size: int, path: str, nested_caller_path: str = ""
    ) -> dict[str, Any]:
        if size == -1:
            return self.fallbackData
        if self.raise_error:
            if path in self.custom_properties and (
                    path is not nested_caller_path or nested_caller_path == ""
            ):
                value = self.custom_properties[path][0](self, type_name, size, path)
                value["custom_type"] = path
                value["type"] = type_name
                return value
            elif type_name == "MapProperty":
                key_type = self.fstring()
                value_type = self.fstring()
                _id = self.optional_guid()
                self.u32()
                count = self.u32()
                key_path = path + ".Key"
                if key_type == "StructProperty":
                    key_struct_type = self.get_type_or(key_path, "Guid")
                else:
                    key_struct_type = None
                value_path = path + ".Value"
                if value_type == "StructProperty":
                    value_struct_type = self.get_type_or(value_path, "StructProperty")
                else:
                    value_struct_type = None
                values: list[dict[str, Any]] = []
                for _ in range(count):
                    try:
                        key = self.prop_value(key_type, key_struct_type, key_path)
                        value = self.prop_value(value_type, value_struct_type, value_path)
                    except Exception as e:
                        print(f"\033[31mDecodeing Failed on MapProperty {path}[{_}]\033[0m")
                        raise e
                    values.append(
                        {
                            "key": key,
                            "value": value,
                        }
                    )
                value = {
                    "type": type_name,
                    "key_type": key_type,
                    "value_type": value_type,
                    "key_struct_type": key_struct_type,
                    "value_struct_type": value_struct_type,
                    "id": _id,
                    "value": values,
                }
                return value
        return super().property(type_name, size, path, nested_caller_path)
    def array_property(self, array_type: str, size: int, path: str):
        count = self.u32()
        value = {}
        if array_type == "StructProperty":
            prop_name = self.fstring()
            prop_type = self.fstring()
            self.u64()
            type_name = self.fstring()
            _id = self.guid()
            self.skip(1)
            prop_values = []
            for _ in range(count):
                try:
                    prop_values.append(self.struct_value(type_name, f"{path}.{prop_name}"))
                except Exception as e:
                    if self.raise_error:
                        print(f"\033[31mDecodeing Failed on ArrayProperty {path}.{prop_name}[{_}]\033[0m")
                    raise e
            value = {
                "prop_name": prop_name,
                "prop_type": prop_type,
                "values": prop_values,
                "type_name": type_name,
                "id": _id,
            }
        else:
            value = {
                "values": self.array_value(array_type, count, size, path),
            }
        return value
    def properties_until_end(self, path: str = "") -> dict[str, Any]:
        properties = {}
        while True:
            try:
                name = self.fstring()
                if name == "None":
                    break
                type_name = self.fstring()
                size = self.u64()
                sub_path = f"{path}.{name}"
                mp_loading = self.mp_loading
                if sub_path in self.custom_properties and self.custom_properties[sub_path][0] is skip_decode:
                    mp_loading = False
                if mp_loading and path == ".worldSaveData" and type_name == "MapProperty" and size > 1048576:
                    properties[name] = {}
                    self.processlist[sub_path] = self.load_mp_map(properties[name], sub_path, size)
                elif mp_loading and path == ".worldSaveData" and type_name == "ArrayProperty" and size > 1048576:
                    properties[name] = {}
                    self.processlist[sub_path] = self.load_mp_array(properties[name], sub_path, size)
                else:
                    properties[name] = self.property(type_name, size, f"{path}.{name}")
            except struct.error as e:
                raise e
            except Exception as e:
                print(f"\033[31mDecodeing Failed on Decodeing Path {path} -> {type(e)}: {str(e)}\033[0m")
                traceback.print_exception(e)
                raise e
        if path == "":
            for mp_path in self.processlist:
                self.processlist[mp_path].join()
                if mp_path in self.custom_properties and 'worldSaveData' in properties:
                    try:
                        self.fallbackData = properties['worldSaveData']['value'][mp_path[15:]]
                        properties['worldSaveData']['value'][mp_path[15:]] = \
                            self.custom_properties[mp_path][0](self,
                                                               properties['worldSaveData']['value'][mp_path[15:]][
                                                                   'type'],
                                                               -1, mp_path)
                        properties['worldSaveData']['value'][mp_path[15:]]["custom_type"] = mp_path
                    except Exception as e:
                        keyList = properties.keys()
                        if 'worldSaveData' in properties:
                            keyList = properties['worldSaveData']['value'].keys()
                            PalObject.debug_wsd = properties['worldSaveData']['value']
                        raise ValueError(f"Decode failed, path={path}.{mp_path}, property={keyList}") from e
            self.processlist = {}
            self.progresslist = {}
        return properties
    def parse_item(self, properties, skip_path):
        if isinstance(properties, dict):
            if 'skip_type' in properties:
                properties_parsed = self.parse_skiped_item(properties, skip_path)
                for k in properties_parsed:
                    properties[k] = properties_parsed[k]
            else:
                for key in properties:
                    call_skip_path = skip_path + "." + key[0].upper() + key[1:]
                    properties[key] = self.parse_item(properties[key], call_skip_path)
        elif isinstance(properties, list):
            top_skip_path = ".".join(skip_path.split(".")[:-1])
            for idx, item in enumerate(properties):
                properties[idx] = self.parse_item(item, top_skip_path)
        return properties
    def parse_skiped_item(self, properties, skip_path, progress: Optional[Callable]=None):
        if "skip_type" not in properties:
            return properties
        writer = FArchiveWriter(PALWORLD_CUSTOM_PROPERTIES)
        if properties["skip_type"] == "ArrayProperty":
            writer.fstring(properties["array_type"])
            writer.optional_guid(properties.get("id", None))
            writer.write(properties['value'])
        elif properties["skip_type"] == "MapProperty":
            writer.fstring(properties["key_type"])
            writer.fstring(properties["value_type"])
            writer.optional_guid(properties.get("id", None))
            writer.write(properties["value"])
        elif properties["skip_type"] == "StructProperty":
            writer.fstring(properties["struct_type"])
            writer.guid(properties["struct_id"])
            writer.optional_guid(properties.get("id", None))
            writer.write(properties["value"])
        keep_custom_type = False
        localProperties = copy.deepcopy(PALWORLD_CUSTOM_PROPERTIES)
        if ".worldSaveData.%s" % skip_path in PALWORLD_CUSTOM_PROPERTIES:
            localProperties[".worldSaveData.%s" % skip_path] = PALWORLD_CUSTOM_PROPERTIES[
                ".worldSaveData.%s" % skip_path]
            keep_custom_type = True
        elif ".worldSaveData.%s" % skip_path in localProperties:
            del localProperties[".worldSaveData.%s" % skip_path]
        data = writer.bytes()
        with FProgressArchiveReader(
                data, PALWORLD_TYPE_HINTS,
                localProperties
        ) as reader:
            if progress is not None:
                progress(reader, len(data))
            decoded_properties = reader.property(properties["skip_type"], len(properties['value']),
                                                 ".worldSaveData.%s" % skip_path)
            for k in decoded_properties:
                properties[k] = decoded_properties[k]
        if not keep_custom_type:
            del properties['custom_type']
        del properties["skip_type"]
        return properties
def group_decode(
        reader: FProgressArchiveReader, type_name: str, size: int, path: str
) -> dict[str, Any]:
    if type_name != "MapProperty":
        raise Exception(f"Expected MapProperty, got {type_name}")
    value = reader.property(type_name, size, path, nested_caller_path=path)
    group_map = value["value"]
    for group in group_map:
        group_type = group["value"]["GroupType"]["value"]["value"]
        if group_type != "EPalGroupType::Guild":
            continue
        group['value']['RawData'] = reader.parse_item(group['value']['RawData'], "GroupSaveDataMap.Value.RawData")
        group_bytes = group["value"]["RawData"]["value"]["values"]
        group["value"]["RawData"]["value"] = palworld_save_group.decode_bytes(
            reader, group_bytes, group_type
        )
    return value
def group_encode(
        writer: FArchiveWriter, property_type: str, properties: dict[str, Any]
) -> int:
    if property_type != "MapProperty":
        raise Exception(f"Expected MapProperty, got {property_type}")
    del properties["custom_type"]
    group_map = properties["value"]
    for group in group_map:
        group_type = group["value"]["GroupType"]["value"]["value"]
        if group_type != "EPalGroupType::Guild":
            continue
        if "values" in group["value"]["RawData"]["value"]:
            continue
        p = group["value"]["RawData"]["value"]
        encoded_bytes = palworld_save_group.encode_bytes(p)
        group["value"]["RawData"]["value"] = {"values": [b for b in encoded_bytes]}
    return writer.property_inner(property_type, properties)
class JsonPalSimpleObject:
    type = None
    value = None
    custom_type = None
    def __init__(self, _type, _value, custom_type=None):
        self.type = _type
        self.value = _value
        self.custom_type = custom_type
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return f"PalObject.toUUID('{str(obj)}')"
        elif isinstance(obj, JsonPalSimpleObject):
            if obj.custom_type is not None:
                return f"PalObject.{obj.type}({repr(obj.value)}, {repr(obj.custom_type)})"
            else:
                return f"PalObject.{obj.type}({repr(obj.value)})"
        return super(CustomEncoder, self).default(obj)
def AutoMakeStruct(struct):
    import re
    structs = {}
    if 'type' in struct and struct['type'] == "StructProperty":
        if struct['struct_type'] in ["Vector"]:
            return structs
        for k in struct['value']:
            if isinstance(struct['value'][k], JsonPalSimpleObject):
                continue
            if struct['value'][k]['type'] in ['IntProperty', 'StrProperty', 'BoolProperty', 'FloatProperty']:
                struct['value'][k] = JsonPalSimpleObject(struct['value'][k]['type'], struct['value'][k]['value'])
            elif struct['value'][k]['type'] == 'StructProperty':
                structs.update(AutoMakeStruct(struct['value'][k]))
                struct['value'][k] = JsonPalSimpleObject(struct['value'][k]['struct_type'], None)
            elif struct['value'][k]['type'] == 'ArrayProperty':
                struct['value'][k] = JsonPalSimpleObject("ArrayProperty", struct['value'][k]['array_type'],
                                                         struct['value'][k]['custom_type'] if 'custom_type' in
                                                                                              struct['value'][
                                                                                                  k] else None)
        if struct['struct_type'] not in dir(PalObject):
            structs[struct['struct_type']] = "    @staticmethod\n" + \
                                             f"    def {struct['struct_type']}():\n" + \
                                             f"        return " + re.sub(r"\"PalObject\.(.+)\",?", "PalObject.\\1,",
                                                                         json.dumps(struct, indent=4,
                                                                                    cls=CustomEncoder).replace("\n",
                                                                                                               "\n        "))
    return structs
class MappingCacheObject:
    __slots__ = ("_worldSaveData", "EnumOptions", "use_mp",
                 "PlayerIdMapping", "CharacterSaveParameterMap", "MapObjectSaveData", "MapObjectSpawnerInStageSaveData",
                 "ItemContainerSaveData", "DynamicItemSaveData", "CharacterContainerSaveData", "GroupSaveDataMap",
                 "WorkSaveData", "BaseCampMapping", "GuildSaveDataMap", "GuildInstanceMapping",
                 "FoliageGridSaveDataMap")

    _MappingCacheInstances = {
    }
    @staticmethod
    def get(worldSaveData, use_mp=True) -> "MappingCacheObject":
        if id(worldSaveData) not in MappingCacheObject._MappingCacheInstances:
            MappingCacheObject._MappingCacheInstances[id(worldSaveData)] = MappingCacheObject(worldSaveData)
            MappingCacheObject._MappingCacheInstances[id(worldSaveData)].use_mp = use_mp
        return MappingCacheObject._MappingCacheInstances[id(worldSaveData)]
    def __init__(self, worldSaveData):
        self._worldSaveData = worldSaveData
        self.use_mp = True
    def __getattr__(self, item):
        if item == 'WorkSaveData':
            self.LoadWorkSaveData()
            return self.WorkSaveData
        elif item == 'MapObjectSaveData':
            self.LoadMapObjectMaps()
            return self.MapObjectSaveData
        elif item == 'MapObjectSpawnerInStageSaveData':
            self.LoadMapObjectMaps()
            return self.MapObjectSpawnerInStageSaveData
        elif item == 'PlayerIdMapping':
            self.LoadCharacterSaveParameterMap()
            return self.PlayerIdMapping
        elif item == 'CharacterSaveParameterMap':
            self.LoadCharacterSaveParameterMap()
            return self.CharacterSaveParameterMap
        elif item == 'ItemContainerSaveData':
            self.LoadItemContainerMaps()
            return self.ItemContainerSaveData
        elif item == 'DynamicItemSaveData':
            self.LoadItemContainerMaps()
            return self.DynamicItemSaveData
        elif item == 'CharacterContainerSaveData':
            self.LoadCharacterContainerMaps()
            return self.CharacterContainerSaveData
        elif item == 'GroupSaveDataMap':
            self.LoadGroupSaveDataMap()
            return self.GroupSaveDataMap
        elif item == 'GuildSaveDataMap':
            self.LoadGroupSaveDataMap()
            return self.GuildSaveDataMap
        elif item == 'BaseCampMapping':
            self.LoadBaseCampMapping()
            return self.BaseCampMapping
        elif item == 'GuildInstanceMapping':
            self.LoadGuildInstanceMapping()
            return self.GuildInstanceMapping
        elif item == 'FoliageGridSaveDataMap':
            self.LoadMapObjectMaps()
            return self.FoliageGridSaveDataMap
        elif item == "EnumOptions":
            with open(f"{module_dir}/resources/enum.json", "r", encoding="utf-8") as f:
                self.EnumOptions = json.load(f)
            return self.EnumOptions
    def LoadWorkSaveData(self):
        BatchParseItem(self._worldSaveData, ['WorkSaveData'], False, use_mp=self.use_mp)
        self.WorkSaveData = {wrk['RawData']['value']['id']: wrk for wrk in
                             self._worldSaveData['WorkSaveData']['value']['values']}
    def LoadMapObjectMaps(self):
        BatchParseItem(self._worldSaveData, ['MapObjectSaveData', 'MapObjectSpawnerInStageSaveData'], False, use_mp=self.use_mp)
        self.MapObjectSaveData = {
            mapobj['MapObjectInstanceId']['value']: mapobj for mapobj in
            self._worldSaveData['MapObjectSaveData']['value']['values']}
        self.MapObjectSpawnerInStageSaveData = {
            mapObj['key']: mapObj
            for mapObj in
            self._worldSaveData['MapObjectSpawnerInStageSaveData']['value'][0]['value'][
                'SpawnerDataMapByLevelObjectInstanceId']['value']
        }
        self.FoliageGridSaveDataMap = {
        }
    def LoadCharacterSaveParameterMap(self):
        self.CharacterSaveParameterMap = {character['key']['InstanceId']['value']: character for character in
                                          self._worldSaveData['CharacterSaveParameterMap']['value']}
        self.PlayerIdMapping = {character['key']['PlayerUId']['value']: character for character in
                                filter(lambda x: 'IsPlayer' in
                                                 x['value']['RawData']['value']['object']['SaveParameter']['value'],
                                       self._worldSaveData['CharacterSaveParameterMap']['value'])}
    def LoadItemContainerMaps(self):
        BatchParseItem(self._worldSaveData, ['ItemContainerSaveData', 'DynamicItemSaveData'], False, use_mp=self.use_mp)
        self.ItemContainerSaveData = {container['key']['ID']['value']: container for container in
                                      self._worldSaveData['ItemContainerSaveData']['value']}
        self.DynamicItemSaveData = {dyn_item_data['ID']['value']['LocalIdInCreatedWorld']['value']: dyn_item_data
                                    for
                                    dyn_item_data in self._worldSaveData['DynamicItemSaveData']['value']['values']}
    def LoadCharacterContainerMaps(self):
        BatchParseItem(self._worldSaveData, ['CharacterContainerSaveData'], False, use_mp=self.use_mp)
        self.CharacterContainerSaveData = {container['key']['ID']['value']: container for container in
                                           self._worldSaveData['CharacterContainerSaveData']['value']}
    def LoadGroupSaveDataMap(self):
        self.GroupSaveDataMap = {group['key']: group for group in self._worldSaveData['GroupSaveDataMap']['value']}
        self.GuildSaveDataMap = {group['key']: group for group in
                                 filter(lambda x: x['value']['GroupType']['value']['value'] == "EPalGroupType::Guild",
                                        self._worldSaveData['GroupSaveDataMap']['value'])}
    def LoadBaseCampMapping(self):
        self.BaseCampMapping = {base['key']: base for base in self._worldSaveData['BaseCampSaveData']['value']}
    def LoadGuildInstanceMapping(self):
        self.GuildInstanceMapping = {}
        for group_id in self.GuildSaveDataMap:
            group_data = parse_skiped_item(self.GuildSaveDataMap[group_id], "GroupSaveDataMap")
            item = group_data['value']['RawData']['value']
            self.GuildInstanceMapping.update(
                {ind_char['guid']: ind_char['instance_id'] for ind_char in item['individual_character_handle_ids']})
    def __del__(self):
        for key in self._worldSaveData:
            if isinstance(self._worldSaveData[key]['value'], MPMapProperty):
                self._worldSaveData[key]['value'].close()
                self._worldSaveData[key]['value'].release()
            elif isinstance(self._worldSaveData[key]['value'], dict) and 'values' in self._worldSaveData[key][
                'value'] and isinstance(
                self._worldSaveData[key]['value']['values'], MPArrayProperty):
                self._worldSaveData[key]['value']['values'].close()
                self._worldSaveData[key]['value']['values'].release()
def parse_skiped_item(properties, skip_path, progress: Optional[Callable]=None, recursive=True, mp=None):
    if "skip_type" not in properties:
        return properties
    writer = FArchiveWriter(PALWORLD_CUSTOM_PROPERTIES)
    if properties["skip_type"] == "ArrayProperty":
        writer.fstring(properties["array_type"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties['value'])
    elif properties["skip_type"] == "MapProperty":
        writer.fstring(properties["key_type"])
        writer.fstring(properties["value_type"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
    elif properties["skip_type"] == "StructProperty":
        writer.fstring(properties["struct_type"])
        writer.guid(properties["struct_id"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
    keep_custom_type = False
    if recursive:
        localProperties = copy.deepcopy(PALWORLD_CUSTOM_PROPERTIES)
    else:
        localProperties = copy.deepcopy(SKP_PALWORLD_CUSTOM_PROPERTIES)
    if ".worldSaveData.%s" % skip_path in PALWORLD_CUSTOM_PROPERTIES:
        localProperties[".worldSaveData.%s" % skip_path] = PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.%s" % skip_path]
        keep_custom_type = True
    elif ".worldSaveData.%s" % skip_path in localProperties:
        del localProperties[".worldSaveData.%s" % skip_path]
    with FProgressArchiveReader(
            writer.bytes(), PALWORLD_TYPE_HINTS,
            localProperties,
            reduce_memory=mp is None
    ) as reader:
        if progress is not None:
            progress(reader, len(properties['value']))
        if reader.mp_loading and mp is not None and properties["skip_type"] == "MapProperty":
            mp[f".worldSaveData.{skip_path}"] = reader.load_mp_map(properties, f".worldSaveData.{skip_path}",
                                                                   len(properties['value']))
        elif reader.mp_loading and mp is not None and properties["skip_type"] == "ArrayProperty":
            mp[f".worldSaveData.{skip_path}"] = reader.load_mp_array(properties, f".worldSaveData.{skip_path}",
                                                                     len(properties['value']))
        else:
            decoded_properties = reader.property(properties["skip_type"], len(properties['value']),
                                                 ".worldSaveData.%s" % skip_path)
            for k in decoded_properties:
                properties[k] = decoded_properties[k]
    if not keep_custom_type:
        del properties['custom_type']
    del properties["skip_type"]
    return properties
class MPProgressReader:
    def __init__(self, proc):
        self.mp_ctx = {}
        self.proc = proc
        self.loaded_size = 0
    def add(self, path, reader, size):
        self.mp_ctx[path] = (reader, size)
    def start(self):
        if len(self.mp_ctx) == 0:
            return
        if self.proc is None:
            return
        self.proc(self, reduce(lambda x, y: x + y[1], self.mp_ctx.values(), 0))
    def progress_eof(self):
        return len(self.mp_ctx) == 0
    def progress(self):
        t_proc = 0
        del_mp_path = []
        for mp_path, ctx in self.mp_ctx.items():
            prog = ctx[0].progress()
            if ctx[0].progress_eof():
                self.loaded_size += ctx[1]
                del_mp_path.append(mp_path)
            else:
                t_proc += prog
        for mp_path in del_mp_path:
            del self.mp_ctx[mp_path]
        return self.loaded_size + t_proc
    def eof(self):
        return len(self.mp_ctx) == 0
def BatchParseItem(_worldSaveData, skip_paths, recursive=True, progress=None, use_mp=True):
    if isinstance(skip_paths, str):
        skip_paths = [skip_paths]
    mp = {}
    t2 = time.time()
    parsed = 0
    skip_paths.sort()
    mp_ctx = MPProgressReader(progress)
    if use_mp:
        mp_items = filter(lambda x: not f".worldSaveData.{x}" in PALWORLD_CUSTOM_PROPERTIES, skip_paths)
        skip_paths = filter(lambda x: f".worldSaveData.{x}" in PALWORLD_CUSTOM_PROPERTIES, skip_paths)
        for skip_path in mp_items:
            properties = _worldSaveData[skip_path]
            if "skip_type" not in properties:
                continue
            parsed += 1
            parse_skiped_item(properties, skip_path,
                    progress=lambda reader, size: mp_ctx.add(skip_path, reader, size),
                    recursive=recursive, mp=mp)
    for skip_path in skip_paths:
        properties = _worldSaveData[skip_path]
        if "skip_type" not in properties:
            continue
        parsed += 1
        print("Parsing .worldSaveData.%s..." % skip_path, end="", flush=True)
        t1 = time.time()
        sub_mp = None if f".worldSaveData.{skip_path}" in PALWORLD_CUSTOM_PROPERTIES else (mp if use_mp else None)
        parse_skiped_item(properties, skip_path, progress, recursive, sub_mp)
        print("Done in %.2fs" % (time.time() - t1))
    mp_ctx.start()
    while mp is not None and len(mp.keys()) > 0:
        s = len(mp.keys())
        for mp_path in mp:
            mp[mp_path].join(timeout=0)
            t3 = time.time() - t2
            if mp[mp_path].is_alive():
                continue
            if mp_path in PALWORLD_CUSTOM_PROPERTIES:
                with FProgressArchiveReader(
                        b"", PALWORLD_TYPE_HINTS,
                        PALWORLD_CUSTOM_PROPERTIES
                ) as reader:
                    reader.fallbackData = _worldSaveData[mp_path[15:]]
                    _worldSaveData[mp_path[15:]] = PALWORLD_CUSTOM_PROPERTIES[mp_path][0](reader,
                                                                                          _worldSaveData[mp_path[15:]][
                                                                                              'type'], -1, mp_path)
                    _worldSaveData[mp_path[15:]]["custom_type"] = mp_path
            print("Loading %s in %.2fs, extra parse %.2fs" % (mp_path, t3, time.time() - t2 - t3))
            del mp[mp_path]
            break
        if len(mp.keys()) - s == 0:
            time.sleep(0.01)
    if parsed > 0:
        print("Parse skipped data in %.2fs" % (time.time() - t2))
SKP_PALWORLD_CUSTOM_PROPERTIES = copy.deepcopy(PALWORLD_CUSTOM_PROPERTIES)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.MapObjectSaveData"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.MapObjectSaveData.MapObjectSaveData.WorldLocation"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.MapObjectSaveData.MapObjectSaveData.WorldRotation"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.MapObjectSaveData.MapObjectSaveData.Model.Value.EffectMap"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.MapObjectSaveData.MapObjectSaveData.WorldScale3D"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.FoliageGridSaveDataMap"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.MapObjectSpawnerInStageSaveData"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.DynamicItemSaveData"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.CharacterContainerSaveData"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.CharacterContainerSaveData.Value.Slots"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.CharacterContainerSaveData.Value.RawData"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.ItemContainerSaveData"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.ItemContainerSaveData.Value.BelongInfo"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.ItemContainerSaveData.Value.Slots"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.ItemContainerSaveData.Value.RawData"] = (skip_decode, skip_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.GroupSaveDataMap"] = (group_decode, group_encode)
SKP_PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.GroupSaveDataMap.Value.RawData"] = (skip_decode, skip_encode)