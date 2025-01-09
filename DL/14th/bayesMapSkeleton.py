import lib601.dist as dist
import lib601.util as util
import lib601.colors as colors
import lib601.ssm as ssm
import lib601.seFast as seFast
import lib601.dynamicGridMap as dynamicGridMap


# Define the stochastic state-machine model for a given cell here.

# Observation model:  P(obs | state)
def oGivenS(s):
    if s=='occupy':
        return dist.DDist({'hit':0.8,'free':0.2})
    elif s=='not':
        return dist.DDist({'hit': 0.2, 'free':0.8})
# Transition model: P(newState | s | a)
def uGivenAS(a):
     def trans(prestate):
         if prestate=='occupy':
            return dist.DDist({'occupy':1.0,'not':0.0})
         elif prestate=='not':
            return dist.DDist({'occupy':0.0,'not':1.0})
     return trans

cellSSM = ssm.StochasticSM(dist.DDist({'occupy':0.5,'not':0.5}),uGivenAS,oGivenS)   

class BayesGridMap(dynamicGridMap.DynamicGridMap):

    def squareColor(self, (xIndex, yIndex)):
        p = self.occProb((xIndex, yIndex))
        if self.robotCanOccupy((xIndex,yIndex)):
            return colors.probToMapColor(p, colors.greenHue)
        elif self.occupied((xIndex, yIndex)):
            return 'black'
        else:
            return 'red'
        
    def occProb(self, (xIndex, yIndex)):
        return self.grid[xIndex][yIndex].state.prob('occupy')
    
    def makeStartingGrid(self):
        lst=util.make2DArrayFill(self.xN,self.yN,lambda x,y:seFast.StateEstimator(cellSSM))
        for i in lst:
            for j in i:
                j.start()
        return lst
    
    def setCell(self, (xIndex, yIndex)):
        self.grid[xIndex][yIndex].step(('hit',None))
        self.drawSquare((xIndex, yIndex))
        
    def clearCell(self, (xIndex, yIndex)):
        self.grid[xIndex][yIndex].step(('free',None))
        self.drawSquare((xIndex, yIndex))
        
    def occupied(self, (xIndex, yIndex)):
        return self.occProb((xIndex, yIndex))>0.97


mostlyHits = [('hit', None), ('hit', None), ('hit', None), ('free', None)]
mostlyFree = [('free', None), ('free', None), ('free', None), ('hit', None)]

def testCellDynamics(cellSSM, input):
    se = seFast.StateEstimator(cellSSM) 
    return se.transduce(input)

#print(testCellDynamics(cellSSM,mostlyHits))
#print(testCellDynamics(cellSSM,mostlyFree))



