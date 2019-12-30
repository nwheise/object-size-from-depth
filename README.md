# realsense

## Install Instructions for macOS
Install dependencies with Homebrew:

    brew install libusb pkg-config
    brew install home
    brew/core/glfw3
    brew install cmake
    brew install librealsense

Then build the librealsense library from source:

    git clone https://github.com/IntelRealSense/librealsense
    cd librealsense
    mkdir build
    cd build
    cmake ../ -DBUILD_PYTHON_BINDINGS=TRUE
    make -j4
    sudo make install #Optional if you want the library to be installed in your system

Copy the ```.so``` files in the folder ```librealsense/build/wrappers/python/``` into the ```site-packages``` folder.