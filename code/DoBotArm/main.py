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

shapePositions = []


# create vision object
UI = Vision(baseWidth)
# create arm object
arm = dbt.DoBotArm("COM8", homeX, homeY, homeZ, home= False)
arm.moveArmXYZ(x= 150, y= 0, z= 0)
arm.moveArmXYZ(x= 150, y= 100, z= 0)
arm.moveArmXYZ(x= 170, y= 0, z= 0)


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

def AddShapePositions():
    if UI.GetMouseState() == True:
        UI.SetMouseState(False)
        pos = UI.GetMousePos()
        if pos[0] < 50 and pos[1] < 15:
            return True
        else:
            UI.AddShapePos(pos)
            print("added shape pos: ", pos)
    return False

def PickAndPlaceShapes():
    for pos in UI.GetShapePositions():
            pos = UI.GetMousePos()
            arm.moveArmRelXYZ(-pos[1], pos[0],0)
            print("arm moving to ", pos)
            Pickup()
            print("picked up object")
            MoveToBelt()
            print("moving object to belt")
            Drop()
            print("dropped object on conveyor")
            Home()
            print("at home position")
            time.sleep(1.0)

    UI.ClearShapePositions()

cap = cv2.VideoCapture(0)

setup = False
while cap.isOpened():

    UI.Display(cap)

    if AddShapePositions() == True:
        PickAndPlaceShapes()

    if setup == False:
        arm.moveArmXYZ(x= homeX, y= homeY, z= clearHeight)
        setup = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()  