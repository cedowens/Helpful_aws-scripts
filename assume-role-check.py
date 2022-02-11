import json
import boto3
import optparse
from optparse import OptionParser
import os
import sys

if (len(sys.argv) != 5 and '-h' not in sys.argv):
    print("Usage: python3 %s -f [path_to_input_file]\n" % sys.argv[0])
    sys.exit(0)

parser = OptionParser()
parser.add_option("-f", "--file", help="Path to aws iam list-roles output file.")
parser.add_option("-a", "--arn", help="ARN value of your account from running sts get-caller-identity.")
(options,args) = parser.parse_args()

file = options.file
arn = options.arn


try:
	myarn = arn.split(':')
	myarn2 = myarn[0] + ':' + myarn[1] + ':' + myarn[2] + '::' + myarn[4] 

	if os.path.exists(file):
		f = open(file,"r")
		info = json.loads(f.read())

		for i in info['Roles']:
			z = i['RoleName']
			x = i['Arn']
			q = i['AssumeRolePolicyDocument']['Statement']
			q2 = str(q)

			if "Effect" in q2 and "Allow" in q2 and "Principal" in q2 and "AWS" in q2 and myarn2 in q2 and "'Condition': {}" in q2:
				print("")
				print("\033[92m\033[4m[+] Potential role for sts-assume role: (current identity: %s)\033[0m"%str(myarn))
				print("\033[33mRole Name:\033[0m %s"%str(z))
				print("\033[33mRole Arn:\033[0m %s"%str(x))
				print("\033[33mAssumeRolePolicyDocument Info:\033[0m %s"%str(q2))
				print("\033[33mTest With Command:\033[1maws sts assume-role --role-arn \"%s\" --role-session-name MySession\033[0m"%str(x))

				print("")
				print("")
	else:
		print("[-] File %s not found"%file)

except Exception as e:
	print(e)
