import boto.ec2
import boto.vpc
import os
import sys
import urllib2

response=urllib2.urlopen('http://www.yahoo.com')

#ACCESS_KEY = raw_input("Enter AWS Access Key: ")
#SECRET_KEY = raw_input("Enter AWS Secret Key: ")

#if not ACCESS_KEY:
#  sys.exit("ERROR: Key error. Exiting")

VPC=[]

#regions = ['us-east-1','us-west-1','ap-northeast-1','ap-southeast-2','sa-east-1','ap-southeast-1','ap-northeast-2','us-west-2','ap-south-1','eu-central-1','eu-west-1']
regions = ['us-west-1']

for region in regions:
  print("Region is: "+region)

  vpc = boto.vpc.connect_to_region(region_name=region,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
  print("Total VPCs in this region", len(vpc.get_all_vpcs()))
  for vpc in vpc.get_all_vpcs():
    print("Doing VPC", vpc.id, vpc.tags)
    if not (vpc.tags)['Name']:
      VPC.append(vpc.id)


for vpcs in VPC:
  print(vpcs)
  
