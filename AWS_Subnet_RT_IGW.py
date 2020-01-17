import boto3

## Create Internet GW and Attach it to VPC

## First Copy the VPC ID from your AWS Console. We have fixed here for now "vpc-a50b2adf"

def igw_attach(vpcID,resource='NONE',region_name='NONE'):
    client = boto3.client(resource,region_name)
    resp = client.create_internet_gateway()
    igwID = resp['InternetGateway']['InternetGatewayId']
    client.attach_internet_gateway(InternetGatewayId=igwID,VpcId=vpcID)
    return igwID

## Function Exectuion
igwid = igw_attach(vpcID='vpc-a50b2adf',resource='ec2',region_name='us-east-1')


## Function for creating in 2 diffent AZ and creating 2 route table for each AZ and creating default route in 
## Each routing table towards Internet Gteway..

def createsubnet_rt(region_name,az_name,subnetcidr,vpcid,resource='ec2',igwID=igwid):
    client = boto3.client(resource,region_name)
    ##Creating IGW and Attaching it to VPC
    print (f"\nCreating Subnets in {az_name} and region is {region_name} ")
    print(f"\nCreating Routing Table for the AZ {az_name}, Our Region is {region_name}")
    rt_resp = client.create_route_table(VpcId=vpcid)
    rtID = rt_resp['RouteTable']['RouteTableId']
    print(f"\nRouting Table Created in the AZ {az_name}")
    print(f"\nAdding Default Route to Internet GW in the Routing Table.")
    client.create_route(DestinationCidrBlock='0.0.0.0/0',GatewayId=igwID,RouteTableId=rtID )
    for subnet in subnetcidr:
        resp = client.create_subnet(AvailabilityZone=az_name,CidrBlock=subnet,VpcId=vpcid)
        # print(resp)
        # subnetIDlist.append(resp['Subnet']['SubnetId'])
        subnetID = resp['Subnet']['SubnetId']
        client.associate_route_table(RouteTableId=rtID,SubnetId=subnetID)
        print (f"Subnet {subnet} created and associated in Routing Table {rtID}")
        #createRT(vpcID='vpc-a50b2adf',region_name=region_name ,subID=subnetID) 

##Primary AZ
createsubnet_rt(subnetcidr=['172.31.1.0/26','172.31.1.64/26','172.31.1.128/26','172.31.1.192/26'],
                vpcid='vpc-a50b2adf',region_name = 'us-east-1',az_name='us-east-1a',igwID=igwid)
## Secondary AZ
createsubnet_rt(subnetcidr=['172.31.2.0/26','172.31.2.64/26','172.31.2.128/26','172.31.2.192/26'],
                vpcid='vpc-a50b2adf',region_name = 'us-east-1',az_name='us-east-1b',igwID=igwid)