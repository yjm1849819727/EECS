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
        f = 0.3  # Forward velocity
        r = 0    # Rotational velocity

        # If the front left, middle left, or far left sonar detects an obstacle closer than 0.3 meters
        if inp.sonars[0] < 0.3 or inp.sonars[1] < 0.3 or inp.sonars[2] < 0.3:
            r = -0.3  # Rotate counterclockwise (to move away from the obstacle)
            f = 0.05  # Slow down the forward motion
            print("close")
        # If all three left sonars detect no obstacles within 0.5 meters
        if inp.sonars[0] > 0.5 and inp.sonars[1] > 0.5 and inp.sonars[2] > 0.5:
            r = 0.3  # Rotate clockwise (to adjust towards the boundary)
            f = 0.3  # Move forward at regular speed
            print("far")
        # If the right sonar sensors detect an obstacle too close (less than 0.05 meters)
        if inp.sonars[5] < 0.05 or inp.sonars[6] < 0.05 or inp.sonars[7] < 0.05:
            r = -0.3  # Rotate counterclockwise to avoid the obstacle
            f = -0.1  # Move backward slightly
        # If no obstacle is detected, evaluate the overall situation
        if self.statement == "No obstacle":
            r = 0  # No rotation
            flag = 1  # Flag to check if all sonar readings are clear
            # Loop through all sonar readings to verify no obstacle is within 0.3 meters
            for i in range(0, 8):
                print(inp.sonars[i])  # Print sonar values for debugging
                flag = flag * (inp.sonars[i] > 0.3)
            if flag:  # If all sonar readings indicate no obstacles
                print("no obstacle")
            else:  # If an obstacle is detected, update the state
                self.statement = "Beside obstacle"
                print(self.statement)
        # Print and adjust final velocities
        print(f, r)
        f = f * 1
        r = r * 6  # Amplify rotational velocity
        return (state, io.Action(fvel=f, rvel=r))

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
    # print inp.sonars[0]
    for i in range(8):
        ipt[i]=inp.sonars[i]
    print(ipt)
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
