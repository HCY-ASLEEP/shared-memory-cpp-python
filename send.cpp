#include <opencv2/opencv.hpp>
#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>

int main() {
    // Create/Open shared memory
    boost::interprocess::shared_memory_object shm(boost::interprocess::open_or_create, "shared_image", boost::interprocess::read_write);
    shm.truncate(2000000); // Adjust size as needed

    // Map the whole shared memory in this process
    boost::interprocess::mapped_region region(shm, boost::interprocess::read_write);

    // OpenCV operations
    cv::Mat image = cv::imread("/home/devenv/2024-01-19_13-35.png");

    // Write image dimensions to shared memory
    int* dimensions = static_cast<int*>(region.get_address());
    dimensions[0] = image.rows;     // Height
    dimensions[1] = image.cols;     // Width
    dimensions[2] = image.channels(); // Channels

    std::cout<<dimensions[0]<<std::endl;
    std::cout<<dimensions[1]<<std::endl;
    std::cout<<dimensions[2]<<std::endl;
    std::cout<<image.total() * image.elemSize()<<std::endl;
    // Copy image data to shared memory
    std::memcpy(static_cast<char*>(region.get_address()) + sizeof(int) * 3, image.data, image.total() * image.elemSize());
    // std::cout<<dimensions[0]<<std::endl;
    // std::cout<<dimensions[1]<<std::endl;
    // std::cout<<dimensions[2]<<std::endl;

    while(true) {}

    return 0;
}
