# SimCC

Simulation of CCHS, using `mypyc` for a 200 millisecond optimisation (for me, using Numba's `cfunc` decorator and generic Python3 takes 1200 ms each iteration whilst compilation with `mypyc` takes 900-1000 ms per iteration)

# Building

The existing `.so` files should work already for MacOS, so skip to [Running](#running). If it doesn't work, go back to this step.

```sh
> pip3 install mypy # if you don't have it already
> ./build.sh
```

# Running

```sh
> ./run.sh
```