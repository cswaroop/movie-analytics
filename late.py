import sys
import os
import getopt
import time
import cmd
import threading
import Queue
import random
import subprocess
import re
from socket import gethostname
import yaml

verbose = True
def make_parseable(contents):
    r = re.compile(r"^OK, ")
    lines = contents.split('\n')
    output = "[\n"
    for line in lines:
        if r.search(line):
            continue
        elif line == "]" or line == "]\r":
            output += "],\n"
        else:
            output += line + "\n"
    output += "]\n"
    return output


def run_aql_command(cmd, node_id=1):
	host = "127.0.0.1"
	port = 3000
	args = ("./aql", "-h", str(host), "-p", str(port), "-o", "json", "-c", cmd )
	popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# cannot use popen.wait() because of a possibility of a deadlock
	(output, errput) = popen.communicate()
	if verbose:
		print "--------------------------------------------"
		print "| " + cmd
		print "--------------------------------------------"
		print output
		print "--------------------------------------------"
		print errput
		print "--------------------------------------------"
	obj1 = None
	if output:
		obj1 = yaml.load(make_parseable(output))
	ret1 = { 'status': popen.returncode, 'stdout': output, 'stderr': errput, 'json': obj1 }
	if popen.returncode == 0 and not output and 'Error' in errput:
		ret1['status'] = 1

	# reset at the end
	return ret1

def main():
	end_time   = 1327948200#int(time.time())
	start_time = 1325356200#end_time - int(sys.argv[1])

# hit movie
	text_file = open("/tmp/sql.txt", "w")
	sql_cmd   = "SET LUA_USERPATH 'lua_files/'"
	text_file.write(sql_cmd+"\n")
	sql_cmd   = "register module 'lua_files/simple_aggregation.lua'"
	text_file.write(sql_cmd+"\n")
	sql_cmd   = "aggregate simple_aggregation.late_flights_by_airline() on test.flights where FL_DATE_BIN between " + str(start_time) + " and " + str(end_time)
	text_file.write(sql_cmd+"\n")
	
	text_file.close()
	command = "Run \'/tmp/sql.txt\'"
	result = run_aql_command(command)
############################################################################################
main()
