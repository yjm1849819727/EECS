import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    startState='go_straight'
    turnState='turn_right'
    def getNextValues(self, state, inp):
        #blank,cornor(wall corner),near(around wall)
        #go_straight,turn_right,turn_left,corner
        print(state)
        if state == 'go_straight':
            if ((inp.sonars[2]<0.2 and inp.sonars[5]<0.2)or inp.sonars[3]<0.15 or inp.sonars[4]<0.15 or (inp.sonars[3]<0.2 and inp.sonars[4]<0.15)):
                return('corner',io.Action(fvel = -0.3, rvel = 0.4))
            elif ((inp.sonars[])):
                return('go_straight',io.Action(fvel=0.1,rvel=0))
            else:
                return('near',io.Action(fvel=0.08,rvel=0))

         if state =='cornor':
             if ():
                 return('corner',io.Action=-0.3,rvel=0.4)
            elif ():
                return('go_stright',io.Action=0.1,rvel=0)
            else:
                return('near',io.Action=0.08,rvel=0)

            if state =='near':
                
             
        
        
        
        #return (state, io.Action(fvel = -0.05, rvel = 0.05))  #fevel=speed,rvel=omega,positive->negiative clock

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
    ipt = [1,1,1,1,1,1,1,1]
    inp = io.SensorInput()
    for i in range(8):
        ipt[i]=inp.sonars[i]
    print (ipt)
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
