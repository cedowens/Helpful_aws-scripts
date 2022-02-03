# Helpful aws boto3 scripts
python3 scripts that include threading to quickly perform checks on large sets (either checks against many aws key pairs or checks against a long list of s3 buckets to see which s3 buckets a set of aws keys with s3 bucket access can actually read from) 

The scripts currently run with threading set to 50, but you can adjust that as needed within the script. This allows the script to finish recursive s3 bucket list access checks on large s3 listings in short order.

2 scripts currently included:
1. check-s3-access.py: This is a threaded python3 script that can take a set of keys and quickly check against a long list of buckets to quickly identify which buckets that key can actually view into (i.e., a key pair may be able to list a bucket name but may not be able to view inside of that bucket, so this script helps with identifying which buckets a set of keys can actually see into)
2. check-identity.py: This is a threaded python3 script that can take one or many aws key pairs and very quickly check if those keys are active and if those keys have any s3 bucket accesses.

## Steps
1. Ensure that boto3 is installed (pip3 install boto3)
2. Enter your access and secret keys in the input.txt file where specified. Note: you can enter multiple sets of aws keys...just put each set on a separate line and the script will check each and create an output file for each
3. > python3 check-s3-access.py -f input.txt OR python3 check-identity.py
4. For check-s3-access.py: Results will be written in the current directory with the access key in the filename. Youc an check the output file for successes by running "grep "CAN read" [outfputfilename]".
5. For check-identity.py: Results will be retunred to stdout
