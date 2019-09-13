# -*- coding:utf-8 -*-


"""
    This module implements utilities to deal with neighborhoods in OR-Testbed.

    Usually, in terms of combinatorial optimization, given a solution ``s``, a neighborhood of ``s`` is the set of solutions close to ``s`` (called candidates).
    Two solutions ``s`` an ``s'`` are close if there's a movement that, applied to ``s``, gives ``s'``. The movement itself depends on the problem, but examples are swapping cities
    in TSP, removing or adding items in knapsack, etc.

    When selecting a candidate of a neighborhood, multiple strategies may be used:
        * Random. Just select one random candidate from neighborhood
        * First improving. Iterate through all candidates in neighborhood and select the first candidate that improves the actual solution.
        * Best. Get the best candidate in the neighborhood. Even though this one seems the optimal, it needs to compute the cost of every candidate, which may be a problem in large neighborhoods.
        * Aspiration Plus. Iterate through all candidates, selecting the one that gives the best result but assuring that a minimum of candidates will be examined.

"""

# TODO Implement Aspiration Plus Candidate selection.

import random


# Candidate selection strategies
class CandidateSelection:
    def select(self, candidates, solution, instance):
        pass


class Random(CandidateSelection):
    def select(self, candidates, solution, instance):
        return random.choice(candidates)


class FirstImproving(CandidateSelection):
    def select(self, candidates, solution, instance):
        for candidate in candidates:
            cost = candidate.fitness(solution, instance)
            if cost > 0:
                return cost, candidate

        # If no candidate improves solution, a random one is chosen in order to continue exploring solution space.
        # TODO Maybe we should provide techniques for this
        last_try_candidate = random.choice(candidates)
        return last_try_candidate.fitness(solution, instance), last_try_candidate


class Best(CandidateSelection):
    def select(self, candidates, solution, instance):
        retval = None
        for candidate in candidates:
            cost = candidate.fitness(solution, instance)
            if retval is None or cost > retval[0]:
                retval = (cost, candidate)
        return retval


# Strategies factory
strategies = {'random': Random(), 'first': FirstImproving(), 'best': Best()}


def strategy_factory(ref):
    return strategies[ref]


# Neighborhood utilities
def select_candidate(selection_strategy, candidates, solution, instance):
    return selection_strategy.select(candidates, solution, instance)

