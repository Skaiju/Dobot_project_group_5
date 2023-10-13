import cv2
from serial.tools import list_ports
from vision import Vision
from arm import Arm
import DoBotArm as dbt
import time

clearHeight = 40
shapeHeight = -35
conveyorHeight = -10
baseHeight = -50

originX = 195
originY = 70

conveyorX = 5
conveyorY = 130

baseWidth = 120
homeX, homeY, homeZ = 195,70, -50

# create vision object
UI = Vision(baseWidth)
# create arm object
arm = dbt.DoBotArm("COM8", homeX, homeY, homeZ, home= False)
arm.moveArmXYZ(x= 150, y= 0, z= 0)
# arm.moveArmXYZ(x= 150, y= 100, z= 0)
# arm.moveArmXYZ(x= 170, y= 0, z= 0)

def Pickup():
    cPos = arm.getPosition()
    arm.moveArmXYZ(cPos[0],cPos[1], shapeHeight)
    arm.toggleSuction()
    time.sleep(0.5)
    cPos = arm.getPosition()
    arm.moveArmXYZ(cPos[0],cPos[1],clearHeight)

def Home():
    arm.moveArmXYZ(x= homeX, y= homeY, z= clearHeight)


def Drop():
    cPos = arm.getPosition()
    arm.moveArmXYZ(cPos[0],cPos[1], conveyorHeight + 40)
    arm.toggleSuction()
    arm.SetConveyor(enabled= True,speed = 1500)
    time.sleep(2)
    arm.SetConveyor(enabled= False,speed = 0)



def MoveToBelt():
    arm.moveArmXYZ(conveyorX,conveyorY,clearHeight)

cap = cv2.VideoCapture(1)

setup = False
while cap.isOpened():

    

    UI.Display(cap)


    if UI.GetMouseState() == True:
        pos = UI.GetMousePos()
        arm.moveArmRelXYZ(-pos[1], pos[0],0)
        print("arm moving to ", pos)
        Pickup()
        MoveToBelt()
        Drop()
        Home()


        UI.SetMouseState(False)

    if setup == False:
        arm.moveArmXYZ(x= homeX, y= homeY, z= clearHeight)
        setup = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()  