
**Create openstack network**
-----------------------------

This would create basic network setup on your openstack installation.

----------

USAGE
-----

 1. You can use virtualenv to test this script. 
 2. You can execute it directly on openstack installation.

**Virtualenv setup:**

Needs the following package to be present on your environment

    gcc
    python-devel
    python-virtualenv
    python-pip

Create  virtualenv and activate

    virtualenv test
    cd test
    source bin/activate
 
 Download the remote git repositry
 

     cd openstack-create-network
     pip install -r requirements.txt

Update config.ini based on your openstack environment and it should be on its location

    [ACCOUNT_CREDENTIALS]
    OS_USERNAME=admin
    OS_PASSWORD=Password
    API_KEY=Password
    PROJECT_ID=admin
    OS_TENANT_NAME=admin
    OS_AUTH_URL=http://10.20.30.40:5000/v2.0/

Execute the command 

    python create-network.py


This would create the two networks and a router

    Public 
    Private
    Router
 


Customizing the new network setup
-------------
1. Network name
Update the config.ini and update the following tags

    [PRIVATE_NETWORK_DETAILS]
    NAME = My_Custom_network
    
    [PRIVATE_SUBNET_DETAILS]
    NAME = Private_Subnet

2. Network subnets

    CIDR = 10.0.0.0/24
    IP_VERSION = 4
    GATEWAY_IP = 10.0.0.1
    START = 10.0.0.2
    END = 10.0.0.25


Flat network configuration

![ScreenShot](https://github.com/mohi048/openstack-create-network/blob/master/flat-network.png)




Network setup for Kilo Release

![ScreenShot](https://github.com/mohi048/openstack-create-network/blob/master/kilo.png)



Network setup for liberty release

![ScreenShot](https://github.com/mohi048/openstack-create-network/blob/master/Liberty.png)
