# Simple Benford's Law Checker

This is a simple python-based web application for checking if the numbers in specified column in user submitted file are following the Benford's Law. 

# Current state
This is a very first draft. The app has limited functionality - for now it only draws a bar plot of distribution of first significant digits in user submitted data vs. distribution of fist first significant according to Benford's Law.

## Getting Started

In order to tun the app you need only to build a Docker image and run it:

```
docker build --tag simple-blc .
```
and run it:
```
docker run --publish 5000:5000 simple-blc
```
