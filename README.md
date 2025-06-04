    
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
- Extract the "core" of a SAT-instance (of course in poly-time)
  - Each variable x occurs at least once as x and -x
  - No unit clauses
  - No trivial clauses (x, -x)
  - No double clauses
  - No superset clauses
  - Biathlet fulfilled
  - LLL fulfilled
  - Keine 2-Eige-Zwillinge
  - Exactly 1 strongly connected component in the variable interaction graph
  - Tovey's criterium satisfied
  - Not a 2-SAT instance
  - Not a Horn-Instance or Renamable-Horn instance
- Detect & solve polynomially solvable SAT-instances (as e.g. horn-clauses), (of course in poly-time)

## Phase 2

**Understand and implement SAT-solvers**

- Implement known base algorithms for SAT in Python

> It is not the aim to get into the realm of competitive SAT-solving (thus python suffices).
> 
> The focus is more on the didactic aspect. It's about understanding the different base approaches and have a working implementation.

- Get some sample SAT instances from online benchmarks
- Run those algorithms against sample instances and measure their performance (not really important, since not optimized anyway)
- Write a little docu / wiki about the algorithms / ideas
- Get a feeling for what instance sizes are possible to deal with nowadays
- Get to know the State-Of-The-Art SAT solvers, and on what base approaches they are building upon

# Phase 3

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
- TAOCP, 4B (Knuth)
- Handbook von Biere?

## Random more ideas

- Implement a SAT-solver in a basic language (Assembler, or even TM) (maybe there is something to learn from that?)

