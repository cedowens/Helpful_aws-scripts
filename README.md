# Check-S3-Access
python3 script using the boto3 library that uses threading to quickly recursively check which s3 buckets a set of aws keys with s3 bucket access can actually read from. This helps solve the problem of having a set of s3 keys that can list out bucket names (ex: aws s3 ls) but you have no idea which buckets the key can actually ls into (ex: aws s3 ls s3://[bucketname])

The script currently runs with threading set to 50, but you can adjust that as needed within the script. This allows the script to finish recursive s3 bucket list access checks on large s3 listings in short order.

## Steps
1. Ensure that boto3 is installed (pip3 install boto3)
2. Enter your access and secret key in the input.txt file where specified. Note: you can enter multiple sets of aws keys...just put each set on a separate line and the script will check each and create an output file for each
3. > python3 check-s3-access.py -f input.txt
4. Results will be written in the current directory with the access key in the filename
5. You can check the output file for successes by running:

> "grep "CAN read" [filename]"
