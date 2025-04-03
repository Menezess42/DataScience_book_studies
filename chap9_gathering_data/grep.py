import sys, re

# sys.argv is its list of command-line arguments
# sys.argv[0] is its name of the program
# sys.argv[1] it will be the regex specified in command-line

regex = sys.argv[1]

# for each line inserted in the script
for line in sys.stdin:
    # if correspond to regex, write in stdout
    for line in sys.stdin:
        sys.stdout.write(line)
