import os
labPath = os.getcwd()
from sys import path
if not labPath in path:
    path.append(labPath)
print 'setting labPath to', labPath

import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

# Remember to change the import in dynamicMoveToPointSkeleton in order
# to use it from inside soar
import dynamicMoveToPointSkeleton
reload(dynamicMoveToPointSkeleton)

import ffSkeleton
reload(ffSkeleton)

from secretMessage import secret

# Set to True for verbose output on every step
verbose = True

# Rotated square points
squarePoints = [util.Point(0.5, 0.5), util.Point(0.0, 1.0),
                util.Point(-0.5, 0.5), util.Point(0.0, 0.0)]

# Put your answer to step 1 here
#GOALGENERATOR
# def stateMachine():
#     #return sm.Cascade(ffSkeleton.FollowFigure(squarePoints),dynamicMoveToPointSkeleton.DynamicMoveToPoint())
#     goalGenerator = sm.Constant(util.Point(1.0,0.5))
#     return sm.Cascade(goalGenerator,dynamicMoveToPointSkeleton.DynamicMoveToPoint())
#goalGenerator = sm.Constant(util.Point(1.0,0.5))
#dynamicMoveToPoint = dynamicMoveToPointSkeleton.DynamicMoveToPoint()
#goalAndmove = sm.Cascade(goalGenerator,dynamicMoveToPoint)
#mySM = sm.Parallel(goalGenerator,sm.Cascade(sm.Constant(io.SensorInput),dynamicMoveToPoint))

# goalGenerator = sm.Constant(util.Point(0.5, 0.5))  
# Sensor_Input=sm.Constant(io.SensorInput())
# moveToPoint = dynamicMoveToPointSkeleton.DynamicMoveToPoint()  
# mySM = sm.Parallel(sm.Cascade(goalGenerator,Sensor_Input), moveToPoint)
goalGenerator = sm.Constant(util.Point(1.0,0.5))
Sensor_Input = sm.Wire()
moveToPoint = dynamicMoveToPointSkeleton.DynamicMoveToPoint()
parallelState = sm.Parallel(goalGenerator,Sensor_Input)
mySM = sm.Cascade(parallelState,moveToPoint)
#mySM = None

######################################################################
###
###          Brain methods                                   
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail = True)
    robot.behavior = mySM

def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks(),
                         verbose = verbose)

def step():
    robot.behavior.step(io.SensorInput()).execute()
    io.done(robot.behavior.isDone())

def brainStop():
    pass

def shutdown():
    pass
