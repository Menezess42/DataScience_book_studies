import re
def type_file_opening_explanation():
    # 'r' means reading. It's the default option if not definedi
    file = input('File name')
    file_for_reading = open(file, 'r')
    # file_for_reading2 = open(file) Same as before but without specifying the 'r'

    # 'w'write -- but destroy everything in the file that was before.
    file_for_writing = open(file, 'w')

    # 'a' add information to the file -- add something to the end of the file
    file_for_appending = open(file, 'a')

    # don't forget to close the file
    file_for_writing.close()

# As it easy to forget to close files. generally we open then
# with in a block
with open(file_name) as f:
    data = function_that_gets_data_from(f)

# In this point f(the file) was already closed
process(data)

# To read a how text file you just have to iterate the lines
starts_with_hash = 0
with open(file_name) as f:
    for line in f: # reads every line from the file
        if re.match('^#', line): # uses a regex to determine if start with #
            starts_with_hash+=1 # if yes, then add 1 to the counter

    # as every line that is read in this format ended with a new line caracter
    # you have to remove before doing anything

