# CMPE273 Assignment 2

Implementing a RocksDB replication in Python using the design from this C++ replicator. (https://medium.com/@Pinterest_Engineering/open-sourcing-rocksplicator-a-real-time-rocksdb-data-replicator-558cd3847a9d) (Links to an external site.)Links to an external site.You can use Lab 1 as a based line. Differences form the replicator are:

1. You will be using GRPC Python server instead of Thrift server.
2. You will be exploring more into GRPC sync, async, and streaming.
3. You can ignore all cluster management features from the replicator.

### How to Use

1. Make sure you have python dependencies installed from requirements.txt (Tested on Python2.7)

    ```
    source venv/bin/activate
    pip install -r requirement.txt
    ```

2. Start master_server.py to start master replicator.

    ```
    python master_server.py
    ```

3. Start follower replicator clients: Code supports muliple client to start replication at the same time

    ```
    python follower_client.py <follower_db_id>
    ```

    Example: Start three follower client on 3 different terminals
        
        python follower_client.py 1
        python follower_client.py 2
        python follower_client.py 3
        

4. Start Pushing data to master_server with the following file

    ```
    python pushData.py <key> <value>
    ```
    
    Example: Put data to master databse with ("key1", "value1")
        
        python pushData.py key1 value1
        python pushData.py key2 value2
        

After executing this script it will be replicated to all the running follower_databases.

5. Read data from slave(Follower) database.

    First stop the replication server so that RocksDB allows reading from the slave database. (Else it will give you an error related to database lock.)

    ```
    python getData.py <follower_db_id> <key>
    ```
    
    Example 1: If you want to get value of "key1" from follower_db_id "1" then
        
        python getData.py 1 key1
    
    Example 2: If you want to get value of "key3" from follower_db_id "2" then
        
        python getData.py 2 key5