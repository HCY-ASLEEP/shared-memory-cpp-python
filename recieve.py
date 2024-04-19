import cv2
import numpy as np
import multiprocessing.shared_memory as shm
import posix_ipc
import struct
import json

class a:
    def __init__(self,sharedBuf) -> None:
        self.shared=sharedBuf
        self.offset=0

    def getJson(self):
        # 读取共享内存中的数据
        # 假设您知道数据的偏移值和长度或整个数据大小
        intSize = struct.calcsize('i')  # 假设整个共享内存都是JSON数据
        
        print("begin to access")
        
        # 从共享内存读取数据
        jsonSize =int.from_bytes(self.shared.buf[self.offset:self.offset+intSize], byteorder='little')
        self.offset+=intSize
        
        print(jsonSize)
        
        # 从共享内存读取数据
        jsonDataBytes=self.shared.buf[self.offset:self.offset+jsonSize]
        self.offset+=jsonSize
        
        # 将bytes数据转换为字符串
        jsonData = jsonDataBytes.tobytes().decode('utf-8')
        
        # 加载JSON数据
        parsedJson = json.loads(jsonData)
        print("Received JSON data:", parsedJson)
    
    def getImage(self):
        print(self.offset)
        # Read image dimensions from shared memory
        dimensions = np.ndarray((3,), dtype=np.int32, buffer=self.shared.buf, offset=self.offset)
        print(dimensions)
    
        # Read image data from shared memory
        height, width, channels = dimensions
        self.offset += 3 * dimensions.dtype.itemsize  # Calculate the offset for image data
        print(self.offset)
        image_data = np.ndarray((height, width, channels), dtype=np.uint8, buffer=self.shared.buf, offset=self.offset)
        self.offset += height*width*channels 
        cv2.imshow("Image from C++", image_data)
        cv2.waitKey(0)





# Attach to the shared memory
sharedBuf = shm.SharedMemory(name="shared_image")

empty = posix_ipc.Semaphore("cpp2python-empty")
full = posix_ipc.Semaphore("cpp2python-full")

print("full not acquired")

full.acquire()

print("full acquired")

b=a(sharedBuf)
b.getJson()
b.getImage()

empty.release()

# # Read image dimensions from shared memory
# dimensions = np.ndarray((3,), dtype=np.int32, buffer=sharedBuf.buf)
# 
# # Read image data from shared memory
# height, width, channels = dimensions
# data_offset = 3 * dimensions.dtype.itemsize  # Calculate the offset for image data
# image_data = np.ndarray((height, width, channels), dtype=np.uint8, buffer=sharedBuf.buf, offset=data_offset)
# 
# empty.release()
# 
# print("empty released")
# 
# cv2.imshow("Image from C++", image_data)
# cv2.waitKey(0)
# 
# # Clean up
# sharedBuf.close()
# sharedBuf.unlink()

