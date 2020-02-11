# Types at the edges in python
## Explanation
Having greater type safety around the edges of a python service can
really help improve the quality of error messages and the general design
of the system. This is a small refactor/bug fixing exercise to try and demonstrate
how pydantic, mypy and types in general can help with this.

In the example code we've setup a system that imports entries from an external
diary API and does the following:

  * indexes them by title, 
  * indexes them by category 
  * stores an ordered list of entries.

The code that calls the API uses a Pydantic model to represent the shape
we think the data has.


## How to run this exercise
### Requirements
This tutorial assumes you have at least python 3.6 and have pipenv.

### Setup
Run the following to prepare the environment and get the dependencies:
```bash
make setup
```

You can validate everything is installed by running:
```bash
make test
```

### Day zero
Take a look around the code in `diary`. You'll be free to change
and add anything in this directory.

We've been given a dev server to test our code against to validate 
everything works correctly run
```bash
make run-0
```
you should see output like:
```
Successfully indexed data
1000 entries
2 unique titles
1 unique categories
```
So our first job is complete we'r ready to go.

### Days 1 - 3
The software is now live. Run :

```bash
make run-1
```

The system will catch the first validation error and display it. 
There's also some helpful text about why this error is now 
happening (what fact has been discovered).

Start altering the code to fix this bug. You can change
anything in `diary` and add any tests you need. Running 
`make test` regularly will help guide you.

Once you're happy run `make run-1` again. If it completes successfully
then move on to the next day.

## Tips
 * Focus on the class `DiaryEntry` this encodes our assumptions about the API data. 
 * Make use of types and mypy - this is the point of the exercise after all.