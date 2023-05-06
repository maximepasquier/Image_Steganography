from ctypes import *
x = 173.3125
bits = cast(pointer(c_float(x)), POINTER(c_int32)).contents.value
print(hex(bits))
#swap the least significant bit
print(bits)
bits ^= 1
print(bits)
y = cast(pointer(c_int32(bits)), POINTER(c_float)).contents.value
print(y)