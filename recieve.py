import cv2
import numpy as np
import multiprocessing.shared_memory as shm
import posix_ipc
import json

class sharedMemoryAdapter:
    def __init__(self,shared) -> None:
        self.shared=shared
        self.offset=0

    def getJson(self):
        # 读取 json 文件的长度
        jsonSizes = np.ndarray((1,), dtype=np.int32, buffer=self.shared.buf, offset=self.offset)
        self.offset+=jsonSizes.dtype.itemsize
        jsonSize=jsonSizes[0]
        # 获取 json 的字节编码
        jsonDataBytes=self.shared.buf[self.offset:self.offset+jsonSize]
        self.offset+=jsonSize
        # 将bytes数据转换为字符串
        jsonData = jsonDataBytes.tobytes().decode('utf-8')
        # 加载JSON数据
        parsedJson = json.loads(jsonData)
        print("Received JSON data:", parsedJson)
    
    def getImage(self):
        # 获取图片的维度大小信息
        dimensions = np.ndarray((3,), dtype=np.int32, buffer=self.shared.buf, offset=self.offset)
        height, width, channels = dimensions
        self.offset += 3 * dimensions.dtype.itemsize
        # 获取图片
        image_data = np.ndarray((height, width, channels), dtype=np.uint8, buffer=self.shared.buf, offset=self.offset)
        self.offset += height*width*channels 
        cv2.imshow("Image from C++", image_data)
        key=cv2.waitKey(0)
        # 检查用户是否按下了 'q' 键，如果是则退出程序
        if key == ord('q'):
            cv2.destroyAllWindows()  # 关闭所有OpenCV窗口


if __name__=="__main__":
    # 关联到共享内存
    shared = shm.SharedMemory(name="shared_image_json")
    
    # 关联到信号量
    empty = posix_ipc.Semaphore("cpp2python-empty")
    full = posix_ipc.Semaphore("cpp2python-full")
    
    while(True):
        print("full not acquired")
        
        full.acquire()
        
        print("full acquired")
        
        shma=sharedMemoryAdapter(shared)
        shma.getJson()
        shma.getImage()
        
        empty.release()
    
    
