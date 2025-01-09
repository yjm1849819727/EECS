import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io


class MySMClass(sm.SM):
    def __init__(self):
        self.statement = "No obstacle"
        print("__init__()")
    def getNextValues(self, state, inp):
        f=0.3
        r=0

        if inp.sonars[0]<0.3 or inp.sonars[1]<0.3 or inp.sonars[2]<0.3 :
            r=-0.3
            f=0.05
            print("close")
        if inp.sonars[0]>0.5 and inp.sonars[1]>0.5 and inp.sonars[2]>0.5 :
            r=0.3
            f=0.3
            print("far")
        if inp.sonars[5]<0.05 or inp.sonars[6]<0.05 or inp.sonars[7]<0.05:
            r=-0.3
            f=-0.1
        if self.statement=="No obstacle":
            r=0
            flag=1
            for i in range(0,8):
                print(inp.sonars[i])
                flag=flag*(inp.sonars[i]>0.3)
            if flag:
                print("no obstacle")
            else:
                self.statement="Beside obstacle"
                print(self.statement)

        print(f,r)
        f=f*1
        r=r*6
        return (state, io.Action(fvel =f, rvel = r))


mySM = MySMClass()
mySM.name = 'brainSM'



'''

        for i in range(0,7):
            if inp.sonars[i]<0.5:
                f=-0.3

'''














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
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    # print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
