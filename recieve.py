import cv2
import numpy as np
import multiprocessing.shared_memory as shm

# Attach to the shared memory
shared_img = shm.SharedMemory(name="shared_image")

# Read image dimensions from shared memory
dimensions = np.ndarray((3,), dtype=np.int32, buffer=shared_img.buf)

# Read image data from shared memory
height, width, channels = dimensions
data_offset = 3 * dimensions.dtype.itemsize  # Calculate the offset for image data
image_data = np.ndarray((height, width, channels), dtype=np.uint8, buffer=shared_img.buf, offset=data_offset)
cv2.imshow("Image from C++", image_data)
cv2.waitKey(0)

# Clean up
shared_img.close()
shared_img.unlink()
