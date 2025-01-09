import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

##12.2.1
#part1
#1.number 2.DDist 3.number 4.procedure 5.DDist
#part2
#1.DDist 2.number 3.procedure 4.DDist 5.number 6.error 7.procedure 8.DDist 9.number
#10.m.observationDistribution(s).prob(o) 11.m.transitionDistribution(i)(y).prob(x)
##12.2.2
def bayesEvidence(state,oD,o):
    b={}
    sd=state.dictCopy()
    sk=sd.keys()
    so={}
    sums=0
    for a in sk:
        so[a]=oD(a).prob(o)*sd[a]
    for j in so.keys():
        sums=sums+so[j]
    for k in sk:
        b[k]=so[k]/sums
    bd=dist.DDist(b)
    return bd
def totalProbability(sGo,tD):
    sg=sGo.dictCopy()
    sgk=sg.keys()
    td={}
    for m in sgk:
        for n in sgk:
            dist.incrDictEntry(td,n,tD(m).prob(n)*sg[m])
    return dist.DDist(td)
class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution    
    def getNextValues(self, state, inp):
        (o, i) = inp
        sGo=bayesEvidence(state,self.model.observationDistribution,o)
        dSPrime=totalProbability(sGo,self.model.transitionDistribution(i))
        return (dSPrime,dSPrime)
# Test
transitionTable = \
   {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}),
    'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = \
   {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}),
    'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}
copyMachine = \
 ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}),
                # Input is irrelevant; same dist no matter what
                lambda i: lambda s: transitionTable[s],
                lambda s: observationTable[s])
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]
cmse = StateEstimator(copyMachine)
print cmse.transduce(obs)
##12.2.3
class Preprocessor(sm.SM):
    def getNextValues(self,state,inp):
        

