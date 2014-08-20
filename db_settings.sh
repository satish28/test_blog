#!/bin/bash

# Please keep this file outside the blog repository
# so that git does'nt track it. Keeping this file
# inside the repo is pointless.
#
# usage db_settings path_to_settings.py add|del
# use add to add db settings
# use del to remove db settings

# Database settings
# Specify your database details below.
NAME="mydb"
USER="satish"
PASSWORD="satish28"

if [ $# -ne 2 ]; then
	echo "Invalid number of arguments"
	echo "Usage: [FILE_PATH] [add|del]"
else
	FILE_PATH=$1
	if ls $FILE_PATH &> /dev/null; then
	    echo "file exists"
	else
	    echo "file does not exist"
		exit 1;
	fi
	if [ "$2" == "add" ]; then 
	    # Replacing db name
	    sed -i "" "s/'NAME'.*,/'NAME': '$NAME',/g" $FILE_PATH
	    # Replacing username
	    sed -i "" "s/'USER'.*,/'USER': '$USER',/g" $FILE_PATH
	    # Replacing password
	    sed -i "" "s/'PASSWORD'.*,/'PASSWORD': '$PASSWORD',/g" $FILE_PATH
	    echo "Database settings added !!"
	elif [ "$2" == "del" ]; then
	    # Deleting db name
	    sed -i "" "s/'NAME'.*,/'NAME': '',/g" $FILE_PATH
	    # Deleting username
	    sed -i "" "s/'USER'.*,/'USER': '',/g" $FILE_PATH
	    # Deleting password
	    sed -i "" "s/'PASSWORD'.*,/'PASSWORD': '',/g" $FILE_PATH
	    echo "Database settings removed !!"
	else
		echo "Argument not recognized.."
		echo "Usage: [FILE_PATH] [add|del]"
	fi
fi
