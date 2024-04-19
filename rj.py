import multiprocessing.shared_memory as shm
import struct
import json

def getJson(sharedBuf,offset):
    # 读取共享内存中的数据
    # 假设您知道数据的偏移值和长度或整个数据大小
    intSize = struct.calcsize('i')  # 假设整个共享内存都是JSON数据
    
    print("begin to access")
    
    # 从共享内存读取数据
    jsonSize =int.from_bytes(sharedBuf.buf[offset:offset+intSize], byteorder='little')
    offset+=intSize
    
    print(jsonSize)
    
    # 从共享内存读取数据
    jsonDataBytes=sharedBuf.buf[offset:offset+jsonSize]
    offset+=jsonSize
    
    # 将bytes数据转换为字符串
    jsonData = jsonDataBytes.tobytes().decode('utf-8')
    
    # 加载JSON数据
    parsedJson = json.loads(jsonData)
    print("Received JSON data:", parsedJson)

   

# # 尝试访问共享内存
# sharedBuf = shm.SharedMemory(name="shared_image")
# # 读取共享内存中的数据
# # 假设您知道数据的偏移值和长度或整个数据大小
# offset = 0  # 数据起始位置
# length = struct.calcsize('i')  # 假设整个共享内存都是JSON数据
# 
# print("begin to access")
# 
# # 从共享内存读取数据
# jsonSize =int.from_bytes(sharedBuf.buf[offset:offset+length], byteorder='little')
# offset+=length
# 
# print(jsonSize)
# 
# # 从共享内存读取数据
# jsonDataBytes=sharedBuf.buf[offset:offset+jsonSize]
# offset+=jsonSize
# 
# # 将bytes数据转换为字符串
# jsonData = jsonDataBytes.tobytes().decode('utf-8')
# 
# # 加载JSON数据
# parsedJson = json.loads(jsonData)
# print("Received JSON data:", parsedJson)
# 
# while(True):
#     a=1

# # 清理，关闭共享内存
# sharedBuf.close()
# sharedBuf.unlink()



