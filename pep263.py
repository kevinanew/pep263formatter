#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import re


def find_python_files(dir):
    assert os.path.exists(dir)
    for root, dir, files in os.walk(dir):
        for _file in files:
            file_abs_path = os.path.join(root, _file)
            _, ext = os.path.splitext(file_abs_path)
            if ext == '.py':
                yield file_abs_path


def add_encoding(python_file_path, backup_file):
    assert os.path.exists(python_file_path)
    _, ext = os.path.splitext(python_file_path)
    assert ext == '.py'

    with open(python_file_path) as python_in, open(
            '%s.formatted' % python_file_path, 'w') as python_out:
        for line in python_in.readlines():
            new_line = replace_encode_if_need(line)
            python_out.write(new_line)

    if backup_file:
        os.rename(python_file_path, '%s.bak' % python_file_path)

    os.rename('%s.formatted' % python_file_path, python_file_path)


def replace_encode_if_need(line):
    coding_re = "^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)"
    result = re.search(coding_re, line)
    if result:
        new_line = '# -*- coding: %s -*-\n' % result.groups()[0]
        return new_line
    return line


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=u'按pep263来格式化python文件')
    parser.add_argument(
        '-f', '--file', type=str, help=u'python 文件路径', required=False)
    parser.add_argument(
        '-d', '--dir', type=str, help=u'python 文件所在的目录', required=False)
    parser.add_argument(
        '-b', '--backup', help=u'备份 python 文件', required=False,
        default=False, action='store_true')

    args = parser.parse_args()
    if args.file:
        add_encoding(args.file, args.backup)
        raise SystemExit

    if args.dir:
        for python_file in find_python_files(args.dir):
            print python_file
            add_encoding(python_file, args.backup)
        raise SystemExit

    parser.print_help()
