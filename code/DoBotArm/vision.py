import cv2
import math
from shape import Shape
import time
class Vision():

    def __init__(self, baseWidth):
        #self.image #= cv2.imread('sample.png')#cv2.imread("check.jpg")
        self.colorList = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
        self.mouseActive = False
        self.mousePos = (0,0)
        self.localMousePos = (0,0)
        self.origin = (0,0)
        self.baseWidth = baseWidth
        self.distPixelRatio = 1
        self.base = []
        self.shapePositions = []
        self.setup = False

    def GetMouseState(self):
        return self.mouseActive
    
    def SetMouseState(self, state: bool):
        self.mouseActive = state
    
    def GetMousePos(self):
        return self.localMousePos

    def GetContours(self,image):
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # # Apply Gaussian blur to reduce noise and improve contour detection
        blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 0)
        # Apply Canny edge detection
        t_lower = 100
        t_upper = 200
        aperture_size = 5 # Aperture size 
        L2Gradient = True # Boolean 
        edges = cv2.Canny(blurred_image, t_lower, t_upper, 
                          apertureSize = aperture_size,  
                            L2gradient = L2Gradient)  
        # cv2.imshow("Edges", edges)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def FindCenter(self,contour):

        M = cv2.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            center = (cx, cy)
            return center
        return (-100,- 100)

    def FindBase(self,image,contours):
        height, width, _ = image.shape
        originPoint = (999,999)
        diagLen = 0
        for contour in contours:
            center = self.FindCenter(contour)
            # Approximate the contour to a polygon with fewer vertices
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:
                angleDict = {}
                for point in approx:
                    x, y = point[0]
                    thisPoint = (x,y)
                    h = y - center[1]
                    w = x - center[0]
                    if h == 0: h = 2
                    if w == 0: w = 2
                    angle = math.atan(h/w) / math.pi * 180
                    angle = int(angle)
                     # check quadrant point lies in and correct degrees
                    if (w < 0 and h > 0) or (w < 0 and h < 0): angle += 180
                    if w > 0 and h < 0: angle += 360
                    angleDict[angle] = thisPoint
                    sortedDict = dict(sorted(angleDict.items()))
                points = []
                if len(sortedDict) == 4:
                    for angle in sortedDict:
                        points.append(sortedDict[angle])

                    h = points[0][1] - points[2][1]
                    w = points[0][0] - points[2][0]
                    _diagLen = math.sqrt(w**2 + h**2)
                    if  _diagLen > diagLen:
                        diagLen = _diagLen
                        self.base = points
                        self.origin = points[3]

    def CropFrame(self,image):
        croppedImage = image[self.base[2][1]+5:self.base[0][1]+5, self.base[2][0]-5:self.base[0][0]-5]
        cv2.imshow("Cropped", croppedImage)
        return croppedImage

    def FindShapes(self,image,contours):
        for contour in contours:
            center = self.FindCenter(contour)
            if self.CheckBounds(center,self.base):
                # Approximate the contour to a polygon with fewer vertices
                epsilon = 0.04 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                if len(approx) > 2:
                    cv2.circle(image,center,5,(0,0,255),2)

    def Calibrate(self):
        basePixelWidth = self.base[3][0] - self.base[2][0]
        self.distPixelRatio = self.baseWidth/basePixelWidth

    def ConvertToLocalMil(self, pixel):
        localPixel = (abs(pixel[0] - self.origin[0]), abs(pixel[1] - self.origin[1]))
        xMill = int(self.distPixelRatio * localPixel[0])
        yMill = int(self.distPixelRatio * localPixel[1])
        localMillPos = (xMill, yMill)

        return localMillPos

    def DisplayText(self,image, name, pos):
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        color = (255,255,0)
        cv2.putText(image,"  " + name, pos, font, scale, color)

    def DisplayBase(self, image):
        for i in range(4):
            color = self.colorList[i]
            if i < 3:
                cv2.line(image, self.base[i], self.base[i+1], color, 2)
            else:
                cv2.line(image, self.base[i], self.base[0], color, 2)
        cv2.circle(image,self.origin,5,(255,255,0),2)
        name = "(0,0)"
        self.DisplayText(image, name, self.origin)

    def CheckBounds(self, point, boundary):
        if point[0] > boundary[2][0] and point[0] < boundary[0][0]:
            if point[1] > boundary[2][1] and point[1] < boundary[0][1]:
                return True
        return False

    def MouseClick(self, event, x, y, flags, param): 
        if event == cv2.EVENT_LBUTTONDOWN: 
            if self.CheckBounds((x,y), self.base):
                self.mousePos = (x,y)
                self.localMousePos = self.ConvertToLocalMil(self.mousePos)
                self.mouseActive = True

    def AddShapePos(self, pos):
        self.shapePositions.append(pos)

    def GetShapePositions(self):
        return self.shapePositions
    
    def ClearShapePositions(self):
        self.shapePositions = []

    def DisplayMouseClick(self, image):
        if self.mouseActive:
            cv2.circle(image, self.mousePos, 7, (255,255,0), 2)
            name = str(self.localMousePos)
            self.DisplayText(image,name,self.mousePos)

    def DisplayStartButton(self, image):
        rectPos1 = (self.origin[0] - 50, self.origin[1])
        rectPos2 = (self.origin[0], self.origin[1] + 15)

        cv2.rectangle(image,rectPos1, rectPos2, (255,255,0), 2)

        textPos = (self.origin[0] - 55, self.origin[1] + 12)

        self.DisplayText(image,"START", textPos)

    def DisplayShapePositions(self, image):
        if len(self.shapePositions) < 0:
            for pos in self.shapePositions:
                cv2.circle(image, pos, 7, (255,255,0), 2)

    def Display(self,cap):

        # Read a single frame from the camera
        ret, frame = cap.read()
        # run once
        if not self.setup:
            contours = self.GetContours(frame)
            self.FindBase(frame, contours)
            self.Calibrate()
            self.setup = True

        self.DisplayBase(frame)
        self.DisplayMouseClick(frame)
        self.DisplayStartButton(frame)
        self.DisplayShapePositions(frame)


        cv2.imshow("Main", frame)
        cv2.setMouseCallback('Main', self.MouseClick, param=frame)
        # time.sleep(0.5)

