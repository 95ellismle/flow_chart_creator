#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:30:54 2017

@author: mellis
"""
import subprocess as sb
import os


# Returns all instances of Fortran files matching the pattern specified. 
# It will check for instances of *pattern* first and if multiple files are found it will check to see if just the pattern specified in filename reduces the number of files found.
def find_file(filename, path):
    find_out = sb.check_output("find %s -name '*%s*'"%(path, filename), shell=True)
    if '\n' in find_out:
        flist = [i for i in find_out.split('\n') if i and 'sw' not in i and ".F" in i]
    else:
        flist = []
    if len(flist) == 1:
        filepath = flist[0]
        return folder_correct(filepath)
    elif len(flist) > 1:
        raise IOError("Sorry found too many files with that name!")
    else:
        raise IOError("Sorry can't find the file!")

# Will open, read then close a file safely.
def open_read_close(path):
    f = open(path)
    txt = f.read()
    txt = txt.split('\n')
    f.close()
    return txt

#Checks if the directory exists and makes it if not
def check_mkdir(path, min_depth=2, max_folders=2):
    path = folder_correct(path)
    lpath = path.split('/')
    act_folders = []
    for i in range(2,len(lpath)):
        sub_path = '/'.join(lpath[:i]) 
        if not os.path.isdir(sub_path):
            act_folders.append(False)
        else:
            act_folders.append(True)
    if not all(act_folders[:min_depth]):
        raise(IOError("The required number of folders to be created exceeds the amount allowed."))
    if not all(act_folders[:-max_folders]):
        raise(IOError("Too many folders need to be created please check the filepaths."))
    else:
        for i in range(2,len(lpath)):
            sub_path = '/'.join(lpath[:i]) 
            if not os.path.isdir(sub_path):
                os.mkdir(sub_path)
    return True

# Checks if a filepath or folderpath exists
def path_leads_somewhere(path):
    if os.path.isfile(path) or os.path.isdir(path):
        return True
    else:
        return False

# Returns an absolute file/folder path. Will convert the relative file/folerpaths such as ../foo -> $PATH_TO_PYTHON_MINUS_1/foo
def folder_correct(f, make_file=False):
    f = os.path.expanduser(f)
    folder = False
    if '/' not in f:
        f = './'+f
    flist = f.split('/')
    clist = os.getcwd().split('/')
    if flist[0] != clist[0] and flist[1] != clist[1]:
        cind, find = 0, 0
        for i in flist:
            if i == '..':
                cind += 1
                find += 1
            if i == '.':
                find += 1
        if cind != 0:
            clist = clist[:-cind]
        flist = flist[find:]
    else:
        clist = []
    if '.' not in flist[-1]:
        folder = True
    if flist[-1] != '' and folder:
        flist.append('')
    f= '/'.join(clist+flist)
    if make_file:
        if path_leads_somewhere(f):
            if folder:
                os.mkdir(f)
            else:
                File = open(f, 'a+')
                File.close()
        return f
    else:
        return f

# Saves the LaTeX flow chart code
def Save_Flow(filepath, tex_code):
    filepath = folder_correct(filepath)
    f = open(filepath, 'w+')
    f.write(tex_code)
    f.close()

# Prints in a nice way to the terminal
def printer(fncs, fname,calls, to_print):
    if not to_print:
        to_print = fncs.keys()
    for i in fncs:
        if calls:
            print("\n")
        if i in to_print:
            print("%s %i:\t%s"%(fname, i, fncs[i][0]))
            if calls:
                for calli, call in enumerate(calls[i]):
                    print("\tCall %i:   %s"%(calli+1, call.strip()))
