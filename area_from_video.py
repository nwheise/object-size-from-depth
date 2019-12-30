#!/usr/bin/env python3

import math

import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

pixels_h = 848
pixels_v = 480

config.enable_stream(rs.stream.depth, pixels_h, pixels_v, rs.format.z16, 30)
config.enable_stream(rs.stream.color, pixels_h, pixels_v, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

align = rs.align(rs.stream.color)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        pixel_too_far = depth_image > 750
        pixel_too_close = depth_image < 105  # min depth distance

        depth_image[pixel_too_far | pixel_too_close] = 0
        color_image[:][pixel_too_far | pixel_too_close] = 0

        fov_h = math.radians(87)
        fov_v = math.radians(58)

        pixel_width = (depth_image / pixels_h) * math.tan(fov_h / 2)
        pixel_height = (depth_image / pixels_v) * math.tan(fov_v / 2)
        pixel_area = pixel_width * pixel_height

        total_area = np.sum(pixel_area)

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET
        )

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))
        cv2.putText(
            images,
            f"Area: {total_area} sq. mm",
            (100, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 127, 255),
            2,
        )

        # Show images
        cv2.namedWindow("RealSense", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("RealSense", images)
        cv2.waitKey(50)
finally:
    # Stop streaming
    pipeline.stop()
