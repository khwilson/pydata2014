PyData2014 Materials
====================

These are supplementary materials for my talk on Determining Skill Levels
at PyData2NYC 2014.

Football
--------

The football package parses and manipulates
* cfb2013lines.csv
* conferences.csv

`cfb2013lines.csv` is a csv of the winners and losers of all college
football games in 2013.

`conferences.csv` is just a mapping from team to an abbreviation of their
conference name (sorry for any inconsistencies; 2013 data is hard to get at
strangely).

The package itself has three main modules:
* `base` for manipulating the data
* `elo` for doing Elo's method on this data
* `make_graph` for producing a win/lose directed dot graph, which you should
  compile with `fdp`.

To use `make_graph`, simply run `python football/make_graph`.

To use `elo`, see the example in `Elo.ipynb`.

IRT
---

The IRT package contains a simple implementation of 1PL IRT with normal priors.
It contains a `simulate` function that allows you build data sets, and then
a `make_irt_neg_objective` function which you can use with `scipy.optimize` to
learn the latent parameters.

For an example of usage, see `IRT.ipynb`.

Tools
-----

I've also included some tools for doing finite-difference tests of jacobians
and hessians. Doing finite-difference tests is *critical* for testing whether
or not your fast implementations of these functions actually match your
objective. If they do not, then you're going to quickly get in trouble with
line search algorithms.

Exercises
---------

Since this was an intermediate talk, I guess I can assign people who come here
exercises:

1. Here's a simple one. Fork this repo and add the gradients and
   hessians of the elo and irt objectives to the packages. No credit if you do
   not *test* these functions, which you can do with the finite-difference tests
   available in the `tools` package.

2. Then play around with the tools. Find other data sets or simulate larger
   data sets. When do the tools break? What assumptions might break down?

3. Be the BCS! Add priors to Elo's method to get your favorite team to the top.
   Some simple ones you could try are:
   - Put a normal prior centered at 1.0 on your favorite team's skill and a
     prior centered at 0.0 for everyone else's. What happens (especially, what
     happens to their conference)?
   - Put a prior on a whole conference. What happens?
   - Put a *nondiagonal* prior on the teams. For instance, try putting a prior
     on every conference that the skills across the conference will be
     normally distributed. How would you do that? Why might you think that's
     a reasonable prior?

License
-------

Everything in this repository is licensed under the Apache 2.0 license.
