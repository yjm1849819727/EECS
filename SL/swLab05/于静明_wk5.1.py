"""
Class and some supporting functions for representing and manipulating system functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util


class SystemFunction:
    """
    Represent a system function as a ratio of polynomials in R
    """
    def __init__(self,numeratorPoly, denominatorPoly):
        self.numerator=numeratorPoly
        self.denominator=denominatorPoly

    def poles(self):
        z=self.denominator.coeffs[:]
        z.reverse()
        Poly_new=poly.Polynomial(z)
        return Poly_new.roots()
    
    def poleMagnitudes(self):
        poles = self.poles()
        magnitudes = []
        for pole in poles:
            magnitudes.append(abs(pole))
        return magnitudes

    def dominantPole(self):
        return util.argmax(self.poles(),abs)

    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__


def Cascade(sf1, sf2):
    return SystemFunction(sf1.numerator * sf2.numerator, sf1.denominator * sf2.denominator)

def FeedbackSubtract(sf1, sf2=None):
    numerator=sf1.numerator*sf2.denominator
    denominator=sf1.denominator*sf2.denominator+sf1.numerator*sf2.numerator
    return SystemFunction(numerator,denominator)
    
#check
s1 = SystemFunction(poly.Polynomial([1]),poly.Polynomial([0.63, -1.6, 1]))
print '-------------------s1---------------------'
print 's1:', s1
print 's1.poles():', s1.poles()
print 's1.poleMagnitudes():', s1.poleMagnitudes()
print 's1.dominantPole():', s1.dominantPole()

s2 = SystemFunction(poly.Polynomial([1]),poly.Polynomial([1.1, -1.9, 1]))
print '-------------------s2---------------------'
print 's2:', s2
print 's2.poles():', s2.poles()
print 's2.poleMagnitudes():', s2.poleMagnitudes()
print 's2.dominantPole():', s2.dominantPole()

T = 0.1
k = 2.0
controller = SystemFunction(poly.Polynomial([-k]), poly.Polynomial([1]))
plant = SystemFunction(poly.Polynomial([-T, 0]), poly.Polynomial([-1, 1]))
controllerAndPlant = Cascade(controller, plant)
wire = SystemFunction(poly.Polynomial([1]), poly.Polynomial([1]))
wall = FeedbackSubtract(controllerAndPlant, wire)
print '----------------------------------------'
print 'controller:', controller
print 'plant:', plant
print 'controllerAndPlant:', controllerAndPlant
print 'wall:', wall
print 'wall.poles():', wall.poles()
print '----------------------------------------'

