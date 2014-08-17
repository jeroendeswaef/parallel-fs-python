#!/usr/bin/python

import os
import shutil

source_dir = "/opt/antlrtry"
target_dir = "/tmp/tt"


# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(source_dir):
    target_root = root.replace(source_dir, target_dir)
    if not os.path.exists(target_root):
        print ("Creating dir: ", target_root)
        os.makedirs(target_root)
    for file in files:
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