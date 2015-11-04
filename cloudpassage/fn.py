#!/usr/bin/env python
# Some basic data handling functions

def merge_dicts(first, second):
    final = first.copy()
    final.update(second)
    return(final)
