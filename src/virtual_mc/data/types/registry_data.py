from typing import Optional
from .generic import Byteable_Object
from .numbers import Float, Int
from .string import String
from .boolean import Boolean

class SoundEvent(Byteable_Object):

    def __init__(self, sound_name: str, has_fixed_range: bool, fixed_range: Optional[float] = None):

        self.sound_name = sound_name
        self.has_fixed_range = has_fixed_range
        self.fixed_range = fixed_range

        if self.fixed_range is not None and not self.has_fixed_range:
            raise ValueError('Indicated non-fixed range, but fixed range was specified')

        if not isinstance(self.fixed_range, float):
            raise TypeError('Float needs to be specified for fixed range')

    def to_bytes(self):
        
        if self.fixed_range is not None and not self.has_fixed_range:
            raise ValueError('Indicated non-fixed range, but fixed range was specified')
        
        if not isinstance(self.fixed_range, float):
            raise TypeError('Float needs to be specified for fixed range')

        sound_name_bytes = String(self.sound_name).to_bytes()

        has_fixed_range_bytes = Boolean(self.has_fixed_range).to_bytes()

        if self.has_fixed_range:

            return sound_name_bytes + has_fixed_range_bytes + Float(self.fixed_range).to_bytes()
        
        return sound_name_bytes + has_fixed_range_bytes

class TeleportFlags(Byteable_Object):

    def __init__(self, rel_x: bool, rel_y: bool, rel_z: bool, rel_yaw: bool, rel_pitch: bool, rel_vel_x: bool, rel_vel_y: bool, rel_vel_z: bool, rel_rotation_vel: bool):

        self.rel_x = rel_x
        self.rel_y = rel_y
        self.rel_z = rel_z
        self.rel_yaw = rel_yaw
        self.rel_pitch = rel_pitch
        self.rel_vel_x = rel_vel_x
        self.rel_vel_y = rel_vel_y
        self.rel_vel_z = rel_vel_z
        self.rel_rotation_vel = rel_rotation_vel
    
    def to_bytes(self):
        
        tally = 0

        tally += 0x1 if self.rel_x else 0
        tally += 0x2 if self.rel_y else 0
        tally += 0x4 if self.rel_z else 0
        tally += 0x8 if self.rel_yaw else 0
        tally += 0x10 if self.rel_pitch else 0
        tally += 0x20 if self.rel_vel_x else 0
        tally += 0x40 if self.rel_vel_y else 0
        tally += 0x80 if self.rel_vel_z else 0
        tally += 0x100 if self.rel_rotation_vel else 0

        return Int(tally).to_bytes()
