#!/bin/bash

echo " "

# Check for presence of all required arguments
if [ -z $3 ]
 then
   echo  "==== >>>> Make sure to specify all required arguments in order <<<< ===="
   echo  "Argument 1 : username with Kerberos ticket"
   echo  "Argument 2 : target folder on hdfs"
   echo  "Argument 3 : local file name"
   exit
fi

# Check for Kerberos ticket
klist | grep $1
if [ $? -eq "1" ]
 then
   echo "==== >>>> Get a kerberos ticket first <<<< ===="
   exit
fi

# Arrange variables
hdfsfolder=$2
localfilename=$3

# Upload file(s)
if [[ -d $localfilename ]]; 
then
    echo "$localfilename is a directory, uploading recursively to $hdfsfolder"
    find $localfilename -name '*' -type f -exec curl -L --negotiate --insecure -u : -T {} "<server>/webhdfs/v1/$hdfsfolder/{}?op=CREATE&overwrite=true" \;
elif [[ -f $localfilename ]]; 
then
    echo "Uploading $localfilename to $hdfsfolder"
	curl -L --negotiate --insecure -u : -T $localfilename "<server>/webhdfs/v1/$hdfsfolder/$localfilename?op=CREATE&overwrite=true"
else
    echo "$localfilename is not valid"
    exit 1;
fi

# Verify if upload was successful
res=$?
if test "$res" != "0";
  then
  	echo "Curl failed with exit code: $res"
  else
    echo "Upload was successful"
fi
