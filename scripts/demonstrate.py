#!/usr/bin/env python3
import sys
import os
path = os.popen("rospack find vid_submission").read().split("/")
path.pop()
path.pop()
path = "/".join(path)
path = path + "/devel/lib"
sys.path.append(path)
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

HEAVE_K_P=0.1
HEAVE_K_I=0.1
HEAVE_K_D=0.1
HEAVE_ACCEPTABLE_ERROR=6
bot.setHeavePIDConstants(HEAVE_K_P,HEAVE_K_I,HEAVE_K_D,HEAVE_ACCEPTABLE_ERROR)

def updateDepth(data):
    depth = data.position.z
    bot.updateCurrentHeavePoint(depth)
    bot.updateThrustValues()
    bot.refresh()

def movement():
    bot.setSurgeThrust(0)
    bot.setYawThrust(0)
    bot.setPitchThrust(0)
    bot.setRollThrust(0)
    bot.setSwayThrust(0)
    bot.updateThrustValues()
    bot.refresh()

    sleep(2) # Let bot settle at a depth
    bot.setSurgeThrust(10)
    bot.updateThrustValues()
    bot.refresh()
    sleep(2)
    bot.setSurgeThrust(-10)
    bot.updateThrustValues()
    bot.refresh() 
    sleep(2)
    bot.setSurgeThrust(0)
    bot.setSwayThrust(10)
    bot.updateThrustValues()
    bot.refresh()
    sleep(1)
    bot.setSwayThrust(-10)
    bot.updateThrustValues()
    bot.refresh()
    sleep(1)
    bot.setSwayThrust(0)
    bot.setYawThrust(10)
    bot.updateThrustValues()
    bot.refresh()
    sleep(1)
    bot.setYawThrust(-10)
    bot.updateThrustValues()
    bot.refresh()
    sleep(1)
    bot.setYawThrust(0)
    bot.setPitchThrust(10)
    bot.updateThrustValues()
    bot.refresh()
    sleep(1)
    bot.setPitchThrust(-10)
    bot.updateThrustValues()
    bot.refresh()
    sleep(1)
    bot.setRollThrust(10)
    bot.setPitchThrust(0)
    bot.updateThrustValues()
    bot.refresh()
    sleep(1)
    bot.setRollThrust(-10)
    bot.updateThrustValues()
    bot.refresh()
    sleep(1)
    bot.setRollThrust(0)
    bot.updateThrustValues()
    bot.refresh()


DEPTHTOPIC = "/pose"
MSGTYPE = Pose
rospy.init_node("Bot")
rospy.Subscriber(DEPTHTOPIC,MSGTYPE,callback=updateDepth)
movementThread = threading.Thread(target=movement,daemon=True)
movementThread.start()
rospy.spin()
