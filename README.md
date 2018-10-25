# color-counter
Get most common colors (in descending order) from a list of URLs.

Setup
=====

The application is a standard python application, but in case you don't want to pollute your environment at all you can run it in docker.

Only python 3.6 is supported.

----

To build docker image:
````
make build
````

To run tests in docker:
````
make test
````

Pytest is used, so run `pytest` only if you are not running in the docker.

To ssh to docker container:

````
make debug
````

You can change logging level in `logger.py` to get out more output.

Usage
=======

Main application is `ccounter/color_counter.py`. You must specify input file, all other arguments are optional. By default it will return 3 most common colors and save the result into `INPUT FILE-colors.csv`. You can specify `--output_file` if you want to specify file where to write the results, or `--number-of-colors` to specify how many colors you would like to get back.

If you want to run the application in docker, you can run `color_counter` bash script, but it doesn't support specifying output file (you can still select number of colors though).

Example:
````
$ ./color_counter ../small-urls.txt
````

Errors (if any) will be printed out periodically (every 100 errors) or at the end of the program, whichever comes first.

Implementation
==============

The app works with async loop and has several stages for the entire pipeline. By default it will keep up to 50 images in the entire pipeline.

`reader` sequentially reads the input file line by line in asynchronous manner to ensure it never blocks the event loop. Read URLs get are inserted into queue (`in_files`).

`fetcher` asynchronously reads the queue and delegates input to a pool of processes that download the images and put their binary representation to the second queue (`analysis`) where they wait to get processed by `counter`.

`counter` loads the images from `analysis` and delegates them to a pool of processes that use numpy and numba to converts the pixels to integers and flatten the integers into single dimensional array on which we perform uniqueness and counting to get back N most common pixels. The result is put into third queue (`results`).

`writer` reads the `results` queue and asynchronously writes it out into output file.

Any errors are put into fourth queue (`failed`) that is read by `errorhandler` where they are periodically flushed (by default with pretty messages, but if you change the logging level you can get back full tracebacks). 

To scale
========

Replace local queues with RabbitMQ or similar and scale out fetcher and counter (if needed) to multiple instances.