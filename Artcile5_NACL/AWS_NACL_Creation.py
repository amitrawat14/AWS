import boto3,csv
from botocore.exceptions import ClientError

## Global Parameter
region ='us-east-1'
CidrBlock = '172.172.0.0/16'
client = boto3.client('ec2',region_name=region)

## GET VPC ID. This is required during Network ACL Creation 
def getVpc(resource='ec2',region_name='NONE',cidr='None'):
    print(f"\nGetting VPC from Region {region_name}")
    client = boto3.client(resource,region_name)
    resp = client.describe_vpcs()
    for vpc in resp['Vpcs']:print(f"printing available CidrBlock in the region {region_name}, {vpc['CidrBlock']}")
    # print(resp['Vpcs'][0]['CidrBlock'])
    if cidr in resp['Vpcs'][0]['CidrBlock']:
        vpcID = resp['Vpcs'][0]['VpcId']
        return vpcID
    else:
        print(f"CIDR Details not found for {cidr}, Enter Correct Cidr Details from above")



## Generate NACL ID
def naclID(VpcId=None):
    nacl_resp = client.create_network_acl(VpcId=VpcId)
    nacl_id =  nacl_resp['NetworkAcl']['NetworkAclId']
    return nacl_id


## Create Network ACL Entry Function
def create_network_acl_entry(client='session',CidrBlock=None,Direction=None,
                            NetworkAclId=None,fromPort=None,toPort=None,
                            Protocol=None,Action='allow',Number=1):
 
    resp = client.create_network_acl_entry(CidrBlock=CidrBlock,
                                    Egress=Direction,NetworkAclId=NetworkAclId,
                                    PortRange={'From': fromPort,'To': toPort,},
                                    Protocol=Protocol,
                                    RuleAction=Action,
                                    RuleNumber=Number,)
    return resp




## Calling Function 
VpcId = getVpc(region_name=region,cidr=CidrBlock) 
nacl_id = naclID(VpcId)

with open('subnet_acl_entry.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader = list(csv_reader)
    for row in csv_reader[1:]:
        CidrBlock,Direction=row[0],row[1]
        fromPort,toPort,protocol = int(row[2]),int(row[3]),row[4]
        action,ruleNumber = row[5],int(row[6])
        if Direction == 'egress':
            Direction = True
        else:
            Direction=False
        try:
            create_network_acl_entry(client=client,CidrBlock=CidrBlock,Direction=Direction,
                                    NetworkAclId=nacl_id,fromPort=fromPort,toPort=toPort,
                                    Protocol=protocol,Action=action,Number=ruleNumber)
        except ClientError as e:
                    # print (f"\nError Occured while Creating ACL ")
                    print (f"\nError found  {e}")
                    print("\nPrinting Entered Rule Details, Please note True means 'Egress Flow', False mean 'Ingress Flow'.")
                    print(CidrBlock,Direction,fromPort,toPort,protocol,action,ruleNumber)


