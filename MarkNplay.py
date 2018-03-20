from feature import Feature
import numpy as np
import cv2
from Functions import *

class MarkNplay(Feature):

    QUADRILATERAL_POINTS = 4
    BLACK_THRESHOLD = 100
    WHITE_THRESHOLD = 155
    SCREEN_PATTERN = [1, 0, 1, 0, 1, 0, 1, 0, 1]


    def __init__(self):
        Feature.__init__(self)
        self.background_image = np.array([])
        self.video_capture = cv2.VideoCapture()


    def screen_thread(self, args):
        image = args
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(gray, 100, 200)
        
        _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        for contour in contours:            
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)

            if len(approx) == self.QUADRILATERAL_POINTS:
                topdown_quad = get_topdown_quad(gray, approx.reshape(4, 2))
                if topdown_quad[(topdown_quad.shape[0]//100)*5, (topdown_quad.shape[1]//100)*5] > self.BLACK_THRESHOLD: 
                    continue
                marker_pattern = None
                try:
                    marker_pattern = get_marker_pattern(topdown_quad, self.BLACK_THRESHOLD, self.WHITE_THRESHOLD)
                except:
                    continue
                if not marker_pattern: continue
                if marker_pattern != self.SCREEN_PATTERN: continue
                if self.is_stop: return
                if marker_pattern == self.SCREEN_PATTERN:
                    img = image
                    self.background_image = add_substitute_quad(img, self.get_video_frame(), approx.reshape(4, 2))
                    return

        self.background_image = np.array([])

    def get_video_frame(self):
        success, frame = self.video_capture.read()
        if success: return frame

        if not self.video_capture.isOpened():
            self.video_capture.open('recepie.mp4')
        else:
            self.video_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)

        return self.video_capture.read()[1]


    def stop(self):
        Feature.stop(self)
        self.background_image = np.array([])
        if self.video_capture.isOpened():
            self.video_capture.release()
