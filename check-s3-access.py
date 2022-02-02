import boto3
import os
import sys
import optparse
from optparse import OptionParser
import threading
from queue import Queue

#########################
def listbuckets(bucket):
    #s3 = boto3.resource('s3')
    try:
        objects = client.list_objects(Bucket=bucket, Prefix='',Delimiter='/')
        if len(objects) == 9:
            print("\033[92m[+] This key CAN read from s3://%s\033[0m\n" %bucket)
            output.write("[+] This key CAN read from s3://%s\n"%bucket)
    except:
        print("\033[91m[-] Unable to view bucket contents for %s\033[0m\n" %bucket)
        output.write("[-] This key is unable to view bucket contents for %s\n"%bucket)
###########################
def threader():
    while True:
        worker = q.get()
        listbuckets(worker)
        q.task_done()

if (len(sys.argv) != 3 and '-h' not in sys.argv):
    print("Usage: python3 %s -f [path_to_input_file]\n" % sys.argv[0])
    sys.exit(0)

parser = OptionParser()
parser.add_option("-f", "--file", help="Path to input file with AWS creds")
(options,args) = parser.parse_args()

file = options.file

if os.path.exists(file):
    with open(file,'r') as credfile:
        for line in credfile:
            parsed = line.strip().split(",")
            akey = parsed[0]
            skey = parsed[1]
            output = open("%s-s3Check.txt" % akey,"w")
            output.write("Recursively checking s3 bucket read access for %s : %s\n" % (akey,skey))
            output.write("-----------------------------------------------------------------------------------\n")

    session = boto3.Session(
    aws_access_key_id=akey,
    aws_secret_access_key=skey)

    client = boto3.client('s3',aws_access_key_id=akey,
    aws_secret_access_key=skey)

    s3 = session.resource('s3')

    q = Queue()

    for x in range(int(50)):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in s3.buckets.all():
        q.put(worker.name)

    q.join()
    print("*"*100)
    print("[+] DONE!")
    output.close()



else:
    print("[-] %s not found. Exiting..." % file)
