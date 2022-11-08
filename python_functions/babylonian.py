#!/usr/bin/env python3

def babylonian(number):
    """
    Find the square root of a number using babylonian method
    """
    lower = 0
    upper = number
    while upper - lower > 0.0001:
        upper = (upper+lower)/2
        lower = number/upper

    print(upper)


babylonian(7)
