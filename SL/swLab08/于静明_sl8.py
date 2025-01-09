'''按照题目只写了part3 可在3运行'''
class Component:
    pass

class OpAmp(Component):
    def __init__(self, nPlus, nMinus, nOut, K=10000):
        self.K = K
        self.nPlus = nPlus
        self.nMinus = nMinus
        self.nOut = nOut
        self.current = 'i-' + nOut  

    def getCurrents(self):
        return [[self.current, self, self.nOut, +1]]

    def getEquation(self):
        equations = []
        equations.append((self.nPlus, self.nMinus))  
        equations.append((self.nOut, self.K * (self.nPlus - self.nMinus)))  
        return equations


n1 = 1.0
n2 = 2.0
n3 = 'n3'
op_amp = OpAmp(n1, n2, n3)


equations = op_amp.getEquation()
for equation in equations:
    print(equation[0], '=', equation[1])

currents = op_amp.getCurrents()
for current in currents:
    print(current[0])
