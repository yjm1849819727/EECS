import random
import operator
import copy
import lib601.util as util

class DDist:
    """
    Discrete distribution represented as a dictionary.  Can be
    sparse, in the sense that elements that are not explicitly
    contained in the dictionary are assumed to have zero probability.
    """
    def __init__(self, dictionary):
        self.d = dictionary
        """ Dictionary whose keys are elements of the domain and values
        are their probabilities. """

    def dictCopy(self):
        """
        @returns: A copy of the dictionary for this distribution.
        """
        return self.d.copy()

    def prob(self, elt):
        """
        @param elt: an element of the domain of this distribution
        (does not need to be explicitly represented in the dictionary;
        in fact, for any element not in the dictionary, we return
        probability 0 without error.)
        @returns: the probability associated with C{elt}
        """
        if elt in self.d:
            return self.d[elt]
        else:
            return 0

    def support(self):
        """
        @returns: A list (in arbitrary order) of the elements of this
        distribution with non-zero probabability.
        """
        return [k for k in self.d.keys() if self.prob(k) > 0]

    def __repr__(self):
        if len(self.d.items()) == 0:
            return "Empty DDist"
        else:
            dictRepr = reduce(operator.add,
                              [util.prettyString(k)+": "+\
                               util.prettyString(p)+", " \
                               for (k, p) in self.d.items()])
            return "DDist(" + dictRepr[:-2] + ")"
    __str__ = __repr__


def bayesEvidence(PBgA,PA,b):
    PB = totalProbability(PBgA, PA)
    result_dict = {}
    for a in PA.support():
        result_dict[a] = (PBgA(a).prob(b) * PA.prob(a)) / PB.prob(b)
    return DDist(result_dict)

def totalProbability(PBgA,PA):
    result_dict = {}
    all_b = set()
    for a in PA.support():
        all_b.update(PBgA(a).support())
    for b in all_b:
        result_dict[b] = sum(PBgA(a).prob(b) * PA.prob(a) for a in PA.support())
    return DDist(result_dict)

def PTgD(val):
    if val == 'disease':
        return DDist({'posTest':0.9, 'negTest':0.1})
    else:
        return DDist({'posTest':0.5, 'negTest':0.5})
PD = DDist({'disease':0.1, 'noDisease':0.9})

def PRgF(val):
    if val == 'f1':
        return DDist({'r1':0.25, 'r2':0.25, 'r3':0.25, 'r4':0.25})
    else:
        return DDist({'r1':0.1, 'r2':0.1, 'r3':0.1, 'r4':0.7})
PF = DDist({'f1':0.5, 'f2':0.5})

print('-------WK10.1.7  Part1-------')
print(bayesEvidence(PTgD, PD, 'posTest'))
print(bayesEvidence(PTgD, PD, 'negTest'))
print(bayesEvidence(PRgF, PF, 'r3'))
print(bayesEvidence(PRgF, PF, 'r4'))
print('-------WK10.1.7  Part2-------')
print(totalProbability(PTgD, PD))
print(totalProbability(PRgF, PF))