# Helpful aws boto3 scripts
python3 scripts to help with aws triage needs 

Two of the scripts (check-identity.py and check-s3-access.py) currently run with threading set to 50, but you can adjust that as needed within the script. This allows the script to finish recursive s3 bucket list access checks on large s3 listings in short order.

3 scripts currently included:
1. check-identity.py: This is a threaded python3 script that can take one or many aws key pairs and very quickly check if those keys are active and quickly performs the following checks:
- checks s3 bucket access
- attempts to list role info
- attempts to list group info
- checks for servicesspecificcredentials
- checks secretsmanager info
- checks parameterstore info
- checks for dynamodb list_tables access

2. check-s3-access.py: This is a threaded python3 script that can take sets of keys and quickly check to identify which buckets that key can actually view into (i.e., a key pair may be able to list a bucket name but may not be able to view inside of that bucket, so this script helps with identifying which buckets a set of keys can actually see into)

3. assume-role-check.py: This script is intended to be run after discovering that a set of aws credentials have iam list-roles privileges. Steps: 1. run aws iam list-roles > output.txt, 2. run aws sts get-caller-identity on the creds and copy the ARN value, 3. python3 assume-role-check.py -a [ARN_value] -f [iam-list-roles-output-file]. The script will then check which roles are potential candidates for sts assume-role operations.


## Steps
**For check-identity.py and check-s3access.py:**

1. Ensure that boto3 is installed (pip3 install boto3)
2. Create a file (example: input.txt) and add one set of credentials per row in this format: accesskey,secretkey
3. in check-identity.py, the region by default is set to **us-west-1**. You can edit that value in the script as needed.
4. Run `python3 check-identity.py -f input.txt`. This script will take all key pairs inclued in input.txt and perform the checks listed above.
5. Based on which keys from #2 have s3 bucket access, add just those keys into a new input file (ex: input2.txt).
6. Run `python3 check-s3-access.py -f input2.txt`. This script will then recursively check across all buckets to see which buckets a key pair can access see into. Results will be written to an outfile in the current directory with the access key in the filename. You can check the output for successes by running `grep "CAN read" [outputfile]`

**For assume-role-check.py:**
1. run `aws iam list-roles > output.txt`
2. run `aws sts get-caller-identity` on the creds and copy the ARN value
3. run `python3 assume-role-check.py -a [ARN_value] -f [iam-list-roles-output-file-from-above]`. The script will then check which roles are potential candidates for sts assume-role operations.
