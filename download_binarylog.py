from blueye.sdk import Drone 

myDrone = Drone()
#print(myDrone.logs)

myDrone.logs["BYEDP220037_ee68b38d092149d4_00068"].download()


