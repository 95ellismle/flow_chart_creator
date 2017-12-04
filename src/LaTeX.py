#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 16:39:24 2017

@author: mellis
"""

#Includes packages in LaTeX
def inc(packages, args=False, Type='usepackage'):
    s = ''
    for i, package in enumerate(packages):
        s += '\n\\%s'%Type
        if args:
            if args[i]:
                s += '['
                for arg in args[i]:
                    s += arg + ', '
                s = s[:-2]+ ']'
        s += '{'+package+'}'
    return s

# Extracts the filename from the path
def path2name(filepath):
    p = filepath.split("/")
    p = p[-1][:p[-1].find('.')]
    p = p.replace("_", " ")
    p = ' '.join([i[0].upper() + i[1:].lower() for i in p.split(' ')])
    return p

# Make strings safe for LaTeX
def TeX_check(s):
    s = s.replace("_", "\_")
    return s

# Creates the flow chart in tikz
def flow_chart(path, subroutines, calls=False):
    mod_name = path2name(path)
    
    s = '\documentclass[12pt,a4paper]{article}'
    s += '\n'
    s += inc(['tikz', 'geometry'], [[],['margin=2cm']])
    s += inc(['shapes, arrows', 'mindmap'], Type='usetikzlibrary')

    s += '\n\n\n\\begin{document}'
    s += '''\n\n\\begin{tikzpicture}[mindmap, every node/.style=concept, concept color=red!20, grow cyclic]\n'''
    
    s += "\\node [root concept]{%s}"%mod_name
    for i in subroutines:
        SR_name = subroutines[i][0]
        s += '\nchild { node { %s }'%TeX_check(SR_name)
        s += '}'
    s += ';'
    s += '\n\\end{tikzpicture}\n'
    s += '\n\\end{document}'  
    return s





