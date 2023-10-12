import cv2

import DoBotArm as dbt
import time
from serial.tools import list_ports
from vision import Vision

# create camera object
UI = Vision()

cap = cv2.VideoCapture(0)

while cap.isOpened():

    UI.Display(cap)







    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()  

# image 0ffset
OffsetX, OffsetY = 0, 0

# arm home position
homeX, homeY, homeZ = 170, 0, 0


# Initialize camera settings
# cam.CaptureImage()



# ctrlDobot = dbt.DoBotArm("COM3", homeX, homeY, homeZ, home= False)
# print("starting")
# ctrlDobot.moveArmXYZ(x= 170, y= 50, z= 0)
# ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)


# ctrlDobot.moveArmRelXYZ(0,0,30)
# ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)

# ctrlDobot.toggleSuction()
# time.sleep(10)
# ctrlDobot.toggleSuction()

# # def SetConveyor(self, enabled, speed = 15000):