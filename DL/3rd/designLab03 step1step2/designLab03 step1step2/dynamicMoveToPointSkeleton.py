#-*-encoding=utf-8-*-
import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
# import lib601.io as io
# Use this line for testing in soar
from soar.io import io

# class DynamicMoveToPoint(sm.SM):
#     def getNextValues(self, state, inp):
#         goalPoint, sensors = inp

#         #https://ocw.mit.edu/ans7870/6/6.01sc/documentation/util.Point-class.html
#         # https://ocw.mit.edu/ans7870/6/6.01sc/documentation/io.SensorInput-class.html
#         currentPose = sensors.odometry #Instance of util.Pose, representing robot's pose in the global frame if cheat = True and the odometry frame if cheat = False.
#         currentPosition = currentPose.point()
#         currentTheta = currentPose.theta

#         distanceToGoal = currentPosition.distance(goalPoint)
#         angleToGoal = currentPosition.angleTo(goalPoint)
#         angleDifference = util.fixAnglePlusMinusPi(angleToGoal - currentTheta)

#         # 打印调试信息

#         if distanceToGoal < 0.05:
#             print('Reached Goal, Stopping')
#             return state, io.Action(fvel=0.0, rvel=0.0)

#         if abs(angleDifference) > 0.1:
#             rotationSpeed = 0.2 if angleDifference > 0 else -0.2

#             return state, io.Action(fvel=0.0, rvel=rotationSpeed)

#         print('Moving forward with fvel=0.2')
#         return state, io.Action(fvel=0.2, rvel=0.0)

import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
# import lib601.io as io
# Use this line for testing in soar
from soar.io import io

class DynamicMoveToPoint(sm.SM):
    def __init__(self):
        self.startState = None

    def getNextValues(self, state, inp):
        goalPoint, sensors = inp
        print "goalPoint",goalPoint,"sensors",sensors
        currentPose = sensors.odometry  # 当前机器人位姿
        
        currentPoint = currentPose.point()  # 转换为 util.Point
        print "currentPoint",currentPoint

        # 1. 判断是否接近目标点
        if currentPoint.isNear(goalPoint, distEps=0.1):  # 距离阈值为 0.1
            return state, io.Action(fvel=0.0, rvel=0.0)  # 停止

        # 2. 计算前往目标点的角度和距离
        angleToGoal = currentPoint.angleTo(goalPoint)  # 当前点到目标的角度
        distanceToGoal = currentPoint.distance(goalPoint)  # 当前点到目标的距离

        # 3. 计算航向修正（角度差）
        headingError = util.fixAnglePlusMinusPi(angleToGoal - currentPose.theta)  # 修正为 [-π, π] 区间

        # 4. 根据距离和角度误差调整前进和转向速度
        forwardVelocity = 0.2  # 固定前进速度
        if abs(headingError) > 0.1:  # 如果角度误差较大，主要进行旋转调整
            rotationalVelocity = 0.5 if headingError > 0 else -0.5  # 根据误差方向调整角速度
        else:
            rotationalVelocity = 0.0  # 角度较小时，停止转向

        # 5. 返回新的运动指令
        return state, io.Action(fvel=forwardVelocity, rvel=rotationalVelocity)