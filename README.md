movie-analytics
===============

Example of realtime analytics in aerospike using movie review database.

###Getting the code
The source code for this example is available on GitHub, at https://github.com/aerospike/movie-analytics.git

Clone the GitHub repository using the following command:
```
git clone https://github.com/aerospike/movie-analytics.git
```

###Test data
The movie review dataset is available from Stanford Network Analysis Projects(http://snap.stanford.edu/data/web-Movies.html). After cleaning and taking subset of 141K reviews we store them in a csv file called moviedata.csv . Description of columns are productId,userId,userId_productId,profileName,helpfulness(in percentage),rating,review_time respectively.

###Load data
Data can be loaded using the [Aerospike Loader](https://github.com/aerospike/aerospike-loader). This a multi-threaded CSV loader that takes full advantage of the hardware capabilities to load data rapidly.

[Aerospike Loader](https://github.com/aerospike/aerospike-loader) uses a JSON formated configuration file to map each column to a Bin name and type. The configuration file ```moviereview.json``` in the project root directory.

To load the data using [Aerospike Loader](https://github.com/aerospike/aerospike-loader), use this command:
```bash
./run_loader -h localhost -c <project root>/moviereview.json <project root>/moviedata.csv
``` 

###Steps to run analytics:

####Prerequisites:
- Aerospike server running
- Aerospike tools installed

####To run quickly: 
    ./run_all.sh

####Mannual steps:
- Create index on write_time
```aql
    aql -c "create index ind on test.demo (write_time) numeric"
```
- Load data slowly in aerospike
```java
    java -jar aerospike-load-1.1-jar-with-dependencies.jar  -wt 1 -rt 1 -l 1 -c moviereview.json moviedata.csv -s demo
```
- Run aggregation
```aql
    ./aql -o json
    set lua_userpath 'lua_files'
    register module 'lua_files/movies.lua'
    aggregate movies.hit_movie() on test.demo where write_time between <current epoch time - 10> and <current epoch time + 10>
    exit
```
- Run the python script to get analytics in past X seconds. 
```python
python most_reviewed.py X
```
