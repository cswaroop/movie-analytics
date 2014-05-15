#!/bin/bash

## Requirement - namespace named as "test"

aql -c "create index ind on test.demo (write_time) numeric"
java -jar aerospike-load-1.1-jar-with-dependencies.jar  -wt 1 -rt 1 -l 1 -c moviereview.json moviedata.csv -s demo 2>&1 > /dev/null &

echo " " > /tmp/aql_commands
cmd="set lua_userpath 'lua_files'"
echo $cmd >> /tmp/aql_commands
cmd="register module 'lua_files/movies.lua'"
echo $cmd >> /tmp/aql_commands

watch -d 'python most_reviewed.py 10'




