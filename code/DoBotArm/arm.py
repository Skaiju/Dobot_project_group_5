import DoBotArm as dbt
import time
from serial.tools import list_ports
import threading


class Arm():

    def __init__(self, homeX = 50, homeY = -70, homeZ = 50, port = "COM8"):

        self.arm = dbt.DoBotArm(port, homeX, homeY, homeZ, home= False)
        connected = self.arm.dobotConnect(False)
        return connected


    def MoveLocal(self,pos):
        self.arm.moveArmRelXY(pos[1], pos[0])

    def PickUp(self, objHeight, surfHeight, clearHeight):
        cPos = self.arm.getPosition()
        self.arm.moveArmXYZ(cPos[0], cPos[1], surfHeight + objHeight)
        time.sleep(1.0)
        self.arm.toggleSuction()
        time.sleep(2.0)
        self.arm.moveArmXYZ(0, 0, clearHeight)
        time.sleep(1.0)
    
    def MoveXYZ(self, globalPosX, globalPosY, globalPosZ):
        self.arm.moveArmXYZ(globalPosX, globalPosY, globalPosZ)

    def MoveZ(self, globalPosZ):
        self.arm.moveArmRelZ(globalPosZ)


    def MoveXY(self,globalPosX, globalPosY):
        self.arm.moveArmXY(globalPosX,globalPosY)

    
    def Drop(self,objHeight, surfHeight, clearHeight):   
        cPos = self.arm.getPosition()
        self.arm.moveArmXYZ(cPos[0], cPos[1], surfHeight + objHeight)
        time.sleep(1.0)
        self.arm.toggleSuction()
        self.arm.moveArmXYZ(0, 0, clearHeight)

    def MoveConveyor(self, _time):
        self.arm.SetConveyor(enabled = True, speed = 1500)
        time.sleep(_time)
        self.arm.SetConveyor(enabled = False, speed = 0)


        
    

    

    
