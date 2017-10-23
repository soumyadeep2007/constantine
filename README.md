# constantine
An implementation of the Byzantine Chain Replication protocol

## PLATFORM
1. DistAlgo 1.0.9
2. Python 3.6.2
3. Windows 10 Education
4. Ubuntu 16.0.4 on VirtualBox with vagrant

## INSTRUCTIONS
1. To run the system, navigate to the src directory and type in the following in a command prompt
python -m da --logfile --message-buffer-size 100000 olympus.da

## CONTRIBUTIONS 

## BUGS AND LIMITATIONS
1. If head changes the operation, the system cannot handle it.  ``

## WORKLOAD GENERATION
The workload is being generated from a file containing some random request strings with each
string having the following format:
"operation_name(args)"

## MAIN FILES
src/olympus.da
src/client.da
src/replica.da - Contains replica, head and tail
src/commons.py - Common functions required by each process
src/random_tasks.py - Contains randomized workload as specified above

## CODE SIZE
1. LOC =
2. N

## LANGUAGE_FEATURE USAGE
1. List comprehensions =   

