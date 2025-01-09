import operator
import lib601.util as util

#----------------------------------------------------------------------------- 
class DDist:
    def __init__(self, distribution):
        self.distribution = distribution
        
    def dictCopy(self):
        return self.distribution.copy()
    
    def prob(self, elt):
        if self.distribution.has_key(elt):
            return self.distribution[elt]
        else:
            return 0
    
    def support(self):
        return [key for key in self.distribution if self.prob(key) > 0]
    
    def __repr__(self):
        if not self.distribution:
            return "Empty DDist"
        
        dict_repr = reduce(operator.add, 
                           [util.prettyString(k) + ": " + util.prettyString(p) + ", " 
                            for k, p in self.distribution.items()])
        return "DDist(" + dict_repr[:-2] + ")"
    
    __str__ = __repr__

#----------------------------------------------------------------------------- 
def incrDictEntry(d, key, value):
    """Increments or adds a key-value pair to the dictionary."""
    if d.has_key(key):
        d[key] += value
    else:
        d[key] = value

#----------------------------------------------------------------------------- 
# Square distribution
def squareDist(lo, hi, loLimit=None, hiLimit=None):
    distribution = {}
    probability = 1.0 / len(range(lo, hi))
    
    for i in range(lo, hi):
        clipped_key = util.clip(i, loLimit, hiLimit)
        incrDictEntry(distribution, clipped_key, probability)
        
    return DDist(distribution)

# Test squareDist    
print squareDist(2, 4)
print squareDist(2, 5)
print squareDist(2, 5, 0, 10)
print squareDist(2, 5, 4, 10)
print squareDist(2, 5, 3, 10)
print squareDist(2, 5, 6, 10)

#----------------------------------------------------------------------------- 
# Triangle distribution
def triangleDist(peak, halfWidth, loLimit=None, hiLimit=None):
    distribution = {}
    hw = halfWidth
    
    # Left part of the triangle
    for i in range(peak - hw + 1, peak):
        distribution[i] = 1.0 / (hw ** 2) + (i - peak + hw - 1) / (hw ** 2)
    
    # Peak point
    distribution[peak] = 1.0 / hw
    
    # Right part of the triangle
    for j in range(peak + 1, peak + hw):
        distribution[j] = 1.0 / hw - (j - peak) / (hw ** 2)
    
    # Apply limits
    limited_distribution = {}
    for k in distribution:
        clipped_key = util.clip(k, loLimit, hiLimit)
        incrDictEntry(limited_distribution, clipped_key, distribution[k])
    
    return DDist(limited_distribution)

# Test triangleDist
print triangleDist(5, 1)
print triangleDist(5, 2)
print triangleDist(5, 3)
print triangleDist(5, 3, 0, 10)
print triangleDist(5, 3, 3, 10)
print triangleDist(5, 3, 4, 10)
print triangleDist(5, 3, 5, 10)
print triangleDist(5, 3, 6, 10)

#----------------------------------------------------------------------------- 
# Mixture distribution
class MixtureDist:
    def __init__(self, dist1, dist2, weight):
        self.dist1 = dist1.dictCopy()
        self.dist2 = dist2.dictCopy()
        self.weight = weight
    
    def prob(self, elt):
        prob1 = self.dist1[elt] if self.dist1.has_key(elt) else 0
        prob2 = self.dist2[elt] if self.dist2.has_key(elt) else 0
        return self.weight * prob1 + (1 - self.weight) * prob2
    
    def support(self):
        all_keys = set(self.dist1.keys()) | set(self.dist2.keys())
        return [key for key in all_keys if self.prob(key) > 0]
    
    def __str__(self):
        result = 'MixtureDist({'
        elts = self.support()
        result += ', '.join([str(x) + ' : ' + str(self.prob(x)) for x in elts])
        result += '})'
        return result
    
    __repr__ = __str__

# Test MixtureDist
print MixtureDist(squareDist(2, 4), squareDist(10, 12), 0.5)
print MixtureDist(squareDist(2, 4), squareDist(10, 12), 0.9)
print MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5)

#----------------------------------------------------------------------------- 
# Signal plotting
import lib601.sig as sig

class IntDistSignal(sig.Signal):
    def __init__(self, dist):
        self.dist = dist
    
    def sample(self, n):
        return self.dist.prob(n)

def plotIntDist(dist, n):
    IntDistSignal(dist).plot(end=n, yOrigin=0)

plotIntDist(MixtureDist(squareDist(2, 4), squareDist(10, 12), 0.5), 20)
plotIntDist(MixtureDist(squareDist(2, 4), squareDist(10, 12), 0.9), 20)
plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)
