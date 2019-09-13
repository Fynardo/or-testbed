# OR-Testbed

OR-testbed is a framework designed to solve combinatorial optimization problems through the use and modeling of 
[metaheuristics](https://en.wikipedia.org/wiki/Metaheuristic). Since metaheuristics are based on certain basic assumptions,
 they can be adapted for a multitude of different problems.

The contribution of OR-Testbed is to provide the implementation of the basic structure of metaheuristics. 
In this way, the problems to be solved (and therefore the related structures needed) only need to be modeled once. 
Then, once each of the functions and parameters of the metaheuristics to be used have been adapted, the problem
 can be solved with all of them from a centralized point. 

In summary, the objective of the framework is to implement the most relevant metaheuristics in the state of the art, 
as well as the techniques commonly used in literature to improve them. This lets developers and researchers to have a 
centralized repository of implemented metaheuristics, techniques and potential execution service for all of their problems. 

At this moment, the list of implemented metaheuristics is:

* GRASP
* Simulated Annealing
* Tabu Search


To see the development plans at a glance, all relevant information can be found in the [roadmap](ROADMAP.md).


## Installing

Since OR-Testbed is coded in pure Python no requirements are needed, just execute:

`pip install or-testbed`

## Examples and usage

There is no oneliner example, but there is a tutorial in the docs section. Also, check the available [examples](examples/) 
where some problems and algorithms are implemented and the usual workflow is showed. 

## Contributing

All contributions will be greatly appreciated. The main alternatives are to report or correct bugs, 
suggest changes or functionalities, open issues and, of course, implement new metaheuristics.

### Testing

Run the unit test collection with:

`pytest`


### Building docs

First, build the docs using Sphinx:

```
cd docs
make html
```

Then open build/html/index.html in your browser to view the docs.

Read more about [Sphinx](https://www.sphinx-doc.org/en/master/).

### Other resources
Since using OR-Testbed requires both coding and optimization related knowledge, this section will be more focused
on the latter:

* [Metaheuristic. *Wikipedia Introduction*](https://en.wikipedia.org/wiki/Metaheuristic)
* [Survey on metaheuristics #1. *Boussaid et al (2013)*](https://www.sciencedirect.com/science/article/pii/S0020025513001588)
* [Survey on metaheuristics #2. *Bianchi et al (2008)*](https://link.springer.com/article/10.1007/s11047-008-9098-4)
* [GRASP. *Resende (1995)*](https://www.researchgate.net/publication/225237245_Greedy_Randomized_Adaptive_Search_Procedures)
* [Simulated Annealing. *Kirkpatrick et al (1983)*](https://science.sciencemag.org/content/220/4598/671)
* [Tabu Search. *Glover (2003)*](https://www.sciencedirect.com/science/article/pii/0305054886900481)
* [Ant Colony Optimization (ACO) survey. *Mohan (2001)*](https://www.sciencedirect.com/science/article/pii/S0957417411013996)
