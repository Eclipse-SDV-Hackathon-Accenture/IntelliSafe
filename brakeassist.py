import cv2
import torch
import numpy as np


# Function to get a warning message based on speed and crossed line
def get_warning_message(speed, max_crossed_line):
    # Implementation of the logic to determine the warning message based on speed and crossed line
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

# Function to handle crossed lines and display warning messages
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


# Class for Brake Assist functionality
class BrakeAssist:
    def __init__(self, model_path, video_path, output_path):
        # Initialization of variables and YOLO model
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
        cv2.imshow("Video", frame)
        self.output.write(frame)