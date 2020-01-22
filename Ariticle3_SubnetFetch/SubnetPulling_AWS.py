import boto3


def region_finder (resource='ec2',region_name ='None'):
    region_list = []
    client = boto3.client(resource,region_name)
    ec2_reg = client.describe_regions()
    for region in ec2_reg['Regions']:
        print (region['RegionName'])
        region_list.append(region['RegionName'])
        # print (ec2_reg['Regions'][i]['RegionName'])
    return region_list

def subnet_finder (resource='ec2',region_name ='None'):
    client = boto3.client(resource,region_name)
    sub_resp = client.describe_subnets()['Subnets']
    print (f"\n *******Printing Subnets in region {region_name}*******")
    for i in sub_resp: 
        print(f"CIDR Block == {i['CidrBlock']} ---  AvailabilityZone == {i['AvailabilityZone']}")
        print ("*" * 100)


region_list = region_finder(region_name='us-east-1')
for region in region_list:
    subnet_finder(region_name = region)

