import pyrealsense2 as rs
import numpy as np
import cv2
import time
from datetime import datetime
import open3d as o3d
import os

def funcCapture(pipeline,contours):
    capture_duration = 16
    color = True
    counter = 0

    date = datetime.now().strftime("%d_%m_%Y-%I:%M:%S_%p")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'./Data/save_{date}.avi', fourcc, 30.0, (640, 480))

    start_time = time.time()
    while (int(time.time() - start_time) < capture_duration):
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()

        depth_frame = frames.get_depth_frame()
        depth_frame = decimate.process(depth_frame)

        depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())

        save_imgs = np.asanyarray(frame.get_data())

        if color:
            mapped_frame, color_source = frame, save_imgs
        else:
            mapped_frame, color_source = depth_frame, depth_colormap

        points = pc.calculate(depth_frame)
        pc.map_to(mapped_frame)

        # if np.shape(frame) != ():
            # frame = cv2.flip(frame,0)

        if counter in [75,150,225,300]:
            date_f = date
            points.export_to_ply(f'./Data/save_{date_f}_{counter}.ply', mapped_frame)
            pcd = o3d.io.read_triangle_mesh(f"./Data/save_{date_f}_{counter}.ply")
            o3d.io.write_triangle_mesh(f"./Data/save_{date_f}_{counter}.off", pcd)
            os.remove(f"./Data/save_{date_f}_{counter}.ply")
        counter += 1

        out.write(save_imgs)
        cv2.putText(save_imgs, 'Motion Detection & Recoding', (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_4)
        # cv2.drawContours(save_imgs, contours, -1, (0, 255, 0), 2)
        cv2.imshow('RealSense', save_imgs)
        key = cv2.waitKey(20)
        if key == ord('q'):
            break
    return 0


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break

if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

pc = rs.pointcloud()
decimate = rs.decimation_filter()
decimate.set_option(rs.option.filter_magnitude, 2 ** 1)
colorizer = rs.colorizer()

cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

capture_duration = 16

motionFound = 0



try:
    while True:
        frames = pipeline.wait_for_frames()
        prev = frames.get_color_frame()

        time.sleep(0.1)
        frames2 = pipeline.wait_for_frames()
        curr = frames2.get_color_frame()

        prev_color_image = np.asanyarray(prev.get_data())

        color_image = np.asanyarray(curr.get_data())

        diff = cv2.absdiff(prev_color_image, color_image)

        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        diff_blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)

        _, thresh_bin = cv2.threshold(diff_blur, 50, 255, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(thresh_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        font = cv2.FONT_HERSHEY_SIMPLEX

        print(len(contours))

        if len(contours) <= 30:
            cv2.putText(prev_color_image, 'Motion Not Detection', (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
            motionFound = 0
        else:
            cv2.putText(prev_color_image, 'Motion Detection', (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_4)
            motionFound = 1

        if motionFound == 1:
            motionFound = funcCapture(pipeline, contours)

        cv2.drawContours(prev_color_image, contours, -1, (0, 255, 0), 2)

        cv2.imshow('RealSense', prev_color_image)

        key = cv2.waitKey(20)
        if key == ord('q'):
            break
finally:
    # Stop streaming
    pipeline.stop()