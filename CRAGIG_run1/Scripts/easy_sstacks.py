# EASY SSTACKS
# 20170208
#
# PURPOSE: To write and execute a shell script to run sstacks; sstacks matches individual samples against your catalog for genotyping
# INPUT VIA ARGPARSE:
#
# -p --threads "enable parallel execution with num_threads threads"
# -b --batch "batch number"
# -s --samples "text file with names of each sample to include in sstacks on its own line and without file extension"
# -o --output "output path to write results, e.g., 'Stacks/'"
# -c -- catalog "catalog file for sstacks to use for genotyping individuals, e.g., 'batch_1'"
# -d --dir "relative path to directory with sample files, e.g., 'Stacks/''"
#
# OUTPUT: match files
#
#
#
##########################################################################################

# import modules
import sys
import subprocess
import time
import argparse

# organize parameter inputs with argparse
parser = argparse.ArgumentParser(description="Write and call a sstacks shell script")
parser.add_argument("-p", "--threads", help="enable parallel execution with num_threads threads", type=int)
parser.add_argument("-b", "--batch", help="batch number", type=int, required=True)
parser.add_argument("-s", "--samples", help="text file with names of each sample to include in sstacks on its own line and without file extension", type=str, required=True)
parser.add_argument("-o", "--output", help="output path to write results, e.g., 'Stacks/'", type=str, required=True)
parser.add_argument("-c", "--catalog", help="catalog file for sstacks to use for genotyping individuals, e.g., 'batch_1'", type=str, required=True)
parser.add_argument("-d", "--dir", help="relative path to directory with sample files, e.g., 'Stacks/' or 'pstacks/'", type=str, required=True)
args = parser.parse_args()

# get sample names
names = [] # initiate list
samples = open(args.samples, "r") # open file w filenames
for line in samples:
	name = line.strip()
	names.append(name)
print names # CHECK^
samples.close()

# make a recursive function that asks the user for input
def simple_getinput(prompt, YES_string, NO_string, else_string):
	answer = raw_input(prompt)
	if answer == "YES":
		print YES_string
	elif answer == "NO":
		sys.exit(NO_string)
	else:
		print else_string
		simple_getinput(prompt, YES_string, NO_string, else_string)

# verify to user that you have the right number of samples
numsamples = len(names)

print "\nYou are working with " + str(numsamples) + " samples."

prompt = "\nType YES if correct. Type NO if incorrect and check your files and code."
YES_string = "\nSample number verified. Program continuing."
NO_string = "\nRuh-roh. Something's wrong. Check your files and verify they match your expectations."
else_string = "\nYour answer is not a valid input. Only YES and NO are valid inputs."
simple_getinput(prompt, YES_string, NO_string, else_string)

# make dictionaries to organize args inputs for shell scripting

# make lists of just inputs that will go directly into stacks with same flags - here, all but --samples
stacksin = [args.threads, args.output, args.catalog]
stacksfl = ["-p", "-o", "-c"]

inc_d = {} # initialize dictionary with parameters to include in this script
exc_d = {} # initilize dictionary to store parameters that won't be included in script

numpar = len(stacksin) # get number of parameters to include

for i in range(0,numpar): # sort each arg and its parameter into the appropriate dictionary
	if stacksin[i] == None:
		exc_d[stacksfl[i]] = stacksin[i]
	else:
		inc_d[stacksfl[i]] = stacksin[i]

# write bash script to run sstacks
shellfile = open("sstacks_shell.txt", "w") # create new file for shell script
shellstring = ""

# write sstacks shell script - supposed to look something like stacks sstacks -b 3 -c stacks_b3/batch_3 -s stacks_b3/2005_297_1 -p 10 -o Stacks
for i in range(0,numsamples):
	firststring = "stacks sstacks -g -b " + str(args.batch) + " " + "-s " + args.dir + "/" + str(names[i]) + " "
	secondstring = ""
	for key, value in inc_d.iteritems():
		secondstring += str(key) + " " + str(value) + " "
	linestring = firststring + secondstring
	shellstring += linestring + "\n"
shellfile.write(shellstring)
shellfile.close()

# let the user know the script is done
print "\nFinished writing sstacks shell script. This is what it looks like:"
print "\n" + shellstring + "\n"

prompt = "\nRun this sstacks shell script?"
YES_string = "\nRunning script."
NO_string = "\nWill not run script. Program discontinued."
else_string = "\nYour answer is not a valid input. Only YES and NO are valid inputs."
simple_getinput(prompt, YES_string, NO_string, else_string)

# write timer function
def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

start = start_time = time.time()

# run sstacks shell script
subprocess.call(["sh sstacks_shell.txt"], shell=True)

end = time.time()
timer(start,end)

#end