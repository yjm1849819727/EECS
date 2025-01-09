#-*-encoding=utf-8-*-
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
verbose = False

# Rotated square points
squarePoints = [util.Point(0.5, 0.5), util.Point(0.0, 1.0),
                util.Point(-0.5, 0.5), util.Point(0.0, 0.0)]

# Step 1: 
# 创建 GoalGenerator：生成一个固定的目标点 (1.0, 0.5)
goalGenerator = sm.Constant(util.Point(1.0, 0.5))
#print("GoalGenerator:", dir(goalGenerator))  # 打印 goalGenerator 的属性


# 使用 sm.Wire 动态传递传感器输入，而不是 sm.Constant
Sensor_Input = sm.Wire()  # sm.Wire 用来传递实时的传感器输入

# 创建 moveToPoint：用于处理目标点和传感器输入的动态移动逻辑
moveToPoint = dynamicMoveToPointSkeleton.DynamicMoveToPoint()

# 并行状态机：将目标生成器和传感器输入并行组合
parallelState = sm.Parallel(goalGenerator, Sensor_Input)

# 串联状态机：将并行输出连接到移动逻辑
mySM = sm.Cascade(parallelState, moveToPoint)
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
