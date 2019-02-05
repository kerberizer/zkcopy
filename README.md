# zkcopy
Simple script for copying ZooKeeper nodes

WARNING: The code has not seen much testing. **USE AT YOUR OWN RISK!**

## Requirements
- Python 3
- [kazoo](https://github.com/python-zk/kazoo)

## Quickstart
### Within one cluster
```
./zkcopy.py -z <host>:<port> -s <src_path> -d <dst_path>
```
### Between clusters
```
./zkcopy.py --source-zk=<host1>:<port1> --destination-zk=<host2>:<port2> -s <src_path> -d <dst_path>
```
## Options
```
-z <host>:<port>
--zookeeper=<host>:<port>

        Convenience option to set the ZooKeeper instance when copying within single cluster.


--source-zk=<host>:<port>
--destination-zk=<host>:<port>

        The source and destination ZooKeeper instances.


-s <src_path>
--source-path=<src_path>
-d <dst_path>
--destination-path=<dst_path>

        Source and destination paths. Copying is __always__ performed recursively. When the
        destination path ends with "/", the source path is copied as its __child__, except
        when the source path is "/" itself, in which case it is copied as the destination.

        E.g. `-s /some/path/file.txt -d /some/other/path/` copies file.txt as a child of
        `/some/other/path`, while `-s /some/path/file.txt -d /some/other/file.txt` would
        copy the node directly onto the destination (recursion applies in both cases).

        It is an error to end the source path with "/". Wildcards are not supported.


-u
--update

        Don't delete the destination node tree before copying. If not give, the destination
        node is removed recursively before copying is commenced.
```
