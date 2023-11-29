# Object Detection and Distance Estimation Script

This script is designed for object detection and distance estimation in a video using the YOLOv5 model. It also provides collision warnings based on the detected object's distance.

## Libraries Used
- **cv2**: OpenCV library for real-time computer vision.
- **torch**: PyTorch library for deep learning.
- **numpy**: Library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.

## Code Explanation
The script contains a `BrakeAssist` class that handles the processing of the video frames and the detection of objects. The class uses a pre-trained YOLOv5 model to detect objects in each frame of the video. The detected objects are then processed to calculate their distance from the vehicle. Based on the calculated distance and the speed of the vehicle, the system provides appropriate warning messages.

The code also adjusts the sentivity of the system based on speed of the car, making it more sensitive when the speed are high since brakes need to be applied sooner on high speeds.

The `process_frame` method process each frame of the video.

The `get_warning_message` function is used to generate the warning messages based on the speed of the vehicle and the maximum crossed line.

The `handle_crossed_lines` function is used to display the warning messages on the video frame.

## Usage

To use the script, create an instance of the `BrakeAssist` class by providing the path to the pre-trained YOLOv5 model, the path to the input video, and the path to the output video. Then, call the `process_video` method on the created instance.

```python
processor = BrakeAssist('yolov5s.pt', 'input.mp4', 'intelli_safe_output.mp4')
processor.process_video()
```

## Note
- The script assumes that the video and the YOLOv5 model are in the same directory as the script.
- The script is set to run on a CPU. To run it on a GPU, set to 0.
- The script uses a threshold score of 0.4 for object detection. Objects with a score below this threshold are ignored.
- The script provides four levels of collision warnings: 'FORWARD COLLISION WARNING', 'COLLISION WARNING SEVERE', 'PAY ATTENTION & TAKE CONTROL', and 'EMERGENCY STOPPING ..!!'. The level of the warning depends on the number of crossed lines.
