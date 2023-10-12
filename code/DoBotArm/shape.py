import numpy as np
import cv2

shapeNames = {
    3:"Triangle", 
    4:"Square", 
    5:"Pentagon" 
}

class Shape():

    def __init__(self, contour, image):

        self.contour = contour  
        self.image = image
        self.center = self.FindCenter()
        self.name = self.FindShapeType()
        self.color = self.get_color_name()

    def FindCenter(self) -> (int,int):

        M = cv2.moments(self.contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            center = (cx, cy)
            return center
        return (-100,- 100)

    def FindShapeType(self) -> str:
       
        # Approximate the shape by a polygon
        epsilon = 0.04 * cv2.arcLength(self.contour, True)
        approx = cv2.approxPolyDP(self.contour, epsilon, True)
        # Calculate the number of vertices of the polygon
        num_vertices = len(approx)
        # Determine the shape based on the number of vertices
        if num_vertices <= 5 and num_vertices >= 3:
            shape = shapeNames[num_vertices]
        elif num_vertices >= 6:
            shape = "Circle"
        else:
            shape = "unknown"
        return shape
    
    def ShowNameText(self, name):
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5
        color = (0,0,0)
        pos = (self.center[0] - (len(self.name) * 4), self.center[1])
        cv2.putText(self.image, name, pos, font, scale, color)
    
    


