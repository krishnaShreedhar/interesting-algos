import cv2
import numpy as np


class CircleDetector:

    def __init__(self,
                 hc_method=cv2.HOUGH_GRADIENT,
                 hc_dp=1,
                 hc_min_dist=20,
                 hc_circles=None,
                 hc_param1=50,
                 hc_param2=30,
                 hc_min_radius=1,
                 hc_max_radius=40):
        self.hc_method = hc_method
        self.hc_dp = hc_dp
        self.hc_min_dist = hc_min_dist
        self.hc_circles = hc_circles
        self.hc_param1 = hc_param1
        self.hc_param2 = hc_param2
        self.hc_min_radius = hc_min_radius
        self.hc_max_radius = hc_max_radius

    def print_details(self, file_path):
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        print(f"{file_path}: shape: {img.shape}, size: {img.size}, dtype: {img.dtype}")

    def detect_circles(self, file_path, do_blur=True):
        # Reading the image file
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        self.print_details(file_path)

        # Convert to grayscale.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if do_blur:
            # Blur using 3 * 3 kernel.
            gray_blurred = cv2.blur(gray, (3, 3))
        else:
            gray_blurred = gray

        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            method=self.hc_method,
                                            dp=self.hc_dp,
                                            minDist=self.hc_min_dist,
                                            circles=self.hc_circles,
                                            param1=self.hc_param1,
                                            param2=self.hc_param2,
                                            minRadius=self.hc_min_radius,
                                            maxRadius=self.hc_max_radius)

        print(f"Finished detecting circles.")
        # Draw circles that are detected.
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))
            print(f"#detected_circles: {len(detected_circles[0, :])}")
            print(f"{detected_circles}")

            for index, circle in enumerate(detected_circles[0, :]):
                a, b, r = circle[0], circle[1], circle[2]
                print(f"index: {index}, a: {a}, b: {b}, r: {r}")

                # Draw the circumference of the circle.
                cv2.circle(img, (a, b), r, (0, 255, 0), 2)

                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                cv2.imshow("Detected Circle", img)
                cv2.waitKey(0)
                if index > 3:
                    break
