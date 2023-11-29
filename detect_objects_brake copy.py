import cv2
import torch
import numpy as np
import time
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import ros.sensor_msgs.CompressedImage_pb2 as CompressedImage_pb2
from PIL import Image
import io
import matplotlib.pyplot as plt
from ros.sensor_msgs import PointCloud2_pb2
import cv2
import torch
import numpy as np
import matplotlib.image as mpimg
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import SensorNearData.VehicleDynamics_pb2 as VehicleDynamics_pb2
import cv2
import torch
import numpy as np
import streamlit as st
import pandas as pd
import numpy as np

def streamlit():
    
    col1, col2, col3 = st.columns(3)
    with col1:
        print("hi")

    with col2:
        l = [[48.1175451,11.6026423,5], [48.1175451,11.6056423,5 ],[48.1175451,11.6026423,100]]
        df = pd.DataFrame(l, columns=['lat', 'lon',"sizes"])
        df['colors']= np.random.rand(3).tolist()
        
        st.map(df, latitude='lat', longitude='lon',size="sizes")
        # st.markdown(page_bg_img, unsafe_allow_html=True)
        
    with col3:
        print("hi")

speed_global = 0

def get_warning_message(speed, max_crossed_line):
    if speed < 4:
        if 4 <= max_crossed_line <= 5:
            return 'FORWARD COLLISION WARNING'
        elif 6 <= max_crossed_line <= 8:
            return 'COLLISION WARNING SEVERE'
        elif 9 <= max_crossed_line <= 11:
            return 'PAY ATTENTION & TAKE CONTROL'
        elif max_crossed_line >= 11:
            return 'EMERGENCY STOPPING ..!!'
    elif 4 <= speed < 8:
        if 5 <= max_crossed_line <= 6:
            return 'FORWARD COLLISION WARNING'
        elif 7 <= max_crossed_line <= 9:
            return 'COLLISION WARNING SEVERE'
        elif 10 <= max_crossed_line <= 12:
            return 'PAY ATTENTION & TAKE CONTROL'
        elif max_crossed_line >= 12:
            return 'EMERGENCY STOPPING ..!!'
    else:
        if 6 <= max_crossed_line <= 7:
            return 'FORWARD COLLISION WARNING'
        elif 8 <= max_crossed_line <= 10:
            return 'COLLISION WARNING SEVERE'
        elif 11 <= max_crossed_line <= 13:
            return 'PAY ATTENTION & TAKE CONTROL'
        elif max_crossed_line >= 13:
            return 'EMERGENCY STOPPING ..!!'


def handle_crossed_lines(frame, crossed_lines, speed):
    if crossed_lines:
        cv2.putText(frame, 'BRAKE', (1000 - 25, 100 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        crossed_lines_str = ', '.join(str(line_num) for line_num in crossed_lines)
        cv2.putText(frame, str(max(crossed_lines)), (1000, 100 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255),
                    2)

        warning_message = get_warning_message(speed, max(crossed_lines))
        if warning_message:
            cv2.putText(frame, warning_message, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2,
                        cv2.LINE_AA)
    return frame


# def create_gif():
#     videoClip = VideoFileClip("intelli_safe_output.mp4")

#     clip_resized = videoClip.resize(height=320)  # Resize the video
#     clip_speed_up = clip_resized.fx(vfx.speedx, 2)

#     clip_speed_up.write_gif("intelli_safe_output.gif")


class BrakeAssist:
    def __init__(self, model_path, video_path, output_path):
        self.device = "cpu"
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        self.model.to(self.device)
        self.video = cv2.VideoCapture(video_path)
        self.width, self.height = 1280, 720
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.output = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width, self.height))
        self.roi_points = np.array([[400, 720], [400, 400], [870, 400], [870, 720]], np.int32)
        self.object_width = 50
        self.focal_length = 1000
        self.dist_ = 35
        self.line_y1 = 600
        self.speed = 0
        self.prev_speed = 0

    def process_frame(self, frame, crossed_lines, speed, prev_speed):
        results = self.model(frame, size=320)
        detections = results.pred[0]

        height, width, _ = frame.shape
        cv2.line(frame, (width // 2, 0), (width // 2, height), (160, 160, 160), 2)

        if abs(speed - prev_speed) >= 0.5:
            if 410 <= self.line_y1 <= 600:
                if speed > prev_speed:
                    self.line_y1 -= 10
                else:
                    self.line_y1 += 10
                prev_speed = speed

        line_gap = 10
        line_ys = [self.line_y1 + i * line_gap for i in range(self.dist_)]
        line_colors = [(255, 0, 0) for _ in range(self.dist_)]

        for detection in detections:
            xmin = detection[0]
            ymin = detection[1]
            xmax = detection[2]
            ymax = detection[3]
            score = detection[4]
            class_id = detection[5]

            if score >= 0.4:
                if xmin < frame.shape[1] // 2:
                    centroid_x = int(xmax)
                    centroid_y = int(ymax)
                else:
                    centroid_x = int(xmin)
                    centroid_y = int(ymax)

                if cv2.pointPolygonTest(self.roi_points, (centroid_x, centroid_y), False) > 0:
                    cv2.circle(frame, (centroid_x, centroid_y), 5, (0, 255, 0), -1)

                    for i, line_y in enumerate(line_ys):
                        if ymax >= line_y:
                            line_colors[i] = (0, 0, 255)
                            crossed_lines.append(i + 1)

                    distance = (self.object_width * self.focal_length) / (xmax - xmin)
                    cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 0, 255), 2)
                    cv2.putText(frame, f"Dist: {distance:.2f} cm", (int(xmin), int(ymin) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
                else:
                    cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)

        for line_y, color in zip(line_ys, line_colors):
            cv2.line(frame, (self.roi_points[0][0], line_y), (self.roi_points[2][0], line_y), color, 2)

        return frame, crossed_lines, prev_speed


    def process_video(self, frame):
        speed = self.speed
        prev_speed = self.prev_speed
        frame = cv2.resize(frame, (1280, 720))

        cv2.polylines(frame, [self.roi_points], True, (0, 200, 0), 2)

        crossed_lines = []

        frame, crossed_lines, prev_speed = self.process_frame(frame, crossed_lines, speed, prev_speed)
        frame = handle_crossed_lines(frame, crossed_lines, speed)
        self.prev_speed = prev_speed
        print("2", speed, prev_speed)
        cv2.imshow("Video", frame)
        self.output.write(frame)

def callback1(topic_name, compressed_image, time):
    img = mpimg.imread(io.BytesIO(compressed_image.data), format=compressed_image.format)
    processor.process_video(img)
    cv2.waitKey(1)



def callback_speed(topic_name, vehicle_dynamics, time):
    processor.speed = vehicle_dynamics.signals.speed
    # speed_list = []
    # speed_list.append(vehicle_dynamics.signals.speed)
    # print("speed_global callbackspeed",speed_global)
    # print("speed_global callbackspeed",vehicle_dynamics.signals.speed)
    # print("len of the list:", len(speed_list))

def callback2(topic_name, point_cloud, time):
    # print("Received PointCloud2:")
    # print("Header:", point_cloud.header)
    # print("Height:", point_cloud.height)
    # print("Width:", point_cloud.width)
    # print("Fields:", point_cloud.fields)
    # print("Is Big Endian:", point_cloud.is_bigendian)
    # print("Point Step:", point_cloud.point_step)
    # print("Row Step:", point_cloud.row_step)
    # print("Data Length:", len(point_cloud.data))
    print("Is Dense:", point_cloud.is_dense)



ecal_core.initialize([], "CompressedImageSubscriber")
sub = ProtoSubscriber("ROSFrontCenterImage", CompressedImage_pb2.CompressedImage)
processor = BrakeAssist('yolov5s.pt', '20231128-1516-56.7048286.mp4', 'intelli_safe_output.mp4')
sub2 = ProtoSubscriber("ROSVLS128CenterCenterRoof", PointCloud2_pb2.PointCloud2)
sub3 = ProtoSubscriber("VehicleDynamicsInPb", VehicleDynamics_pb2.VehicleDynamics)
sub3.set_callback(callback_speed)
sub2.set_callback(callback2)
sub.set_callback(callback1)
streamlit()
processor.video.release()
processor.output.release()
cv2.destroyAllWindows()
while ecal_core.ok():
    time.sleep(10)
ecal_core.finalize()

