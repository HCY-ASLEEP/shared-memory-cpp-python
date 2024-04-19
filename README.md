### Dependency
- rapid-json
    ```bash
    sudo apt install rapidjson-dev
    ```
- opencv
    ```bash
    sudo apt install libopencv-dev
    ```
- boost
    ```bash
    sudo apt-get install libboost-all-dev
    ```
### Compile
```bash
g++ send.cpp -o send.exe -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_imgcodecs
```
