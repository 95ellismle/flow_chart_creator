#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 21:11:14 2017

@author: mellis
"""

# Finds the indices of the lines where the statement appears (such as SUBROUTINE)
def begin_index(ltxt, statement, begin_statement, disallowed_chars):
    all_begin_statement_indices = [i for i, line in enumerate(ltxt) if statement in line.lower()]
    begin_indices = []
    for i in all_begin_statement_indices:
        line = ltxt[i].lower()
        statement_pos = line.find(statement)
        begin_pos = line.find(begin_statement)
        line = line.replace(statement,"")
        line = line[:line.find(begin_statement)]
        line = line.strip()
        if statement_pos < begin_pos and begin_pos != -1 and all(i not in line for i in disallowed_chars):
            begin_indices.append(i)
    return begin_indices

# Finds the indices of the lines where the statement ends (such as END SUBROUTINE)
def end_index(ltxt, begin_index, end_statement, disallowed_chars):
    end_statement = end_statement.lower()
    for i, line in enumerate(ltxt):
        line = line.lower()
        if end_statement in line.lower() and any(i not in line for i in disallowed_chars):
            end_index = i + begin_index
            break
    return end_index

# Extracts the filename from the path
def path2name(filepath):
    p = filepath.split("/")
    p = p[-1][:p[-1].find('.')]
    p = p.replace("_", " ")
    p = ' '.join([i[0].upper() + i[1:].lower() for i in p.split(' ')])
    return p


# Will splice the line to get the name of the subroutine/call etc...
def line_splice(line, statement, begin_statement):
    line = line.lower()
    statement = statement.lower()
    begin_statement = begin_statement.lower()
    splice1 = line.find(statement) + len(statement)
    splice2 = line.find(begin_statement)
    return line[splice1:splice2].strip()

# Will align text left or right
def align(string, len_line=5, rl='r'):
    num_spaces = len_line-len(string)
    if rl == 'r':
        return "".join([" " for i in xrange(num_spaces)]) +  string
    elif rl == 'l':
        return string + "".join([" " for i in xrange(num_spaces)])

# Calls the correct functions in order.
def splicing(ltxt, statement, begin_statement, end_statement, d_on=True, start_d_index=1):
    begin_indices = begin_index(ltxt, statement, begin_statement, ['!', "'", '"', ' ', '%'])
    end_indices = [end_index(ltxt[i:], i, end_statement, ['!', "'", '"', '%']) for i in begin_indices]
    splices = {}
    if d_on:
        for i in range(len(begin_indices)):
            name = line_splice(ltxt[begin_indices[i]], statement, begin_statement)
            txt = ltxt[begin_indices[i]:end_indices[i]+1]
            splices[i+start_d_index] = (name, txt)
    else:
        splices = [line_splice(ltxt[i], statement, begin_statement) for i in begin_indices]
    return splices, begin_indices, end_indices
