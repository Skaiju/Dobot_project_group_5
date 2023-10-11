import cv2
import math

class Vision():

    def __init__(self) -> None:
        self.CaptureImage()
        self.image = cv2.imread('sample.png')#cv2.imread("check.jpg")
        self.colorList = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
        self.FindBase()


    def CaptureImage(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Camera not found.")
        else:
            # Read a single frame from the camera
            ret, frame = cap.read()

            if ret:
                # Save the captured frame as an image file (e.g., 'captured_image.jpg')
                cv2.imwrite('sample.png', frame)

            # Release the VideoCapture object
            cap.release()

        #Close all OpenCV windows
        cv2.destroyAllWindows()

    def GetContours(self):
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # # Apply Gaussian blur to reduce noise and improve contour detection
        blurred_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
        # Apply Canny edge detection
        edges = cv2.Canny(blurred_image, 250, 300)  # You can adjust the threshold values

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

    def FindBase(self):
        contours = self.GetContours()
        height, width, _ = self.image.shape
        originPoint = (999,999)
        diagLen = 0
        base = []
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
                        base = points
        i = 0
        for point in base:
            cv2.circle(self.image, point, 5, self.colorList[i], 2)
            i += 1
                    
        cv2.imshow("awe", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
