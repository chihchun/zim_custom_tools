#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Rex Tsai 2013
# 
# Usage: doittomorrow.py %s %n
# 
# This script move all un-checked task to tomorrow page, 
# and xchecked the tasks in currenet page.

import sys
import pprint
import copy
import os
from datetime import date, timedelta

from zim.formats import ParseTree, Element, TreeBuilder, ParseTreeBuilder, get_format, UNCHECKED_BOX, CHECKED_BOX, XCHECKED_BOX

def main(orig_file, notebook_path):
    assert(os.path.isdir(notebook_path))
    assert(os.path.isfile(orig_file))

    dumper = get_format('wiki').Dumper()
    parser = get_format('wiki').Parser()

    text = open(orig_file).read()
    parsetree = parser.parse(text)
    newtree = ParseTree().fromstring("<zim-tree></zim-tree>")

    for para in parsetree.findall('p'):
        p = Element("p")
        for node in flatten_list(para, para):
            p.append(node)
        newtree.getroot().extend(p)

    # new todo list
    text = ''.join(dumper.dump(newtree)).encode('utf-8')

    tomorrow = date.today() + timedelta(1)

    directory = os.path.join(notebook_path, "Calendar", str("%04d" % tomorrow.year), str("%02d" % tomorrow.month))
    filename = "%02d.txt" % tomorrow.day
    if (not os.path.exists(directory)): os.makedirs(directory)

    # write tasks to tomorrow page.
    with open(os.path.join(directory, filename), 'a+') as the_file:
         the_file.write(text)

    # update original wiki page.
    text = ''.join(dumper.dump(parsetree) ).encode('utf-8')
    with open(orig_file, 'w') as the_file:
         the_file.write(text)
    
def flatten_list(node, parent = None, copied = False):
    for child in node.getchildren():
        if child.tag in ('li') and child.get('bullet') not in (CHECKED_BOX, XCHECKED_BOX):
            if copied is False:
               yield copy.deepcopy(parent)
               copied = True
            # makr the bullet xchecked as record.
            child.set('bullet', XCHECKED_BOX)
       
        for i in flatten_list(child, node, copied):
            yield i

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
