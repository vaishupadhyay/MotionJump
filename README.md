# Motion Jump
#### Do you miss your old school space bar games? 

What if I tell you, you don't have to touch your keyboard to play, All you need for controling the game is your hand gesture. Isn't it cool?
I have used Python and OpenCV to achieve this. Just using Mac and webcam feed, I've made this small script to detect hand gestures and press the "Space bar" button automatically.

### Environment
| OS | MacOS Catalina 10.15.3 | 
|---|---|
| Platform | Python 3.8.3 | 

### Libraries used
* OpenCV 4.2.0
* Numpy 1.18.5
* PyAutoGUI 0.9.50

### Installation
```bash
pip3 install numpy pyautogui opencv-contrib-python
python3 MotionJump.py
```

When running the python file, you can expect to see the real time frame from your camera with a bounding rectangular framing your hand. The bounding rectangular will contain yellow circles corresponding to the fingertips and finger webbing.

### Execution:
1. Run the program and switch over to your browser and open an online space bar game. (Example: Pony Ride Game)
2. Keep your hand within the rectangle as you start. Move your hand to make the horse jump.

> **Note:** To increase accuracy of gesture recognition, it is recommended to run the code in a bright light room. Additionally, the code can analyse one hand (either left or right), and the hand needs to be in front of the camera.

### References & Tutorials
* OpenCV documentation: http://docs.opencv.org/2.4.13/
* OpenCv python hand gesture recognition: http://creat-tabu.blogspot.com/2013/08/opencv-python-hand-gesture-recognition.html