#!/usr/bin/python3

from yaml import load, dump

import os
import shutil
import re
import sys

stream = open("settings.yaml", 'r')
settings = load(stream)

source_dir = settings['source_dir']
target_dir = settings['target_dir']

if not os.path.exists(source_dir):
    print("source directory does not exist")
    sys.exit(1)

ignored_patterns = settings['ignored_patterns']
compiled_patterns = []

symlinked_nodes = settings['symlinked_nodes']
added_files = settings['added_files']

def compile_patterns():
    for pattern in ignored_patterns:
        compiled_patterns.append(re.compile(pattern))

def is_ignored(node):
    is_matching = False
    i = 0
    while i < len(ignored_patterns):
        if (compiled_patterns[i].match(node)):
            is_matching = True
        i = i + 1
    return is_matching

def get_symlink(node):
    for key in symlinked_nodes:
        if key == node:
            print (key, node, symlinked_nodes[node])
            return symlinked_nodes[node]
    return None

def create_symlink(origin, dst):
    print ("Creating symlink...", origin, ">>", dst)
    os.symlink(origin, dst)

def get_added_files(dir):
    files_to_add = []
    for key in added_files:
        print(added_files[key], '<->', dir)
        if added_files[key] == dir:
            files_to_add.append(key)
    return files_to_add

def copy_if_necessary(source_file, target_file, target_root):
    do_copy_file = False
    if os.path.exists(target_file):
        t = os.path.getmtime(source_file)
        t2 = os.path.getmtime(target_file)
        if t != t2:
            do_copy_file = True
    else:
        do_copy_file = True
    if do_copy_file:
        print ("Copying file ", source_file)
        shutil.copy2(source_file, target_root)

compile_patterns()

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(source_dir):
    relative_root = root.replace(source_dir + '/', '')
    target_root = root.replace(source_dir, target_dir)
    ignore_copying_files = False
    # create new directories
    if not is_ignored(relative_root):
        if not os.path.exists(target_root):
            symlink_origin = get_symlink(relative_root)
            if symlink_origin == '.':
                symlink_origin = source_dir + "/" + relative_root
            if symlink_origin:
                create_symlink(symlink_origin, target_root)
                ignore_copying_files = True
            else:
                print ("Creating dir: ", target_root)
                os.makedirs(target_root)
        if not ignore_copying_files:
            files_to_copy = []
            for file in files:
                if not is_ignored(file):
                    source_file = root + '/' + file
                    target_file = target_root + '/' + file
                    files_to_copy.append({'source': source_file, 'target': target_file})
                else:
                    print("Ignoring: ", file)

            for file_to_copy in files_to_copy:
                copy_if_necessary(file_to_copy['source'], file_to_copy['target'], target_root)

            for added_file in get_added_files(relative_root):
                copy_if_necessary(added_file, added_file.replace(os.path.dirname(added_file), target_root), target_root)

    else:
        print ("Ignoring: ", target_root)