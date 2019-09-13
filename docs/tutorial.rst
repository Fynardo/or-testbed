.. _tutorial:

========
Tutorial
========

This section acts as a tutorial and it will present some insights about how to use an adapt OR-Testbed to solve our problems.


Traveling Salesman Problem (TSP)
--------------------------------

Introduction
^^^^^^^^^^^^

TSP is one of the best known combinatorial optimization problems, so it will serve perfectly to explain how to use OR-Testbed.
To summarize, our salesman must visit a certain number of cities, he wants to minimize the cost associated with his whole trip and, of course, he only
wants to visit each city once. So this gives us a graph where each node represents a city and an edge between cities represents the distance
between them. We want to give our salesman a sequence of cities he must visit that finishes in the starting city and minimizes the distance he must travel.

Check some resources if you are unfamiliar with TSP:

* `Wikipedia`_

.. _Wikipedia: https://en.wikipedia.org/wiki/Travelling_salesman_problem

* `xkcd`_

.. _xkcd: https://www.explainxkcd.com/wiki/index.php/399:_Travelling_Salesman_Problem

* `google OR-Tools`_

.. _google OR-Tools: https://developers.google.com/optimization/routing/tsp

* `TSPLIB`_

.. _TSPLIB: http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsplib.html


We can start modeling TSP in OR-Testbed and solving it the best we can. All the code in this example is avaiable on
`Github <http://github.com/Fynardo/OR-Testbed/tree/master/examples/tsp>`_.

Problem Definition
^^^^^^^^^^^^^^^^^^


In OR-Testbed, three things are needed to solve a problem:

1. An **Instance**. Instance objects store input data and some logic, for example is their responsibility to know how to check the feasibility
of a solution and calculating its objective. In TSP, instances will have information about cities and distances.

2. A **Solution**. Solution objects store the obtained solution for some problem, its internal structure depends on the problem itself,
but all solutions in OR-Testbed share share a value called **objective**, that represents the quality of the solution. In TSP this objective
is the cost of the calculated trip.

3. A **Solver**. The solver is the one that does the work, this is, the algorithm itself. Each solver implements one metaheuristic or a variation of
a metaheuristic. In TSP, we will need to implement some methods related to the solvers in order to adapt their logic to TSP.


Defining an instance
^^^^^^^^^^^^^^^^^^^^

All instance objects extend from an abstract class defined in OR-Testbed called, as you may imagine, Instance. This class provides some
methods for general functionality, like data setters and getters and a basic JSON loader. Check :ref:`instance <entities_instance>` docs for more information.

Lets check the code, first we must import abstract instance class like in the solution case.

.. code-block:: python

    import or_testbed.entities.instance as base_instance

Now, we are going to define the data related to our problem. Instance objects need two pieces of information: the **name** of the instance and the **data** related to it. The name is used to refer to some
concrete data, for example, in TSPLIB all instances have a name (*a280*, *brazil58*, *ch130*, etc) and that represents the number of cities and other information.

On the other hand we have instance data, this is the information about the cities, their distances, etc.
Lets code a small TSP example with 5 cities (named from 'A' to 'E'):

.. code-block:: python

    instance_name = 'tsp_example'
    cities = {'A': {'B': 3, 'C': 5, 'D': 6, 'E': 2}, 'B': {'A': 3, 'C': 25, 'D': 10, 'E': 5}, 'C': {'A': 5, 'B': 25, 'D': 3, 'E': 4}, 'D': {'A': 6, 'B': 10, 'C': 3, 'E': 1}, 'E': {'A': 2, 'B': 5, 'C': 4, 'D': 1}}

As you can see, cities information are codified with a adjacency list using a python dict, this may not be an optimal approximation but its fine for an example. Now we can instantiate our TSPInstance class as follows:

.. code-block:: python

    class TSPInstance(base_instance.Instance):
        def __init__(self, name, data=None):
            super().__init__(name, data)

Since we are not overriding any logic, we just extend base instance class. In this example we could use the base class directly but chances are that
we usually need to adapt something (like the data loader).


Defining a solution
^^^^^^^^^^^^^^^^^^^

As with the instance object, the solution object also extends some abstract class called Solution. This class initializes the objective value to 0
by default, so it assumes that the cost function can be represented with a numeric value. Of course it provides the common getter and setter methods to interact
with the objective.

We have to implement two methods: ``is_feasible`` and ``calculate_objective``. The first one is responsible of checking whether a solution is feasible or not,
based on concrete problem requirements. In TSP, we just need to assure that all cities are visited once. The second one calculates the objective,
i.e., the cost of the trip. In TSP this cost is basically the sum of distances between cities, but could be as complex as needed.

Also, it provides a basic ``compare_to`` method, that compares two solutions based on their objectives.
Check :ref:`solution <entities_solution>` docs for more information.

So, in order to make our solution for TSP, we must extend this class. We can import the solution abstract class in the usual way, for example:

.. code-block::python

    import or_testbed.entities.solution as base_solution

Now, for TSP we want two things: a starting city and the sequence of cities that our salesman is going to visit. The following code does just that.

.. code-block:: python

    class TSPSolution(base_solution.Solution):
        def __init__(self, initial_city):
            super().__init__()
            self.initial_city = initial_city
            self.cities = [initial_city]

        def is_feasible(self, in_instance):
            return set(self.cities) == set(in_instance.data.keys())

        def calculate_objective(self, in_instance):
            return sum([in_instance.data[a][b] for a,b in zip(self.cities, self.cities[-1:] + self.cities[:-1])])

Inside the ``__init__`` function we initialize the solution (the sequence of cities to visit) with the starting city. Note that since there is no need
to update the objective right now.

Then we override methods ``is_feasible`` and ``calculate_objective``, not that they both have access to concrete instance information.
First, to check the feasibility we just want to check if all cities ( ``in_instance.data.keys()`` ) are present in the solution ( ``self.cities`` ).
Second, for the objective we want to sum all distances between the sequence of cities (and between last city and the starting one). That's a pretty
hard to read oneliner, but what it just sums distances between the cities present in the solution object.

These two methods are going to be called by the solvers when needed, we just need to give them an implementation.


Solving an instance
^^^^^^^^^^^^^^^^^^^

The last step is to get a solver working and create a trip for our salesman. In this tutorial we are going to use :ref:`GRASP <grasp_solver>` to generate
a solution. There is more solvers implemented in the examples folder in Github repository.

`GRASP <https://en.wikipedia.org/wiki/Greedy_randomized_adaptive_search_procedure>`_ is a very simple, yet very powerful, optimization algorithm.
To construct a solution, what it does is basically 4 steps:

1. Defines candidates to add to the solution. In TSP, these candidates are cities to visit.
2. Applies a greedy function to each candidate to calculate the incurring cost of adding that candidate to the solution. In TSP, this may be the distance between last city and the remaining not visited ones.
3. Ranks candidates according to this cost. In TSP, closer cities will rank better than farther ones.
4. Filters candidates depending on their costs, depending on alpha parameter, this creates the Restricted Candidates List (RCL). In TSP, this may mean that some far cities will not be taken into account.
5. Adds one random candidate to the solution. In TSP, one of the closest solutions will be added as next city to visit.

The power of GRASP comes when some randomness is applied in step 4, this lets the algorithm to explore new solution space, therefore, achieving better solutions.

OR-Testbed implements the core of GRASP, and manages randomness with the parameter **alpha** (a float value between 0 and 1). In step 3, when ranking candidates we can take into account only a subset
of al possible candidates, this is what alpha does with the following equation:

.. code-block:: none

    c_min <= c(e) <= c_min + alpha*(c_max - c_min)

Where **c(e)** is the cost of candidate **e** (based on the greedy function), **c_min** and **c_max** are the minimum and maximum costs of the remaining candidates, respectively.

What this means is that when alpha is 0 only candidates with minimum cost are taken into account (pure greedy approach). On the other hand, when
alpha is 1 all candidates are taken into account (pure randomness approach). What alpha does is to set the confidence we have in our greedy function.

Anyhow, to solve our TSP problem we must implement some other logic. GRASP workflow (as lots of other metaheuristics) is about selecting candidates and making small changes
to solutions in the best trajectory as possible. In OR-Testbed we implement this logic within two entities: candidates and movements.

Lets start with movements. As stated earlier, multiple metaheuristics work by exploring neighborhoods and trying to find paths that eventually may guide them to good solutions.
This neighborhoods are defined by the moves. For example, in GRASP our only move is to add cities to the sequence until all cities are covered.
The neighborhood (the set of candidates to take into account) related to that move are the cities left to be added to the sequence.

Lets see an example, this could be the GRASP move and candidate definition for TSP:

.. code-block:: python

    class TSPGraspCandidate(base_candidate.Candidate):
        def __init__(self, city):
            self.city = city

        def fitness(self, solution, instance):
            last_visited = solution.cities[-1]
            return instance.data[last_visited][self.city]

    class TSPGraspMove(base_move.Move):
        @staticmethod
        def make_neighborhood(solution, instance):
            return [TSPGraspCandidate(city=c) for c in instance.data[solution.cities[-1]].keys() if c not in solution.cities]

        @staticmethod
        def apply(in_candidate, in_solution):
            in_solution.cities.append(in_candidate.city)
            return in_solution


Candidates store internal structure and the fitness function, which is the cost of adding the candidate city as the next step on our sequence.
On the other hand, neighborhoods are just a candidates list, in this case, made by the cities not added yet to the solution.
To apply this move, we just append the candidate to the solution.

Executing our solver
^^^^^^^^^^^^^^^^^^^^

All the needed components are implemented now, that means that there's only one more step, executing it all.

.. code-block:: python

    import or_testbed.solvers.grasp as base_grasp

    if __name__ == '__main__':
        # Instantiate instance
        my_tsp = TSPInstance(instance_name, cities)
        # Create factory from solution
        tsp_solution_factory = TSPSolution.factory(initial_city='A')
        # Instantiate GRASP solver (with parameter alpha = 0.0, greedy approach) passing our move.
        tsp_solver = base_grasp.GraspConstruct(tsp, alpha=0.0, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove)
        # Run the solver
        feasible, solution = tsp_solver.solve()
        # Retrieve the cities sequence and the objective value (the cost of the trip)
        print('Salesman will visit: {}'.format(solution.cities))
        print('Total cost: {}'.format(solution.get_objective()))


Basically we instantiate the instance, the solution, the solver and then we call ``solve`` method, that triggers the solver and returns
the solution found. In fact, a tuple is returned, first element (``feasible``) is a boolean that tells if the solution found is feasible or not,
second element is the solution itself.
Note that the solution is not instantiated directly, what we do is to create a factory around it, but its the same syntax.
What this means is that solvers usually need to be able to create new solutions, so we want to give them a way to do so, thats what
``factory`` class method does.

Once executed we will get a solution for our problem, an easily improvable one to be fair.

Improving our solution
^^^^^^^^^^^^^^^^^^^^^^

In our previous example, we solved the problem with alpha being 0.0, this means that there is no randomness, so the greedy function will rule it all.
We could set another value to alpha (like 0.3) so the solver would be able to explore more solutions. That's a fine approximation, but with
randomness involved we usually want to try and stabilize our solutions. This is where **multistart** techniques come in, this lets us run
our solvers a number of times and get the best result.

Lets see how we do it with OR-Testbed:

.. code-block:: python

    import or_testbed.solvers.grasp as base_grasp

    if __name__ == '__main__':
        # Instantiate instance
        my_tsp = TSPInstance(instance_name, cities)
        # Make a solution factory as before
        tsp_solution_factory = TSPSolution.factory(initial_city='A')
        # Since we want to execute multiple GRASP instances, we also make a factory from it
        tsp_grasp_factory = base_grasp.GraspConstruct.factory(instance=tsp, alpha=0.3, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove)
        # Instantiate our multistart version of GRASP with 25 iterations
        tsp_multistart = base_grasp.MultiStartGraspConstruct(iters=25, inner_grasp_factory=tsp_grasp_factory)
        # Run the solver
        feasible, ms_solution = tsp_multistart.solve()
        # Retrieve the cities sequence and the objective value (the cost of the trip) of the best solution found
        print('Salesman will visit: {}'.format(ms_solution.cities))
        print('Total cost: {}'.format(ms_solution.get_objective()))

Running a multistart solver is almost the same as running the proper solver, the main difference is that now, for the *inner solver* (GRASP)
we don't want an instance, we need a factory, because the multistart solver is going to instantiate it many times. The good thing is that
our solution now is better (the optimal one in fact).

Note that we don't need to implement anything within ``MultiStartGraspConstruct``, since it's a direct extension from the base multistart solver.

The bad thing is that the console is full of information that we may not want to see right now, that's because the logger is set to print everything by default.

Logging
^^^^^^^

Every solver logs the steps it takes, printing in to the standard output (console) by default. That's fine, but we may don't want all of the information.
OR-Testbed includes a logging utility that lets the developer show or hide information (or send it to a log file).

For example, in our multistart GRASP example, we may want to only see the output of the multistart solver, not the inner one.
We can set that with:

.. code-block:: python

    tsp_grasp_factory = base_grasp.GraspConstruct.factory(instance=tsp, alpha=0.3, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove, debug=False)

That's the same line from the example but with the parameter **debug** set to ``False``, that prevents any output to be printed.
Note that we can set debug parameter to ``True`` or ``False`` to any solver.

Of course we may not want to see the output but to store it to check later, we can do that setting the ``log_file`` parameter, for example:

.. code-block:: python

    tsp_grasp_factory = base_grasp.GraspConstruct.factory(instance=tsp, alpha=0.3, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove, debug=False, log_file='log.txt')

That will not print the output but store it to a text file called *log.txt*.


What's Next
^^^^^^^^^^^

There is some more examples on how to use OR-Testbed showing another problems and solvers available at
`examples <http://github.com/Fynardo/OR-Testbed/tree/master/examples>`_
folder on Github repo.