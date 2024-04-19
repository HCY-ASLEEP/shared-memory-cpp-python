#include <opencv2/opencv.hpp>
#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <semaphore.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <rapidjson/document.h>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>

class shareMemoryAdapter {
  private:
    boost::interprocess::shared_memory_object shm;
    boost::interprocess::mapped_region region;
    char* shmp; // share memory pointer
    sem_t* empty;
    sem_t* full;
    int offset;
    void write(cv::Mat& mat) {
        int size= mat.total() * mat.elemSize();

        // Write image dimensions to shared memory
        int* dimensions = (int*)(shmp + offset);
        dimensions[0] = mat.rows;     // Height
        dimensions[1] = mat.cols;     // Width
        dimensions[2] = mat.channels(); // Channels
        offset+=sizeof(int)*3;

        std::cout<<dimensions[0]<<std::endl;
        std::cout<<dimensions[1]<<std::endl;
        std::cout<<dimensions[2]<<std::endl;
        std::cout<<"----------------"<<std::endl;
        std::cout<<offset<<std::endl;
        
        // Copy image data to shared memory
        std::memcpy(shmp + offset, mat.data, size);
        offset+=size;
        
        std::cout<<size<<std::endl;
        std::cout<<offset<<std::endl;

    }
    void write(rapidjson::Document& doc) {
        // Convert JSON document to string
        rapidjson::StringBuffer buffer;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
        doc.Accept(writer);
        std::string data = buffer.GetString();
        int size=data.size();

        std::cout<<size<<std::endl;

        // Write size
        int* head=(int*)(shmp+offset);
        head[0]=size;
        offset+=sizeof(int);

        // Write JSON data to shared memory
        std::memcpy(shmp+offset, data.c_str(), size);
        offset+=size;
        

        std::cout<<offset<<std::endl;
    }

  public:
    shareMemoryAdapter(const char* shmName,const int size,const char* semEmptyName,const char* semFullName) {
        // Set access flags
        auto flags=boost::interprocess::open_or_create;
        // Set access mode
        auto mode=boost::interprocess::read_write;
        // Create/Open shared memory
        shm=std::move(boost::interprocess::shared_memory_object(flags, shmName, mode));
        // Adjust size as needed
        shm.truncate(size);
        // Map the whole shared memory in this process
        region=std::move(boost::interprocess::mapped_region(shm,mode));
        // Get share memory pointer
        shmp=static_cast<char*>(region.get_address());
        // create semaphore
        // 0664 : access ,means rw-rw-r--
        empty = sem_open(semEmptyName,O_CREAT,0664,1);
        full = sem_open(semFullName,O_CREAT,0664,0);
        // occupied offset
        offset=0;
    }
    void clear() {
        offset=0;
    }
    void write(rapidjson::Document& jsonDoc, cv::Mat& mat) {
        // Waiting for empty buffer
        sem_wait(empty);
        
        // Write into shm
        write(jsonDoc);
        write(mat);
        
        // Signal full buffer
        sem_post(full);

    }
};


int main() {
    shareMemoryAdapter shm("shared_image",2000000,"cpp2python-empty","cpp2python-full");

    // OpenCV operations
    cv::Mat image = cv::imread("/home/devenv/2024-01-19_13-35.png");
    
    // Create RapidJSON document
    rapidjson::Document doc;
    doc.SetObject();

    // Add data to JSON document
    rapidjson::Value key("name");
    rapidjson::Value value("John");
    doc.AddMember(key, value, doc.GetAllocator());

    shm.clear();
    shm.write(doc,image);
    
    while(true);
}

/*
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
    void* p=region.get_address();
    int* dimensions = static_cast<int*>(p);
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
*/
