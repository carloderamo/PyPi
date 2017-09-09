import numpy as np

from mushroom.algorithms.agent import Agent
from mushroom.utils.dataset import max_QA, parse_dataset
from mushroom.utils.replay_memory import Buffer, ReplayMemory


class BatchTD(Agent):
    """
    Implements functions to run batch algorithms.

    """
    def __init__(self, approximator, policy, gamma, **params):
        super(BatchTD, self).__init__(approximator, policy, gamma, **params)

    def __str__(self):
        return self.__name__


class FQI(BatchTD):
    """
    Fitted Q-Iteration algorithm.
    "Tree-Based Batch Mode Reinforcement Learning", Ernst D. et.al.. 2005.

    """
    def __init__(self, approximator, policy, gamma, **params):
        self.__name__ = 'FQI'

        super(FQI, self).__init__(approximator, policy, gamma, **params)

    def fit(self, dataset, n_iterations):
        """
        Fit loop.

        Args:
            dataset (list): the dataset;
            n_iterations (int): number of FQI iterations.

        """
        target = None
        for i in xrange(n_iterations):
            target = self._partial_fit(dataset, target,
                                       **self.params['fit_params'])

    def _partial_fit(self, x, y, **fit_params):
        """
        Single fit iteration.

        Args:
            x (list): a two elements list with states and actions;
            y (np.array): targets;
            **fit_params (dict): other parameters to fit the model.

        """
        state, action, reward, next_states, absorbing, last = parse_dataset(x)
        if y is None:
            y = reward
        else:
            maxq, _ = max_QA(next_states, absorbing, self.approximator)
            y = reward + self._gamma * maxq

        sa = [state, action]
        self.approximator.fit(sa, y, **fit_params)

        return y


class DoubleFQI(FQI):
    """
    Double Fitted Q-Iteration algorithm.
    "Estimating the Maximum Expected Value in Continuous Reinforcement Learning
    Problems". D'Eramo C. et. al.. 2017.

    """
    def __init__(self, approximator, policy, gamma, **params):
        self.__name__ = 'DoubleFQI'

        super(DoubleFQI, self).__init__(approximator, policy, gamma, **params)

    def _partial_fit(self, x, y, **fit_params):
        pass


class WeightedFQI(FQI):
    """
    Weighted Fitted Q-Iteration algorithm.
    "Estimating the Maximum Expected Value in Continuous Reinforcement Learning
    Problems". D'Eramo C. et. al.. 2017.

    """
    def __init__(self, approximator, policy, gamma, **params):
        self.__name__ = 'WeightedFQI'

        super(WeightedFQI, self).__init__(approximator, policy, gamma, **params)

    def _partial_fit(self, x, y, **fit_params):
        pass
