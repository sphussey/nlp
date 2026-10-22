#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title: re_matching.py
Version: 1.0.0
Description:
	1. This function determines is a provided string:
		a. starts with single asterisk.
		b. contains at least one word ending in "oxy"
			followed by whitespace.
		c. sentence must not contain any punctuation.
	2. This function extracts voltages from a specific string per design.
	(see test_1) t is not designed to be a general voltage extracter.

Author: Shane Hussey
Create Date: 2026-10-21
Licence: MIT
Usage:
	python re_matching.py

"""



import re

def regex_match(string: str) -> str:
	"""
	This function determines is a provided string:
		1. starts with single asterisk.
		2. contains at least one word ending in "oxy"
			followed by whitespace.
		3. sentence must not contain any punctuation.

	:string: str: string to be checked for match
	:return: str: returns the string if it matches the criteria
					or "No match." is no match
	"""
	re_string = r"^(\*)[a-zA-Z\s\n]*([a-zA-Z]oxy\s)[a-zA-Z\s\n]*$"
	if re.match(re_string, string):
		return string
	else:
		return "No match."

def extract_voltage(string: str) -> list[tuple[str]]:
	"""
	This function extracts voltages from a specific string per design.
	(see test_1) t is not designed to be a general voltage extracter.
	The function returns a list of tuples where each tuple contains the
	value @ index=0 and the unit at index=1 as this seemed to be the most
	useful format for working with the extracted info.

	:string: str: input string
	:return: list[tuple(str)]: list of tuples
	"""
	voltage_pattern = r'([0-9]*[\.\,]*[0-9]+\s*)(V|mVolt[s]*|mV)'
	return re.findall(voltage_pattern, string)




def test_regex_match():

	assert regex_match("* contains epoxy cement") == "* contains epoxy cement"
	assert regex_match("* contains only epoxy cement and water") == \
						"* contains only epoxy cement and water"
	assert regex_match("* contains oxygen cement") == "No match."
	assert regex_match("* contains, e.g., epoxy cement") == "No match."
	assert regex_match("*oxy cement") == "No match."
	assert regex_match("* contains\n epoxy ") == "* contains\n epoxy "
	assert regex_match("* contains oxygen oxygen oxygen only epoxy\ncement and water") == \
						"* contains oxygen oxygen oxygen only epoxy\ncement and water"
	assert regex_match("* contains hydroxyapatite cement") == "No match."
	assert regex_match("* contains 'epoxy' cement") == "No match."
	assert regex_match("*epoxy cement") == "*epoxy cement"
	assert regex_match(" * epoxy cement") == "No match."
	assert regex_match("** epoxy cement") == "No match."
	assert regex_match("* contains 'epoxy' cement") == "No match."
	assert regex_match("* contains epoxy cement.") == "No match."
	print("All tests passed")




def test_extract_voltages():

	test_1 = """\
		The power supply used in the experimental setup was rated at 110V\
		and 100W. Experiment 1 showed that average response of the neurons was 10\
		mVolts and the standard deviation 1 mVolt. On a subsequent experiment the\
		average response was still 10 mV but the standard deviation went down to\
		0.01 mVolts. The neurons were in V1 were assumed to have identical response\
		distributions.""".replace("\t", "")

	test_1_expected = [
		('110', 'V'),
		('10', 'mVolts'),
		('1 ', 'mVolt'),
		('10 ', 'mV'),
		('0.01 ', 'mVolts')]

	#print(extract_voltage(test_1))
	assert extract_voltage(test_1) == test_1_expected
	print("Test Passed")



def main():
	test_regex_match()
	test_extract_voltages()


if __name__ == '__main__':
	main()