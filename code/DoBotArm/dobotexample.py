import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
homeX, homeY, homeZ = 170, 0, 0
ctrlDobot = dbt.DoBotArm("COM8", homeX, homeY, homeZ, home= False)
print("starting")
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)
ctrlDobot.moveArmXYZ(x= 150, y= 0, z= 0)
ctrlDobot.moveArmXYZ(x= 150, y= 100, z= 0)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)

# ctrlDobot.moveArmRelXYZ(0,50,0)

# print(ctrlDobot.getPosition())

# ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)

# ctrlDobot.toggleSuction()
# time.sleep(10)
# ctrlDobot.toggleSuction()

# def SetConveyor(self, enabled, speed = 15000):


