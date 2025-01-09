import lib601.sig  as sig # Signal
import lib601.ts as ts  # TransducedSignal
import lib601.sm as sm  # SM

######################################################################
##  Make a state machine model using primitives and combinators
######################################################################

def plant(T, initD):
    #机器人运动模型
    return sm.Cascade(sm.R(initD),sm.Gain(T))

def controller(k):
    #控制器模型
    return sm.Gain(k)

def sensor(initD):
    #传感器模型
    return sm.R(initD)

def wallFinderSystem(T, initD, k):
    # 构建整个墙壁寻找系统的状态机
    plant_machine = plant(T, initD)
    controller_machine = controller(k)
    sensor_machine = sensor(initD)
    return sm.FeedbackSubtract(sm.Cascade(controller_machine, plant_machine), sensor_machine)

# Plots the sequence of distances when the robot starts at distance
# initD from the wall, and desires to be at distance 0.7 m.  Time step
# is 0.1 s.  Parameter k is the gain;  end specifies how many steps to
# plot. 

initD = 1.5

def plotD(k, end = 50):
  d = ts.TransducedSignal(sig.ConstantSignal(0.7),
                          wallFinderSystem(0.1, initD, k))
  d.plot(0, end, newWindow = 'Gain '+str(k))

