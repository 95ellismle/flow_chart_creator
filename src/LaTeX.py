#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 16:39:24 2017

@author: mellis
"""
from src import text as txt_lib
from src import IO as io

import subprocess as sb
import os
import numpy as np

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

# Make strings safe for LaTeX
def TeX_check(s):
    s = s.replace("_", "\_")
    return s

# Builds the pdf flow chart
def build_tex(tex_folder, mod_name):
    base_filepath = tex_folder+mod_name
    extensions = ['tex','pdf','aux','log']
    filepaths = {i:io.folder_correct(base_filepath+'.'+i) for i in extensions}
    remove_filepaths = [io.folder_correct(os.getcwd()+'/'+mod_name+'.'+i) for i in ['aux','log']]
    jnk_filepath = io.folder_correct(base_filepath+'6sfdsafo7re_4adsfsd.tmp')
    sb.call("pdflatex %s > %s"%(filepaths['tex'],jnk_filepath), shell=True)
    os.remove(jnk_filepath)
    for i in remove_filepaths:
        os.remove(i)
    os.rename(io.folder_correct(os.getcwd()+'/'+mod_name+'.pdf'), filepaths['pdf'])
    sb.call("xdg-open %s"%filepaths['pdf'], shell=True)


def shift_sorter(ang, iteration, length, fact=1, alt_fact=0.5):
    fit = np.polyfit([5,24], [1,5], 1)
    r = np.polyval(fit, length)
    rad2deg = (2*np.pi)/360
    if length > 10:
        if iteration %2 == 0:
            xshift = r*np.cos(ang*rad2deg)
            yshift = r*np.sin(ang*rad2deg)
        else:
            xshift = alt_fact*r*np.cos(ang*rad2deg)
            yshift = alt_fact*r*np.sin(ang*rad2deg)
    else:
        xshift = r*np.cos(ang*rad2deg)
        yshift = r*np.sin(ang*rad2deg)
    return xshift*fact, yshift*fact

# Creates the call bubbles in the concept map
def calls2flow(calls, parent_ang):
    s = ''
    min_sep = 36
    len_calls = len(calls)
    angles = np.zeros(len_calls)
    if len_calls < 11:
        for i in range(len_calls):
            angles[i] = (parent_ang - min_sep*((len_calls/2) - 0.5 - i))%360
            
        if  any(357<i or i<3 for i in angles):
             angles += 17
        elif any(177<i<183 for i in angles):
            angles -= 17
        for i, call in enumerate(calls):
            s += '\nchild [grow=%.3f, concept color = red!9] {node {%s}}'%(angles[i], TeX_check(call))
    else:
        calls = {i:['{\scriptsize %s}'%s,'bob'] for i,s in enumerate(calls)}
        s += subs2flow(calls, fact=0.3, alt_fact=0, col='red!9')
    return s

# Removes any calls that don't really show much
def calls_tidy(calls, remove=['section']):
    calls = list(set([call for call in calls if any(rem not in call for rem in remove)]))
    return calls

# Creates the subroutine bubbles in the concept map
def subs2flow(dictionary, calls=False, fact=1, alt_fact=0.5, col='red!17'):
    sib_ang = 360/len(dictionary)
    s = ''
    for i in dictionary:
        SR_name = dictionary[i][0]
        ang = (sib_ang*i) - 17
        if calls:
            unique_calls = calls_tidy(calls[i])
            xshift, yshift = shift_sorter(ang, i, len(unique_calls),  fact=fact*2)
        else:
            xshift, yshift = shift_sorter(ang, i, len(dictionary),  fact=fact, alt_fact = alt_fact)
        s += '\nchild [grow=%.3f, xshift=%.3f cm, yshift=%.3f cm, concept color = %s] { node { %s }'%(ang, xshift, yshift, col, TeX_check(SR_name))
        if calls:    
            s += calls2flow(unique_calls, ang)
        s += '}'
    return s

# Creates the flow chart in tikz
def flow_chart(path, subroutines, calls, functions=False):
    mod_name = txt_lib.path2name(path)
    
    s = '\documentclass[12pt,a4paper]{article}'
    s += '\n'
    s += inc(['tikz', 'geometry'], [[],['margin=2cm']])
    s += inc(['shapes, arrows', 'mindmap'], Type='usetikzlibrary')

    s += '\n\n\n\\begin{document}'
    s += '\\resizebox{\\textwidth}{!}{'
    s += '\n\n\\begin{tikzpicture}[mindmap, every node/.style=concept, concept color=red!30, grow cyclic,\n'
    s += 'level 1 concept/.append style={minimum size =0cm}]\n'
    s += "\\node [root concept]{%s}"%mod_name
    s += subs2flow(subroutines, calls)
    
    s += ';'
    s += '\n\\end{tikzpicture}\n'
    s += '}'
    s += '\n\\end{document}'  
    return s





