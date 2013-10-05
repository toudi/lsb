lsb
===

Lightweight Service Bus

Disclaimer
==========
At current state, this code is merely a proof of concept.

Here's the concept:

you have multiple scouts, which listen for jobs you want to do.
each scout can have multiple middleware classes it handles

after digging trough every middleware, the job is then passed to job server (the proof of concept uses gearman)

that's all for now :D

Usage
=====

**client.py** - this is the code that sends a job to be scheduled. currently, this is done asynchronous due to the proof-of-concept stage, but synchronous call is obviously possible ;)

**worker.py** - this is gearman worker that handles the actual job to be processed. in the future, the input data will be encrypted (see below)

**scout**     - this is the scout module. client connects randomly to 1..n instances of scout and sends job he wants to run.


in order to view the mind blowing demo (lol) you must do the following:

```
0/ (install the gearman server)
1/ virtualenv env
2/ source env/bin/activate
3/ pip install -r requirements.txt
4/ python worker.py (start the worker process)
5/ python scout/__init__.py (start the scout daemon)
6/ python client.py
```

Encryption
==========

I don't have the code yet, but the assumption is this:

- scout **must** have a database with registered public keys of the workers - this will prevent somebody from creating a fake worker which would sniff for the tasks.
- each worker when starting the work **must** contact scout module for acquiring the password
- scout can then use the public key to encrypt symmetrical password and send it to worker
- worker uses it's private key to decrypt the message and thus obtaining password for decrypting jobs
- each password **should** be different per worker.
