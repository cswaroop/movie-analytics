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

verbose = False
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
	end_time   = int(time.time())
	start_time = end_time - int(sys.argv[1])

# hit movie
	text_file = open("/tmp/sql.txt", "w")
	sql_cmd   = "SET LUA_USERPATH 'lua_files/'"
	text_file.write(sql_cmd+"\n")
	sql_cmd   = "register module 'lua_files/movies.lua'"
	text_file.write(sql_cmd+"\n")
	sql_cmd   = "aggregate movies.hit_movie() on test.demo where write_time between " + str(start_time) + " and " + str(end_time)
	text_file.write(sql_cmd+"\n")
	
	text_file.close()
	command = "Run \'/tmp/sql.txt\'"
	result = run_aql_command(command)
	str1=""
	res =""
	for r in result['json']:
		for k in r:
			str1 = k['hit_movie']
	max = 0;
	result_str = "None"
	if not str1:
		print "No data found"
		return
	for k,v in str1.iteritems():
		v = int(v)
		if max < v:
			max = v
			result_str = k
	movie_name = result_str
	print "Trending movie " + result_str + " in last "+ str(end_time-start_time)+" seconds. It got reviewed " + str(max) + " number of times."
#############################################################################################
	# avg rating
	text_file = open("/tmp/sql.txt", "w")
	sql_cmd   = "SET LUA_USERPATH 'lua_files/'"
	text_file.write(sql_cmd+"\n")
	sql_cmd   = "register module 'lua_files/movies.lua'"
	text_file.write(sql_cmd+"\n")
	sql_cmd   = "aggregate movies.avg_rating(\'"+movie_name+"\') on test.demo where write_time between " + str(start_time) + " and " + str(end_time)
	text_file.write(sql_cmd+"\n")
	text_file.close()
	command = "Run \'/tmp/sql.txt\'"
	result = run_aql_command(command)

	str1=""
	for r in result['json']:
		for k in r:
			str1 = k['avg_rating']
	if not str1:
		print "No data found"
		return
	
	print "avg rating during this time " + str(str1)

##############################################################################################
	# active_user
	text_file = open("/tmp/sql.txt", "w")
	sql_cmd   = "SET LUA_USERPATH 'lua_files/'"
	text_file.write(sql_cmd+"\n")
	sql_cmd   = "register module 'lua_files/movies.lua'"
	text_file.write(sql_cmd+"\n")
	sql_cmd   = "aggregate movies.active_user() on test.demo where write_time between " + str(start_time) + " and " + str(end_time)
	text_file.write(sql_cmd+"\n")
	text_file.close()

	command = "Run \'/tmp/sql.txt\'"
	result = run_aql_command(command)
	str1=""
	res =""
	for r in result['json']:
		for k in r:
			str1 = k['active_user']
	max = 0;
	result_str = "None"
	if not str1:
		print "No data found"
		return
	
	if str1:
		for k, v in str1.iteritems():
			v = int(v)
			if max < v:
				max = v
				result_str = k
	
	print "Most active user during this time was " + result_str + " who submitted review " + str(max) + " number of times."

main()
