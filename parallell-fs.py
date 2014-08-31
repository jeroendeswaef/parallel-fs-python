#!/usr/bin/python

import os
import shutil
import re

source_dir = "/opt/antlrtry"
target_dir = "/tmp/tt"

ignored_patterns = [".git", ".*\.pyc"]
compiled_patterns = []

symlinked_nodes = { "data": "." }

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

compile_patterns()

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(source_dir):
    relative_root = root.replace(source_dir + '/', '')
    target_root = root.replace(source_dir, target_dir)
    # create new directories
    if not is_ignored(relative_root):
        if not os.path.exists(target_root):
            symlink_origin = get_symlink(relative_root)
            if symlink_origin == '.':
                symlink_origin = source_dir + "/" + relative_root
            if symlink_origin:
                create_symlink(symlink_origin, target_root)
            else:
                print ("Creating dir: ", target_root)
                os.makedirs(target_root)
        for file in files:
            if not is_ignored(file):
                do_copy_file = False
                source_file = root + '/' + file
                target_file = target_root + '/' + file
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
            else:
                print("Ignoring: ", file)
    else:
        print ("Ignoring: ", target_root)