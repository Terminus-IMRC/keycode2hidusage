#!/usr/bin/env python3

import sys
import argparse

def error_and_exit(reason):
	print("%s: error: %s"%(sys.argv[0], reason), file=sys.stderr)
	exit(1)

# Let's cooking!
def mine():
	
	parser = argparse.ArgumentParser(description="Converts numerical 2-column CSV to C table")
	parser.add_argument("-i", "--input", help="Input CSV file name", type=argparse.FileType("r"), default=sys.stdin)
	parser.add_argument("-n", "--name", help="Output table name", type=str, default=None)
	parser.add_argument("-o", "--output", help="Output table file name", type=argparse.FileType("w"), default=sys.stdout)
	parser.add_argument("-e", "--entry", help="Entries per a line in the output table", type=int, default=16)
	parser.add_argument("-w", "--width", help="Width of each number in the output table", type=int, default=3)
	args = parser.parse_args()

	if args.name == None:
		error_and_exit("output table name is not specified")

	table=[0 for x in range(0xff+1)]

	while True:
		try:
			s=args.input.readline()
		except EOFError:
			break
		if len(s)==0:
			break

		s=s.split(",")
		e1=int(s[0], 0)
		e2=int(s[1], 0)

		table[e1]=e2

	print("#include <stdint.h>", file=args.output)
	print("", file=args.output)
	print("uint8_t %s = {"%(args.name), file=args.output)
	for x in range(0, 0xff+1):
		if x%args.entry==0:
			start="\t"
		else:
			start=""
		if x%args.entry!=args.entry-1:
			end=","
		else:
			end="\n"
		print("%s%*d"%(start, args.width, table[x]), end=end, file=args.output)
	print("};", file=args.output)

if __name__ == "__main__":
	mine()
