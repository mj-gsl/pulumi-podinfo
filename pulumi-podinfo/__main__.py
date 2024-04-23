import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("vpc", cidr_block="10.0.0.0/16")

# Create an Internet Gateway for the VPC
ig = aws.ec2.InternetGateway("ig", vpc_id=vpc.id)

# Create a public subnet
subnet = aws.ec2.Subnet("subnet", vpc_id=vpc.id, cidr_block="10.0.1.0/24", map_public_ip_on_launch=True)

# Create a Route Table for the subnet
route_table = aws.ec2.RouteTable("route_table", vpc_id=vpc.id)

# Create a route that directs internet-bound traffic to the Internet Gateway
route = aws.ec2.Route("route",
    route_table_id=route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=ig.id)

# Associate the Route Table with the subnet
route_table_association = aws.ec2.RouteTableAssociation("route_table_association",
    route_table_id=route_table.id,
    subnet_id=subnet.id)

# Create a security group that allows HTTP and SSH access and outbound internet access
sg = aws.ec2.SecurityGroup("podinfo-sg",
    vpc_id=vpc.id,
    ingress=[
        {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]},
        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]}
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
    ])

# Create an EC2 instance using the Ubuntu AMI
instance = aws.ec2.Instance("instance",
    instance_type="t2.micro",
    vpc_security_group_ids=[sg.id],
    ami="ami-023adaba598e661ac",  # Updated AMI for Ubuntu
    subnet_id=subnet.id,
    associate_public_ip_address=True,
    key_name="Podinfo-key"
)

# Output the public IP of the instance
pulumi.export("public_ip", instance.public_ip)
