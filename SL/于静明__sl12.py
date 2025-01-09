import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution

    def getNextValues(self, state, inp):
        (observation, input_signal) = inp
        posterior_given_observation = self.__bayesEvidence(state, self.model.observationDistribution, observation)
        next_state_distribution = self.__totalProbability(posterior_given_observation, self.model.transitionDistribution(input_signal))
        return (next_state_distribution, next_state_distribution)

    def __bayesEvidence(self, prior_state_distribution, observation_distribution, observation):
        posterior_distribution = {}
        prior_dict = prior_state_distribution.dictCopy()
        states = prior_dict.keys()
        likelihood_given_state = {}
        total_likelihood = 0

        for state in states:
            likelihood_given_state[state] = observation_distribution(state).prob(observation) * prior_dict[state]

        for state in likelihood_given_state.keys():
            total_likelihood += likelihood_given_state[state]

        for state in states:
            posterior_distribution[state] = likelihood_given_state[state] / total_likelihood

        return dist.DDist(posterior_distribution)

    def __totalProbability(self, posterior_given_observation, transition_distribution):
        prior_dict = posterior_given_observation.dictCopy()
        states = prior_dict.keys()
        next_state_distribution = {}

        for current_state in states:
            for next_state in states:
                dist.incrDictEntry(next_state_distribution, next_state, 
                                   transition_distribution(current_state).prob(next_state) * prior_dict[current_state])

        return dist.DDist(next_state_distribution)

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
print(cmse.transduce(obs))
