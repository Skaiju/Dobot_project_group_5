import cv2
from serial.tools import list_ports
from vision import Vision
from arm import Arm
clearHeight = 100
shapeHeight = 20
conveyorHeight = 50
originX = -70
originY = 50
baseWidth = 150
homeX, homeY, homeZ = originX, originY, clearHeight

# create camera object
UI = Vision(baseWidth)
# arm = Arm(homeX, homeY, homeZ, "COM3")
cap = cv2.VideoCapture(0)

while cap.isOpened():

    UI.Display(cap)

    if UI.GetMouseState() == True:
        print("arm moving to ", UI.GetMousePos())
        UI.SetMouseState(False)






    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()  