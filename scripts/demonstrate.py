#!/usr/bin/env python3
import sys
sys.path.append('/home/vibhav/localization_ws/devel/lib/')
from time import sleep
import motion_controller as m
import rospy
from std_msgs.msg import String,Float32
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from scipy.spatial.transform import Rotation
import threading


bot = m.ThrusteredVehicleMotionController()
bot.setHeaveControlMode(0) # 0 means closed loop mode
bot.setSurgeControlMode(1) # 0 means closed loop mode
bot.setSwayControlMode(1) # 0 means closed loop mode

bot.setYawControlMode(1) # 0 means closed loop mode
bot.setPitchControlMode(1) # 0 means closed loop mode
bot.setRollControlMode(1) # 0 means closed loop mode

bot.resetAllThrusters()

#TODO
# raise(NotImplementedError("Target Heavepoint not set, PID Values not set "))
bot.setTargetHeavePoint(0)

HEAVE_K_P=0.01
HEAVE_K_I=0.01
HEAVE_K_D=0.01
HEAVE_ACCEPTABLE_ERROR=0.1
bot.setHeavePIDConstants()

def updateDepth(data):
    depth = data.z
    bot.updateCurrentHeavePoint(depth)
    bot.updateThrustValues()
    bot.refresh()

def movement():
    sleep(3) # Let bot settle at a depth
    bot.setSurgeThrust(10)
    bot.updateThrustValues()
    bot.refresh()

DEPTHTOPIC = "/depth"
MSGTYPE = String
rospy.init_node("Bot")
rospy.Subscriber(DEPTHTOPIC,MSGTYPE,callback=updateDepth)
movementThread = threading.Thread(target=movement)
movementThread.start()
rospy.spin()
