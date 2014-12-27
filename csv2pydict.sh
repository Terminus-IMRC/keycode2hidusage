#!/usr/bin/env bash

if test -z "$1"; then
	echo "$0: error: specicy csv file" >&2
	exit 1
fi

INFILE="$1"
echo "Input file name: $INFILE" >&2
if ! test -f "$INFILE"; then
	echo "$0: error: $INFILE: no such file" >&2
	exit 1
fi

echo "$1" | grep -q '\.csv$' && f=$(basename "$1" .csv) || f=$(basename "$1")
DICTNAME="${f}_dict"

echo "Output dictionary name: $DICTNAME" >&2
if echo "$DICTNAME" | grep -q '[^a-zA-Z_0-9]'; then
	echo "$0: error: $DICTNAME contains non-alphabetical nor non-numerical character" >&2
	exit 1
fi
if echo "$DICTNAME" | grep -q '^[0-9]'; then
	echo "$0: error: $DICTNAME starts with non-alphabetical character" >&2
	exit 1
fi

echo "$DICTNAME = {"
grep -v '^#' <"$INFILE" | sed 's/\(..*\),\(..*\)/	\1:\2,/'
echo "}"
