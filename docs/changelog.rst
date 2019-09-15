.. _changelog:

Change log
----------

Version 1.0.1
^^^^^^^^^^^^^
Released in 14/9/2019

* Minor fixes in examples

Version 1.0.0
^^^^^^^^^^^^^
Released in 13/9/2019.

* Added Tabu Search implementation
* Added Candidate entity to model trajectory solvers
* Added Move entity to model trajectory solvers
* Added neighborhood utilities to decouple solvers
* Solvers now don't need any method overriding thanks to candidates and moves
* Added tests for solvers implemented using TSP example problem
* Moved factory logic to the classes that need it


Version 0.1.0
^^^^^^^^^^^^^
Released in 6/9/2019

* Initial structure for the project.
* Added base solver and multistart approach
* Added GRASP implementation
* Added Simulated Annealing implementation
