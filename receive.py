import cv2
import numpy as np
import multiprocessing.shared_memory as shm
import posix_ipc
import json

class sharedMemoryAdapter:
    def __init__(self,shared) -> None:
        self.shared=shared
        self.offset=0
        self.data={}
    
    def clear(self) -> None:
        self.offset=0
        self.data={}
        
    def readData(self)->dict:
        return self.data

    def readJson(self)->None:
        # 读取 json 文件的长度
        jsonSizes = np.ndarray((1,), dtype=np.int32, buffer=self.shared.buf, offset=self.offset)
        self.offset+=jsonSizes.dtype.itemsize
        jsonSize=jsonSizes[0]
        # 获取 json 的字节编码
        jsonByteData=self.shared.buf[self.offset:self.offset+jsonSize]
        self.offset+=jsonSize
        
        self.data['json']=jsonByteData

            
    def readImage(self)->None:
        # 获取图片的维度大小信息
        dimensions = np.ndarray((3,), dtype=np.int32, buffer=self.shared.buf, offset=self.offset)
        self.offset += 3 * dimensions.dtype.itemsize
        height, width, channels = dimensions
        # 获取图片
        mat = np.ndarray((height, width, channels), dtype=np.uint8, buffer=self.shared.buf, offset=self.offset)
        self.offset += height*width*channels 
        
        self.data['mat']=mat
        
        

if __name__=='__main__':
    shmName='shared_image_json'
    semEmpty='cpp2python-empty'
    # 关联到共享内存
    semFull='cpp2python-full'
    shared = shm.SharedMemory(name=shmName)
    # 关联到信号量
    empty = posix_ipc.Semaphore(semEmpty)
    full = posix_ipc.Semaphore(semFull)
    shma=sharedMemoryAdapter(shared)
    while(True):
        print('full not acquired')
        print(empty.value)
        print(full.value)

        shma.clear()

        full.acquire()
        
        shma.readJson()
        shma.readImage()
        
        empty.release()
        
        data=shma.readData()
        
        jsonByteData=data['json']
        # 将bytes数据转换为字符串
        jsonStrData = jsonByteData.tobytes().decode('utf-8')
        # 加载JSON数据
        parsedJson = json.loads(jsonStrData)
        print('Received JSON data:', parsedJson)
        
        mat=data['mat']
        # 展示图片
        cv2.imshow('Image from C++', mat)
        key=cv2.waitKey(0)
        # 检查用户是否按下了 'q' 键，如果是则退出程序
        if key == ord('q'):
            cv2.destroyAllWindows()  # 关闭所有OpenCV窗口



    
    
