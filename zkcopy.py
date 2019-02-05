#!/usr/bin/env python3

import getopt
import sys

import kazoo.exceptions

from kazoo.client import KazooClient


def copy_node(zk_src, zk_dst, src_path, dst_path):
    node_data, node_stat = zk_src.get(src_path)
    print('Copying {} ...'.format(dst_path))
    zk_dst.ensure_path(dst_path)
    zk_dst.set(dst_path, node_data)
    if node_stat.numChildren == 0:
        return
    for src_node in zk_src.get_children(src_path):
        src_node_path = src_path + '/' + src_node
        dst_node_path = dst_path + '/' + src_node
        node_data, node_stat = zk_src.get(src_node_path)
        print('Copying {} ...'.format(dst_node_path))
        try:
            zk_dst.create(dst_node_path, node_data)
        except kazoo.exceptions.NodeExistsError:
            zk_dst.set(dst_node_path, node_data)
        if node_stat.numChildren > 0:
            copy_node(zk_src, zk_dst, src_node_path, dst_node_path)


def main():
    try:
        opts, args = getopt.getopt(
                sys.argv[1:],
                's:d:uz:',
                [
                    'zookeeper=',
                    'source-zk=',
                    'source-path=',
                    'destination-zk=',
                    'destination-path=',
                    'update',
                ])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    src_zk = None
    src_path = None
    dst_zk = None
    dst_path = None
    delete_before_copy = True
    for opt, arg in opts:
        if opt in ('-z', '--zookeeper'):
            src_zk = arg
            dst_zk = arg
        elif opt in ('', '--source-zk'):
            src_zk = arg
        elif opt in ('', '--destination-zk'):
            dst_zk = arg
        elif opt in ('-s', '--source-path'):
            src_path = arg
        elif opt in ('-d', '--destination-path'):
            dst_path = arg
        elif opt in ('-u', '--update'):
            delete_before_copy = False
        else:
            assert False
    if None in (src_zk, dst_zk, src_path, dst_path):
        print('ERROR: no Zookeeper instance or source path or destination path provided.')
        sys.exit(2)
    if not src_path.startswith('/') or not dst_path.startswith('/'):
        print('ERROR: Paths must start with "/".')
        sys.exit(0)
    if len(src_path) > 1 and src_path.endswith('/'):
        print('ERROR: Source path must not end with "/".')
        sys.exit(2)
    if dst_path.endswith('/'):
        if src_path == '/':
            dst_path = dst_path[:-1]
        else:
            dst_path = dst_path + src_path.rsplit('/', 1)[-1]
    zk_src = KazooClient(src_zk)
    if dst_zk == src_zk:
        zk_dst = zk_src
    else:
        zk_dst = KazooClient(dst_zk)
    zk_src.start()
    zk_dst.start()
    if not zk_src.exists(src_path):
        print('ERROR: Source path "{}" does not exist.'.format(src_path))
        sys.exit(2)
    if delete_before_copy:
        print('Deleting {} ...'.format(dst_path))
        zk_dst.delete(dst_path, recursive=True)
    copy_node(zk_src, zk_dst, src_path, dst_path)
    zk_src.stop()
    zk_dst.stop()
    print('Done.')


if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 tw=100 et:
