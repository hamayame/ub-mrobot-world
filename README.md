UB Mobile Robotic World on Indigo
=============

Package ini saya buat untuk dapat digunakan dalam pembelajaran mata kuliah Mobile Robotics Fakultas Ilmu Komputer

Package ini dependan dengan beberapa package lain antara lain:
1.tum_simulator (https://github.com/dougvk/tum_simulator)
2.cmvision (https://github.com/kbogert/cmvision/tree/indigo-devel)
3.ardrone-autonomy (https://ardrone-autonomy.readthedocs.io/en/latest/index.html)

Cara memasang package ini:
1.Menuju ke folder workspace yang digunakan dengan ROS
    ```
    cd  (alamat folder workspace)/src
    ```
2.Unduh package dan dependensi package
    ```
    git clone 
    cd ..
    rosdep install --from-paths src --ignore-src --rosdistro indigo -y
    ```
3.Build package
    ```
    catkin_make
    ```
4.Source environment ROS
    ```
    source devel/setup.bash
    ```
