# Stop Motion Python Script
This project allows user to easily create stop motion animations by capturing frame-by-frame webcam video. It was developed to work with a keyboard or external buttons connected to Raspberry Pi GPIO's as command triggers. Although it's Raspberry Pi based, can be modified to work at any machine with Python terminal.

### Applications
- Education
- Entertainment
- Infinity and Beyond...

### Cloning and Running
Clone the code opening the terminal in any folder and running:
```
$ sudo git clone https://github.com/dlavino/stopmotion.git
```
A new directory called *stopmotion* is created, run the following command line to enter directory and run the script:
```
$ sudo python stopmotion/stopmotion.py
```

## Software Requirements
The script was written and tested using Raspberry Pi 3 Model B running Raspbian GNU/Linux 8 (jessie) and Python 2.7.9 (native in this version of Raspbian). Previous versions of Raspberry Pi may be subject to lack of performance.
Due to multithreading tasks and some graphical processes the script uses some third open-source libraries which are not native at Python. The non-native libraries used in this version of the script is listed right below:
- [OpenCV](https://github.com/opencv/opencv)
- [numpy](https://github.com/numpy/numpy)
- [imutils](https://github.com/jrosebr1/imutils)

### Instalation
All the packages are completely `pip`-installable. If it's not already installed, open the terminal and run the following codes (internet connection is required):
```
$ sudo pip install opencv
```
```
$ sudo pip install numpy
```
```
$ sudo pip install imutils
```
Also certify that you have GPIO Module already installed, if you're not sure try to install it:
```
$ sudo apt-get install python-rpi.gpio
```
## Hardware Requirements
The script works well in 1280 x 720 screen resolution, although, the interface is screen adaptible, so you don't need to care too much about it. You can also change Raspbian system resolution to verify which one's fits better to your purpose.
Mouse and keyboard are necessary to perform the steps above. During the execution only external buttons connected to GPIO pins of the Raspberry are needed to interact with the program.

## Commands
Keyboard keys and Raspberry GPIO pins perform same functions inside the program routine. GPIO pins are already pulled-down, so when connecting GPIO pins to phisical buttons you just need to apply referenced 3.3V to it.
The table bellow shows all available commands, keys and GPIO's associated each self.

| Command | Description | Keyboard Key | GPIO pin |
| --- | --- | --- | --- |
| CAPTURE | Pick current frame of the video and add to the sequence or back to *capture mode* when playing a sequence | `c` | `6` |
| UNDO | Delete last frame of the sequence | `a` | `17` |
| PLAY | Play sequence animation | `p` | `5` |
| RESET | Delete all frames | `r` | `4` |
| INCREASE SPEED | Increase animation FPS | `m` | `-` |
| DECREASE SPEED | Decrease animation FPS | `n` | `-` |
| QUIT | Exit application | `q` | `-` |




