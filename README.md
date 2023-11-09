# SimpleConcurrentMapper
Simple wrapper classes for async python MP/MT jobs. This Python script provides a utility for concurrent task execution using the `concurrent.futures` module. It introduces a custom `PseudoPoolExecutor` class that mimics the behavior of a pool executor, along with a `PseudoFuture` class to represent future results.


## Usage

```python
from concurrent_mapper import concurrent_submit

# Example usage
def example_function(task):
    # Your task logic here
    return result

tasks = [task1, task2, task3]

# Submit tasks concurrently
for result in concurrent_submit(fn=example_function, tasks=tasks, nproc=4, chunk_size=2, mode='mt'):
    print(result)
```

## One interface

```python
concurrent_mapper.concurrent_submit(*, fn : callable, tasks : iterable, other_args=tuple(), kwargs=dict(), nproc = 4, chunk_size = 0, mode = 'mt'/'mp'/'seq')
```

Witch submit `fn(*((task[i], ) + other_args), **kwargs)` to a queue with max length `nproc`, the maximum concurrent jobs.

## Configuration

- `fn`: The function to be executed concurrently.
- `tasks`: List of tasks to be processed.
- `other_args`: Additional arguments to be passed to the function.
- `kwargs`: Keyword arguments to be passed to the function.
- `nproc`: Number of processes or threads to use.
- `chunk_size`: Size of task chunks for parallel processing.
- `mode`: Execution mode ('mp' for multiprocessing, 'mt' for multithreading, 'seq' for sequential).

## Classes and Functions

### PseudoFuture

A simple class representing a "future" object with the following methods:

- `__init__(self, aresult)`: Initializes the future with a result.
- `done(self)`: Returns True, indicating that the task is completed.
- `result(self, timeout=None)`: Returns the result passed during initialization.
- `cancel(self)`: Always returns False.
- `cancelled(self)`: Always returns False.
- `running(self)`: Always returns False.

### PseudoPoolExecutor

A custom class inheriting from `concurrent.futures.Executor`. It has a `submit` method that takes a function and its arguments, then returns a `PseudoFuture` instance.

### iterator_split

A generator function that splits an iterable into chunks of a specified size.

### concurrent_submit

The main function for concurrent task submission. It takes parameters for the function (`fn`), tasks, additional arguments (`other_args`), keyword arguments (`kwargs`), number of processes (`nproc`), chunk size (`chunk_size`), and mode.



---
