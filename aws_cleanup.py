import boto.ec2
import boto.vpc
import os
import sys

REGIONS = ['us-west-1']
#REGIONS = ['us-east-1','us-west-1','ap-northeast-1','ap-southeast-2','sa-east-1','ap-southeast-1','ap-northeast-2','us-west-2','ap-south-1','eu-central-1','eu-west-1']

VPC=[]
SUBNETS=[]
ROUTE_TABLES=[]
IG=[]
ACL=[]


def print_banner(message):
  print("")
  divider="*"*len(message)
  print(divider)
  print(message)
  print(divider)

def build_vpc_list(vpc_connection):
  for vpc in vpc_connection.get_all_vpcs():
    if not (vpc.tags)['Name']:
      VPC.append(vpc.id)

def build_subnet_list(vpc_connection):
  subnets=vpc_connection.get_all_subnets(filters=[('vpcId',VPC)])
  for subnet in subnets:
    SUBNETS.append(subnet.id)

def build_routetable_list(vpc_connection):
  route_tables=vpc_connection.get_all_route_tables(filters=[('vpc-id',VPC)])
  for route_table in route_tables:
    print(route_table.routes)
    ROUTE_TABLES.append(route_table.id)

def build_ig_list(vpc_connection):
  igs=vpc_connection.get_all_internet_gateways(filters=[('attachment.vpc-id',VPC)])
  for ig in igs:
    IG.append(ig.id)

def build_acl_list(vpc_connection):
  acls=vpc_connection.get_all_network_acls(filters=[('association.subnet-id', SUBNETS)])
  for acl in acls:
    ACL.append(acl.id)

def print_assets_to_delete():
  print("")
  print("The Following Assets Will be Deleted")
  print("")
  print_banner("VPCs")
  for vpc in VPC: print(vpc)
  print_banner("Subnets")
  for subnet in SUBNETS: print(subnet)
  print_banner("Route Tables")
  for rt in ROUTE_TABLES:
    print(rt.destination_cidr_block)

  print_banner("Internet Gateways")
  for ig in IG: print(ig)
  print_banner("Network ACLs")
  for acl in ACL: print(acl)


def cleanup(vpc_connection):
  print_assets_to_delete()
  print("")
  answer=raw_input("Are you sure you want to delete these assets (y/n)?: ")
  if answer == 'y' or answer == "Y":
    for subnet in SUBNETS:
      vpc_connection.delete_subnet(subnet)
    for rt in ROUTE_TABLES:
      vpc_connection.delete_route_table(rt)
    for vpc in VPC:
      vpc_connection.delete_vpc(vpc)
  else:
    print ("Bye !")


if __name__ == "__main__":

  ACCESS_KEY=raw_input("Enter AWS ACCESS KEY: ")
  SECRET_KEY=raw_input("Enter AWS SECRET kEY: ")

  if not ACCESS_KEY or not SECRET_KEY:
    sys.exit("ERROR: Key error. Exiting")

  for region in REGIONS:
    print("Region is: "+region)

    vpc_connection = boto.vpc.connect_to_region(region_name=region,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

    build_vpc_list(vpc_connection)
    build_subnet_list(vpc_connection)
    build_routetable_list(vpc_connection)
    build_ig_list(vpc_connection)
    build_acl_list(vpc_connection)

    cleanup(vpc_connection)



