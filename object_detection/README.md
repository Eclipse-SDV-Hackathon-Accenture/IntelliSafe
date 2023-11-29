# Object Detection and Distance Estimation Script

This script is designed for object detection and distance estimation in a video using the YOLOv5 model. It also provides collision warnings based on the detected object's distance.

## Libraries Used
- **cv2**: OpenCV library for real-time computer vision.
- **torch**: PyTorch library for deep learning.
- **numpy**: Library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.

## Code Explanation
1. The YOLOv5 model is loaded from the local path 'yolov5s.pt' using PyTorch's `torch.hub.load()` function.
2. A video is loaded using OpenCV's `cv2.VideoCapture()` function.
3. A VideoWriter object is created to save the processed video.
4. A polygonal Region of Interest (ROI) is defined using numpy's `np.array()` function.
5. The actual dimensions of the object and the focal length of the camera are defined.
6. Each frame of the video is processed in a while loop. If a frame cannot be read, the loop breaks.
7. The polygonal ROI is drawn on the frame using OpenCV's `cv2.polylines()` function.
8. The y-coordinates of three horizontal lines inside the ROI are calculated.
9. Object detection is performed on the frame using the loaded YOLOv5 model.
10. For each detected object, the bounding box's centroid is calculated. If the centroid is inside the polygon ROI, the distance to the object is calculated using the formula `(object_width * focal_length) / (xmax - xmin)`. The bounding box and the distance are drawn on the frame.
11. If the bounding box crosses any of the horizontal lines, a collision warning is displayed on the frame.
12. The processed frame is displayed using OpenCV's `cv2.imshow()` function and written to the output video using the `write()` function of the VideoWriter object.
13. The loop can be stopped by pressing 'q'.
14. At the end of the script, the video capture and writer objects are released, and all OpenCV windows are destroyed.

## Note
- The script assumes that the video and the YOLOv5 model are in the same directory as the script.
- The script is set to run on a CPU. To run it on a GPU, set to 0.
- The script uses a threshold score of 0.4 for object detection. Objects with a score below this threshold are ignored.
- The script provides four levels of collision warnings: 'FORWARD COLLISION WARNING', 'COLLISION WARNING SEVERE', 'PAY ATTENTION & TAKE CONTROL', and 'EMERGENCY STOPPING ..!!'. The level of the warning depends on the number of crossed lines.