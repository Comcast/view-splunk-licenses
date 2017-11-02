#!/usr/bin/env python
#
# This script runs the command to get all Splunk Licenses, parses the output
# and prints it up in human-readable format.
#

import argparse
import datetime
#import dateutil.parser
import json
import logging
logger = logging
import socket, errno
import subprocess
import os
import sys
import time

#parser = argparse.ArgumentParser(description = "Check the overall health of Zookeeper Clusters")
#parser.add_argument("--debug", help = "Enable debug messages", action = "store_true" )

#args = parser.parse_args()

#
# ANSI color codes.
#
color_green = '\033[92m'
color_red = '\033[91m'
color_end = '\033[0m'


#
# Set up logging
#
date_format = "%Y-%m-%d %H:%M:%S"
format = "%(asctime)s.%(msecs)03d: %(levelname)s: %(message)s"

level = logging.INFO

logging.basicConfig(level = level, format = format, datefmt = date_format)


#
# This function runs a command and returns the output as a string.
# If there is anything on standard error or a non-zero return code, an exception is thrown.
#
def runCmd(cmd):

	logging.info("Executing command '%s'..." % cmd)
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	retval = process.wait()
	(stdout, stderr) = process.communicate()

	if retval or stderr:
		error = "Retval: %d, stderr: %s" % (retval, stderr)
		raise Exception(error)

	return(stdout)


#
# Check to see if this line is a new license. New licneses are a 64-byte Sha-256
# on a line by themselves.
#
def isNewLicense(text):

	if ":" in text:
		return False

	if len(text) == 64:
		return True

	return False


#
# Turn the number of bytes into a human-readable string
#
def getQuotaHuman(quota):

	retval = quota

	mb = 1024 * 1024
	gb = mb * 1024

	if (quota > gb):
		retval = ("%.2f GB" % (quota / gb) )

	elif (quota > mb):
		retval = ("%.2f MB" % (quota / mb) )

	else:
		retval = ("%s b" % (quota))

	return(retval)


#
# Parse the text from Splunk's license command.
#
# Array of dictionaries is returned with info on each license.
#
def parseLicenseText(text):

	retval = []
	row = {}

	for line in text.split("\n"):

		fields = line.split("\t")
		index = len(fields) - 1
		field = fields[index]

		if isNewLicense(field):
			#logger.info("Found new license: %s", field)
			if (row):
				retval.append(row)
			row = {}

		values = field.split(":")
		if values[0] == "quota":
			row["quota"] = int(values[1])
			row["quota_human"] = getQuotaHuman(int(values[1]))

		elif values[0] == "creation_time":
			row["creation_time"] = values[1]
			row["creation_time_human"] = time.strftime("%Y-%m-%d %H:%M:%S",
				time.localtime(int(values[1])))

		elif values[0] == "expiration_time":
			row["expiration_time"] = values[1]
			row["expiration_time_human"] = time.strftime("%Y-%m-%d %H:%M:%S",
				time.localtime(int(values[1])))

		elif values[0] == "label":
			row["label"] = values[1]

		elif values[0] == "license_hash":
			row["license_hash"] = values[1]

		elif values[0] == "status":
			row["status"] = values[1]

	return(retval)


#
# Print up our license data
#
def printLicenses(data):

	total_bytes = 0

	print("%8s %12s %20s %20s  %s" % ("Status", "Quota", "Creation Date", "Expiration Date", "Label"))
	print("%8s %12s %20s %20s  %s" % ("========", "==========", "===================", "===================", "============================"))


	for row in data:
		total_bytes += row["quota"]

		color = color_green
		if row["status"] != "VALID":
			color = color_red

		print("%s%8s %12s %20s %20s  %s%s" % (color, row["status"], row["quota_human"], row["creation_time_human"], row["expiration_time_human"], row["label"], color_end))

	print("")
	print("Total Quota bytes: %s%s%s" % (color_green, getQuotaHuman(total_bytes), color_end))
	print("")


def main():

	cmd = "/var/splunk/bin/splunk list licenses"
	logger.info("Running command %s..." % cmd)
	license_text = runCmd(cmd)
	#print license_text

	license_data = parseLicenseText(license_text)
	#print json.dumps(license_data, indent=4, sort_keys=True)
	
	printLicenses(license_data)


main()


