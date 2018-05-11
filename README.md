# better_logging

This is faster than logging and simply writing to a file. It is also faster when threaded or with multiprocessing. It is almost as simple as writing to the file, but with a little bit of smarts.

better_logging has a Controller that manages the set up of logging. Importing the logger sets allows for just one Controller per project that implements better_logging. Importing the module for the first time spins up a thread that attempts to drain a queue. Every call to log a message move it's memory in to the Queue and then immediately returns to the user, off-putting all writing to a file on the logging thread. To simplify everything, there is a standard format that will be printed. Right now, this only works on Linux as I have not investigated getting the thread id on Windows (not the threading.get_ident() magic cookie).

better_logging will attempt to drain this message Queue on exit, but it depends on a graceful exit. When writing production applications it is recommended that the main thread hand all exceptions and only terminate with grace.
