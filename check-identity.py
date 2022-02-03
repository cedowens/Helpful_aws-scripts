import boto3
import os
import sys
import optparse
from optparse import OptionParser
import threading
from queue import Queue


#########################
def checkidentity(worker):
    try:
        x = worker.split(':')
        accessky = x[0]
        scrtky = x[1]
        client = boto3.client('sts',aws_access_key_id=accessky,aws_secret_access_key=scrtky,region_name='us-west-1')
        response = client.get_caller_identity()
        print("-------------------------------------------------------")
        print("STS Check Results for key pair: \033[33m%s : %s\033[0m" % (accessky,scrtky))
        print("\033[92m===> Account: %s\033[0m"%str(response['Account']))
        print("\033[92m===> UserId: %s\033[0m"%str(response['UserId']))
        print("\033[92m===> Arn: %s\033[0m"%str(response['Arn']))
        print("-------------------------------------------------------")
    except:
        pass


    try:
        print("-------------------------------------------------------")
        print("Checking for s3 bucket access for key pair: \033[33m%s : %s\033[0m" % (accessky,scrtky))
        client2 = boto3.client('s3',aws_access_key_id=accessky,aws_secret_access_key=scrtky,region_name='us-west-1')
        r = client2.list_buckets()
        print("\033[92m===>[+] Key pair %s : %s has s3 bucket access\033[0m" % (accessky,scrtky))
        print("-------------------------------------------------------")
    except:
        pass

    try:
        print("-------------------------------------------------------")
        print("Attempting to list role info for key pair \033[33m%s : %s\033[0m" % (accessky,scrtky))
        client3 = boto3.client('iam',aws_access_key_id=accessky,aws_secret_access_key=scrtky,region_name='us-west-1')
        b = client3.list_roles()
        b2 = b['Roles']
        b3 = str(b2).split(',')
        print("\033[92m%s\033[0m"%b3)
        print("-------------------------------------------------------")

    except:
        pass

    try:
        print("-------------------------------------------------------")
        print("Attempting to list group info for key pair \033[33m%s : %s\033[0m" % (accessky,scrtky))
        client4 = boto3.client('iam',aws_access_key_id=accessky,aws_secret_access_key=scrtky,region_name='us-west-1')
        c = client4.list_groups()
        c2 = c['Groups']
        c3 = str(c2).split(',')
        print("\033[92m%s\033[0m"%c3)
        print("-------------------------------------------------------")
    except:
        pass

    try:
        print("-------------------------------------------------------")
        print("Attempting to list servicesspecificcredentials key pair \033[33m%s : %s\033[0m" % (accessky,scrtky))
        client5 = boto3.client('iam',aws_access_key_id=akey,aws_secret_access_key=skey,region_name='us-west-1')
        d= client5.list_service_specific_credentials()
        d2 = d['ServiceSpecificCredentials']
        d3 = str(d2).split(',')
        print("\033[92m%s\033[0m"%d3)
        print("-------------------------------------------------------")

    except:
        pass

    try:
        print("-------------------------------------------------------")
        print("Performing a secretsmanager check for key pair \033[33m%s : %s\033[0m" % (accessky,scrtky))
        client6 = boto3.client('secretsmanager',aws_access_key_id=akey,aws_secret_access_key=skey,region_name='us-west-1')
        pag = client6.get_paginator('list_secrets')
        iterator = pag.paginate()
        for page in iterator:
            secdict = page['SecretList']
            print("\033[92m%s\033[0m"%secdict)
        print("-------------------------------------------------------")

    except:
        pass

    try:
        print("-------------------------------------------------------")
        print("Performing a parameter store check for key pair \033[33m%s : %s\033[0m" % (accessky,scrtky))
        client7 = boto3.client('ssm',aws_access_key_id=akey,aws_secret_access_key=skey,region_name='us-west-1')
        pag2 = client7.get_paginator('describe_parameters')
        iterator2 = pag2.paginate()
        for pg in iterator2:
            mydict = pg['Parameters']
            print("\033[92m%s\033[0m"%mydict)
        print("-------------------------------------------------------")

    except:
        pass

    try:
        print("-------------------------------------------------------")
        print("Checking dynamodb list tables access for key pair \033[33m%s : %s\033[0m" % (accessky,scrtky))
        client8 = boto3.client('dynamodb',aws_access_key_id=akey,aws_secret_access_key=skey,region_name='us-west-1')
        e = client8.list_tables()
        print(response['TableNames']);
        print("-------------------------------------------------------")

    except:
        pass

###########################
def threader():
    while True:
        worker = q.get()
        checkidentity(worker)
        q.task_done()
###########################

if (len(sys.argv) != 3 and '-h' not in sys.argv):
    print("Usage: python3 %s -f [path_to_input_file]\n" % sys.argv[0])
    sys.exit(0)

parser = OptionParser()
parser.add_option("-f", "--file", help="Path to input file with AWS creds")
(options,args) = parser.parse_args()

file = options.file
keylist = []

if os.path.exists(file):
    with open(file,'r') as credfile:
        for line in credfile:
            parsed = line.strip().split(",")
            akey = parsed[0]
            skey = parsed[1]
            fullkey = "%s:%s"%(akey,skey)
            keylist.append(fullkey)

    q = Queue()

    for x in range(int(50)):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for pair in keylist:
        q.put(pair)

    q.join()
    print("*"*100)
    print("[+] DONE!")

else:
    print("[-] %s not found. Exiting..." % file)
