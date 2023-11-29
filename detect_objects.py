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

import cv2
import torch
import numpy as np
import matplotlib.image as mpimg
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

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
        self.dist_ = 12

    def process_frame(self, frame, line_ys, line_colors, crossed_lines):
        results = self.model(frame, size=320)
        detections = results.pred[0]

        height, width, _ = frame.shape
        cv2.line(frame, (width // 2, 0), (width // 2, height), (160, 160, 160), 2)

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

        return frame, crossed_lines

    def process_video(self, frame):
        # while True:
            # success, frame = self.video.read()
        frame = cv2.resize(frame, (1280, 720))
        # if not success:
        #     break

        cv2.polylines(frame, [self.roi_points], True, (0, 200, 0), 2)
        line_y1 = 600
        line_gap = 10
        line_ys = [line_y1 + i * line_gap for i in range(self.dist_)]
        line_colors = [(255, 0, 0) for _ in range(self.dist_)]
        crossed_lines = []

        frame, crossed_lines = self.process_frame(frame, line_ys, line_colors, crossed_lines)

        if crossed_lines:
            cv2.putText(frame, 'BRAKE', (1000 - 25, 100 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            crossed_lines_str = ', '.join(str(line_num) for line_num in crossed_lines)
            cv2.putText(frame, str(max(crossed_lines)), (1000, 100 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            if 4 <= max(crossed_lines) <= 5:
                cv2.putText(frame, 'FORWARD COLLISION WARNING', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2,
                            cv2.LINE_AA)
            elif 6 <= max(crossed_lines) <= 8:
                cv2.putText(frame, 'COLLISION WARNING SEVERE', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2,
                            cv2.LINE_AA)
            elif 9 <= max(crossed_lines) <= 11:
                cv2.putText(frame, 'PAY ATTENTION & TAKE CONTROL', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2,
                            cv2.LINE_AA)
            elif max(crossed_lines) >= 11:
                cv2.putText(frame, 'EMERGENCY STOPPING ..!!', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2,
                            cv2.LINE_AA)

        cv2.imshow("Video", frame)
        self.output.write(frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break


def callback1(topic_name, compressed_image, time):
    img = mpimg.imread(io.BytesIO(compressed_image.data), format=compressed_image.format)
    processor.process_video(img)
    cv2.waitKey(1)

ecal_core.initialize([], "CompressedImageSubscriber")
sub = ProtoSubscriber("ROSFrontCenterImage", CompressedImage_pb2.CompressedImage)
processor = BrakeAssist('yolov5s.pt', '20231128-1516-56.7048286.mp4', 'intelli_safe_output.mp4')
sub.set_callback(callback1)
processor.video.release()
processor.output.release()
cv2.destroyAllWindows()
while ecal_core.ok():
    time.sleep(10)
ecal_core.finalize()

