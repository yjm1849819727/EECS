import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):

    # def getNextValues(self, state, inp):
    #     if inp.sonars[4]<=0.3 or inp.sonars[5]<=0.3 or inp.sonars[6]<=0.3 or inp.sonars[7]<=0.3:
    #         return (state, io.Action(fvel = 0, rvel = 0.5))
    #     elif  inp.sonars[5]<=0.5 or inp.sonars[6]<=0.5 or inp.sonars[7]<=0.5:
    #         return (state, io.Action(fvel = 0.3, rvel = 0))
    #     elif inp.sonars[0]<=0.5 or inp.sonars[1]<=0.5 or inp.sonars[2]<=0.5 or inp.sonars[3]<=0.5:
    #         return (state, io.Action(fvel = 0, rvel = 0.5))
    #     else:
    #         return (state, io.Action(fvel = 0, rvel = -0.5))

    # def getNextValues(self, state, inp):
    #     if  inp.sonars[3]<=0.45 or inp.sonars[4]<=0.45 :
    #         return (state, io.Action(fvel = -0.07, rvel = 0))
    #     elif  inp.sonars[3]<=0.55 or inp.sonars[4]<=0.55 :
    #         return (state, io.Action(fvel = 0, rvel = 0))
    #     else:
    #         return (state, io.Action(fvel = 0.07, rvel = 0))
    def getNextValues(self, state, inp):
        return (state, io.Action(fvel = 0, rvel = 0))
mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=True) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
