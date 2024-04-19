#include <opencv2/opencv.hpp>
#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <semaphore.h>
#include <fcntl.h>
#include <sys/stat.h>

int main() {
    // Create/Open shared memory
    boost::interprocess::shared_memory_object shm(boost::interprocess::open_or_create, "shared_image", boost::interprocess::read_write);
    shm.truncate(2000000); // Adjust size as needed

    // Map the whole shared memory in this process
    boost::interprocess::mapped_region region(shm, boost::interprocess::read_write);

    // OpenCV operations
    cv::Mat image = cv::imread("/home/devenv/2024-01-19_13-35.png");
    
    // create semaphore
    // 0664 : access ,means rw-rw-r--
    sem_t* empty = sem_open("cpp2python-empty",O_CREAT,0664,1);
    sem_t* full = sem_open("cpp2python-full",O_CREAT,0664,0);
    
    // Waiting for empty buffer
    sem_wait(empty); 

    // Write image dimensions to shared memory
    int* dimensions = static_cast<int*>(region.get_address());
    dimensions[0] = image.rows;     // Height
    dimensions[1] = image.cols;     // Width
    dimensions[2] = image.channels(); // Channels
   
    // Copy image data to shared memory
    std::memcpy(static_cast<char*>(region.get_address()) + sizeof(int) * 3, image.data, image.total() * image.elemSize());
   
    // Signal full buffer
    sem_post(full);

    while(true) {}

    return 0;
}

