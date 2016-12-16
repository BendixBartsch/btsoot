#!/usr/bin/env python3

import sys
import os
try:
	from compare import compare
except ImportError:
	print("Failed to import compare library.")
	exit()

usage = "USAGE: btsoot add/rm/scan "

class color:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def scandirectory(walk_dir, scanfile, silent = False):
	try:
		print("Initializing scan...")
		with open(scanfile, "w") as f:
			f.write("path,checksum\n")
			for root, subdirs, files in os.walk(walk_dir):
				f.write(root + "\n")
				for filename in files:
					file_path = os.path.join(root, filename)
					checksum = compare.sha1sum(file_path)
					if silent == True:
						print(file_path, checksum, end="\n")
					else:
						pass
					print(checksum)
					f.write(file_path + "," + checksum + "\n")
		print("...done.")
	except FileNotFoundError:
		print("There were an reading error... Probably os protected.")


def main():
	try:
		if sys.argv[1] == "add":
			try:
				name = sys.argv[2]
				path = sys.argv[3]
				server = sys.argv[4]
			except IndexError:
				print("Usage: " + sys.argv[0] + " add name path server")
				print("Type local if you want to use local filesystem.")
				exit()
			with open("btsoot.conf", "a") as f:
				f.write("name=" + name + '\n')
				f.write("path=" + path + '\n')
				f.write("server=" + server + '\n')
		elif sys.argv[1] == "rm":
			try:
				name = sys.argv[2]
			except IndexError:
				print("Usage: " + sys.argv[0] + "rm name")
				exit()
			try:
				f = open("btsoot.conf", "r")
				row = 0
				beginning_row = -10
				indentifier = "name=" + name + '\n'
				lines = f.readlines()
				f.close()
				f = open("btsoot.conf", "w")
				for line in lines:
					row = row + 1
					if line == indentifier:
						beginning_row = row
					elif row == beginning_row + 1 or row == beginning_row + 2:
						pass
					else:
						f.write(line)
				f.close()
			except FileNotFoundError:
				print("Configfile not found. Create one with 'add'.")
		elif sys.argv[1] == "scan":
			print("Execute scan...")
			#NAME NEEDS TO BE RESOLVED TO CORRECT DIRECTORY!
			#USE PPARTIAL FUNCTION FROM 'rm'
			scandirectory(sys.argv[2], "testfile", True)


	except IndexError:
		print(usage)
		exit()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Stopping program.")
		sys.exit()
