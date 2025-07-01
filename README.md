    
# SAT - Project

In this project, I want to grapple with the satisfiability problem (SAT).

## Phase 1

**Basic foundation**

- Have proper internal encodings of SAT-instances
  - Bit-Matrix (binary np-array)
  - Clauses as sets of integers 
- Parse & write instances to files (in different formats)
  - DIMACS CNF
  - Bit-Matrix
- Visualize CNFs
  - Bit-Matrix (per literal or variable)
  - Clause-Shared-Variables-Graph
  - Clause-Literal-Graph
  - Variable-Interaction-Graph
- Extract the "kernel" of a SAT-instance (of course in poly-time)
  - Each variable x occurs at least once as x and -x (= no pure literals)
  - No unit clauses
  - No tautological clauses (x, -x)
  - No duplicate clauses
  - No superset clauses
  - Biathlet fulfilled
  - LLL fulfilled
  - Keine 2-Eige-Zwillinge
  - Exactly 1 strongly connected component in the variable interaction graph
  - Tovey's criterium satisfied
  - Not a 2-SAT instance
  - Not a Horn-Instance or Renamable-Horn instance
  - TODO: Blocked clause elimination? (see https://users.aalto.fi/%7Etjunttil/2020-DP-AUT/notes-sat/preprocessing.html)

## Phase 2

**Understand and implement SAT-solvers**

- Implement known base algorithms for SAT in Python

> It is not the aim to get into the realm of competitive SAT-solving (thus python suffices).
> 
> The focus is more on the didactic aspect. It's about understanding the different base approaches and have a working implementation.
> 
> Of course, there are two many to cover them all, I decided just for a selection.

### Implemented SAT-solvers

- Brute Force (see [here](sat/solve/brute_force.py))
- 2 SAT (see [here](sat/solve/two_sat.py))

#### DPLL-artig

- DPLL base algorithm ([recursive](sat/solve/dpll/dpll_recursive.py) and [iterative](sat/solve/dpll/dpll.py))
  - each using different [heuristics](sat/solve/dpll/heuristics.py)
- DPLL with conflict driven clause learning (see [here](sat/solve/dpll/dpll_cdcl.py))
  using different [heuristics](sat/solve/dpll/heuristics.py)
- Monien-Speckenmeyer (see [here](sat/solve/dpll/monien_speckenmeyer.py))
- Paturi-Pudlak-Zane (see [here](sat/solve/dpll/paturi_pudlak_zane.py))

#### Local search based

- Two-sided deterministic local search (see [here](sat/solve/local_search/two_sided_deterministic_local_search.py))
- Random local search (see [here](sat/solve/local_search/random_local_search.py))
- Dantsin local search (see [here](sat/solve/local_search/dantsin_local_search.py))
- Schöning's Algorithm (see [here](sat/solve/local_search/schoening.py))
- GSAT ([base version](sat/solve/local_search/greedy_sat.py) and [with walk](sat/solve/local_search/greedy_sat_with_walk.py))
- WSAT (see [here](sat/solve/local_search/walk_sat.py))


# Phase 3

TODO.

Ideas:

- Write a little docu / wiki about the algorithms / ideas 
- create animation of the order the assignments get checked in different approaches
- Get some sample SAT instances from online benchmarks
- Run those algorithms against sample instances and measure their performance (not really important, since not optimized anyway)
- Get a feeling for what instance sizes are possible to deal with nowadays
- Get to know the State-Of-The-Art SAT solvers, and on what base approaches they are building upon
  z.b. https://github.com/jaras209/SAT_solver/blob/master/cdcl.py, "2-watched literals" (irgendne art index)

# Phase 4

**Try to do some research on my own** 

- Generate "core" SAT-instances (satisfiable & not satisfiable, minimally unsatisfiable)
  - Maybe also specific types of SAT-instances such as (Renamable-)Horn, 3SAT, etc.
- Is it possible to find characteristics of (un)satisfiable instances (of course poly-computable)?
  - Given minimally unsatisfiable instances, check if there are shared (maybe just in a subset) characteristics to find
    - Maybe some attribute A, s.t. : instance has A => instance is unsatisfiable
    - Or attribute B, s.t. : instance has B => instance is satisfiable
- Given a core instance, what do I know about it?
  - By combining all induced attributes of the instance
  - Is it possible to use it for a SAT-solver?

## Literature

- Das Erfüllbarkeitsproblem SAT (Schöning, [siehe hier](https://www.google.de/books/edition/Das_Erf%C3%BCllbarkeitsproblem_SAT/55HzCQAAQBAJ?hl=de&gbpv=0))
- Handbook of Satisfiability (Biere et al.)
- TAOCP, 4B (Knuth)

## Random more ideas

- Implement a SAT-solver in a basic language (Assembler, or even TM) (maybe there is something to learn from that?)

## Helpful links

https://pysathq.github.io/
https://cse442-17f.github.io/Conflict-Driven-Clause-Learning/
https://users.aalto.fi/%7Etjunttil/2020-DP-AUT/notes-sat/cdcl.html
