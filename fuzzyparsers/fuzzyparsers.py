# -*- coding: utf-8 -*-

import datetime
import re

def default_match(t,item):
    return t.lower()[:len(item)] == item.lower()

def fuzzy_match(target,item,match_fucn=None):
	"""
	target:  list of possible matches
	item:  item to find in the list
	match_fucn:  callable function taking 2 parameters (first from the target list, second is item) and returning a boolean
		if match_fucn is None then it will default initial lower-case matching of strings
	"""

	if match_fucn is None:
		def default_match(t,item):
			return t.lower()[:len(item)] == item.lower()

		match_fucn = default_match

	candidates = [t for t in target if match_fucn(t,item)]
	if len(candidates) == 1:
		return candidates[0]
	elif len(candidates) == 0:
		return None
	else:
		raise ValueError("ambigious match")

def str_to_month(s):
    return fuzzy_match(["january","february","march","april","may","june","july","august","september","october","november","december"], s)

def str_to_date_int(s):
    m = re.match("([a-zA-Z]*) ([0-9]+)(,|) ([0-9]+)",s)
    if m:
        return int(m.group(4)),str_to_month(m.group(1)),int(m.group(2))
    m = re.match("([a-zA-Z]*) ([0-9]+)",s)
    if m:
        return None,str_to_month(m.group(1)),int(m.group(2))
    # yyyy-mm-dd
    m = re.match("([0-9]{4})[-./]([0-9]{1,2})[-./]([0-9]{1,2})",s)
    if m:
        return int(m.group(1)),int(m.group(2)),int(m.group(3))
    # mm-dd-yyyy
    m = re.match("([0-9]{1,2})[-./]([0-9]{1,2})[-./]([0-9]{4})",s)
    if m:
        return int(m.group(3)),int(m.group(1)),int(m.group(2))
    m = re.match("(-|\+)([0-9]+)",s)
    if m:
        if m.group(1)=='+':
            d = datetime.date.today() + datetime.timedelta(int(m.group(2)))
        elif m.group(1)=='-':
            d = datetime.date.today() - datetime.timedelta(int(m.group(2)))
        return d.year,d.month,d.day
    raise NotImplementedError
    return None,None,None

def str_to_date(s):
    """
    Parses input `s` into a date.  The accepted date formats are quite flexible.
    
    jan 12, 2003
    jan 5
    2004-3-5
    +34 -- 34 days in the future (relative to todays date)
    -4 -- 4 days in the past (relative to todays date)
    """
    year,month,day = str_to_date_int(s)
    if year is None:
        year = datetime.date.today().year
    if month is None:
        month = datetime.date.today().month
    if day is None:
        day = datetime.date.today().day
    return datetime.date(year,month,day)
