# constantine
An implementation of the Byzantine Chain Replication protocol

## PLATFORM
1. DistAlgo 1.0.9
2. Python 3.6.2
3. Windows 10 Education
4. Ubuntu 16.0.4 on VirtualBox with vagrant

## INSTRUCTIONS
1. To run the system, navigate to the src directory and type in the following command:
python -m da --message-buffer-size {size_in_bytes} --logfile --logfilename {log_file_path_with_name} olympus.da {test-case-path}
Example: python -m da --message-buffer-size 1000000 -F output --logfile --logfilename ../log/testcase1 olympus.da ../test_cases/test_operation_change_fwd_request_t1_single_client.csv
Please note: Enter a significantly large buffer size in bytes, like the size in the example above to avoid running
into buffer constraints.

## CONTRIBUTIONS
1. Client, Olympus, logs, documentation - Soumyadeep
2. Replica, config files, testing - Tushar

## BUGS AND LIMITATIONS
1. For result validation simplicity in the client, we have assumed that the keys used for each client's workload
is segregated on a per client basis.
2. Test for: test_operation_change_fwd_request_t2_multi_client.csv is failing intermittently


## WORKLOAD GENERATION
The workload is being generated from a file containing some random request strings with each
string having the following format:
"operation_name(args)"

## MAIN FILES
src/olympus.da
src/client.da
src/replica.da - Contains replica, head and tail.
src/commons.py - Contains common functions required across Replica, Olympus and Client.
src/log_messages.py - Contains the log messages used in the system.
src/random_tasks.py - Contains randomized workload as specified above. It can be modified if the user so desires.

## CODE SIZE
1. LOC (including spaces and comments) =
    i)   Algorithm code ~ 1510 (~72%)
    ii)  Trigger and maintenance code ~ 420 (~20%)
    iii) Log statements ~ 170 (~8%)
    iv) Total = 2100
2. Mechanism to obtain the LOC = Added counts in IDE and used Find to get the counts of logs

## LANGUAGE_FEATURE USAGE
1. List comprehensions = 3
2. Dictionary comprehensions = 2

## OTHER COMMENTS
1. Tried to use inheritance in DistAlgo with Replica as a base and Head and Tail as subclasses,
but encountered problems with the language.
