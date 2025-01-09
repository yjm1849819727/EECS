#python3.6
#pip install nose
#new demo
#scripts:python C:\Users\yjm\Desktop\eecs\wk311111.py
class SM:
    startState = None

    def getNextValues(self, state, inp):
        raise NotImplementedError

    def start(self):
        self.state = self.startState

    def step(self, inp):
        (nextState, output) = self.getNextValues(self.state, inp)
        self.state = nextState
        return output

class Parallel(SM):
    def __init__(self, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = (self.sm1.startState, self.sm2.startState)

    def getNextValues(self, state, inp):
        (s1, s2) = state
        (nextS1, out1) = self.sm1.getNextValues(s1, inp[0])
        (nextS2, out2) = self.sm2.getNextValues(s2, inp[1])
        return ((nextS1, nextS2), (out1, out2))

class Cascade(SM):
    def __init__(self, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = (self.sm1.startState, self.sm2.startState)

    def getNextValues(self, state, inp):
        (s1, s2) = state
        (nextS1, out1) = self.sm1.getNextValues(s1, inp)
        (nextS2, out2) = self.sm2.getNextValues(s2, out1)
        return ((nextS1, nextS2), out2)

class PureFunction(SM):
    def __init__(self, func):
        self.func = func
        self.startState = None

    def getNextValues(self, state, inp):
        output = self.func(inp)
        return (state, output)


def testFunc(x):
    print('-----------i am 3.1.3-------------')
    return x + 1

testSM = PureFunction(testFunc)
print(testSM.getNextValues(None,1))
print('---------------')
class BA1(SM):
    """Fee of $100 on every (non-zero) deposit and withdrawal; 2% interest per time step"""
    startState = 0

    def getNextValues(self, state, inp):
        if inp != 0:
            newState = state * 1.02 + inp - 100
        else:
            newState = state * 1.02
        return (newState, newState)


class BA2(SM):
    """No transaction fee; 1% interest per time step."""
    startState = 0
    def getNextValues(self, state, inp):
        newState = state * 1.01 + inp if inp != 0 else state * 1.01
        return (newState, newState)

# Part 1
def max_balance(balances):
    return max(balances)


accounts = Parallel(BA1(), BA2())
maxAccount = Cascade(accounts, PureFunction(max_balance))


# Part2
def switch_deposit(inp):
    if abs(inp) > 3000:
        return (inp, 0)  # 1
    else:
        return (0, inp)  # 2


def sum_balances(balances):
    return sum(balances)


switch_machine = PureFunction(switch_deposit)
account_balances = Parallel(BA1(), BA2())
switchAccount = Cascade(Cascade(switch_machine, account_balances), PureFunction(sum_balances))

inputs = [5000, -4000, 1000]

switchAccount.start()
for inp in inputs:
    output = switchAccount.step(inp)
    print("Switch Account Output: {}".format(output))

maxAccount.start()
for inp in inputs:
    output = maxAccount.step((inp, inp))
    print("Max Account Output: {}".format(output))

