from neutronclient.v2_0 import client
import configparser
import requests
import time
verbose = 0

def update(val,param):
	d1 = {i:j for i,j in val.items() if j }
	d2 = {x.replace(param+'_',param+':'): d1[x] for x in d1.keys()}
	return d2

def update_subnet(subnet,net_id):
    dd = {}
    dl = []
    dd['start'] = subnet.pop('start')
    dd['end'] = subnet.pop('end')
    subnet['allocation_pools'] = [dd]
    subnet['network_id'] = net_id
    dl.append(subnet['dns_nameservers'])
    subnet['dns_nameservers'] = dl
    return subnet

def create_network(network_name,subnet_name):
    if 'network_id' not in network_name.keys():
        priv = update(network_name,'provider')
        network_name = update(priv,'router')
        network_name['admin_state_up'] = 'True'
        body_sample = {'network': network_name}
        if verbose: print "creating network %s with paramters %s \n" %(network_name['name'],body_sample)
        netw = neutron.create_network(body=body_sample)
        net_dict = netw['network']
        network_id = net_dict['id']
        network_name = net_dict['name']
        print ('Network id %s created having name %s\n' %(network_id,network_name))
        priv_subnet = update_subnet(subnet_name,network_id)
        body_create_subnet = {'subnets': [priv_subnet]}
        if verbose: print "creating subnet %s with paramters %s \n " %(subnet_name['name'],body_sample)
        network_subnet = neutron.create_subnet(body=body_create_subnet)
        print ('subnet id %s created having name %s\n' %(network_subnet['subnets'][0]['id'], network_subnet['subnets'][0]['name']))
    else:
        network_id = network_name['network_id']
        print "Skipping network creation as NETWORK_ID specificed on config.ini, creating subnet only\n"
        #print network_name['network_id']
        priv_subnet = update_subnet(subnet_name,network_id)
        body_create_subnet = {'subnets': [priv_subnet]}
        if verbose: print "creating subnet %s with paramters %s \n " %(subnet_name['name'],body_sample)
        network_subnet = neutron.create_subnet(body=body_create_subnet)
        print ('subnet id %s created having name %s\n' %(network_subnet['subnets'][0]['id'], network_subnet['subnets'][0]['name']))
    return (network_id,network_subnet['subnets'][0]['id'])

def create_router(router_name,private_network,public_network):
    (priv_net_id,priv_subnet_id) = private_network
    (pub_net_id,pub_subnet_id) = public_network
    request = {'router': {
                            'name': router_name,
                            'admin_state_up': True,
                            'external_gateway_info': 
                            {
                            'network_id':pub_net_id,
                            'enable_snat':'True'
                            }
                            }}
    if verbose: print "creating router %s with paramters %s \n" %(router_name,request)
    router = neutron.create_router(request)
    router_id = router['router']['id']
    neutron.add_interface_router(router_id, { 'subnet_id' : priv_subnet_id } )
    print("Router id %s created with name %s \n" %(router_id,router_name))
    return router_id

config = configparser.ConfigParser()
if config.read('./config.ini') != []:
    pass
else:
    raise IOError("Could not read config.ini file on base directory")

credentials = dict(config['ACCOUNT_CREDENTIALS'])
priv_net = dict(config['PRIVATE_NETWORK_DETAILS'])
priv_subnet = dict(config['PRIVATE_SUBNET_DETAILS'])
pub_net = dict(config['PUBLIC_NETWORK_DETAILS'])
pub_subnet = dict(config['PUBLIC_SUBNET_DETAILS'])
router = dict(config['ROUTER'])

try:
    print "\n Attempting to connect on %s" %credentials['auth_url']
    response = requests.get(url=credentials['auth_url'],timeout=(10.0,1))
except requests.exceptions.ReadTimeout as e:
    print e.message
finally:
    print "Connected to the host"

neutron = client.Client(**credentials)
private_network  = create_network(priv_net,priv_subnet)
public_network = create_network(pub_net,pub_subnet)
router_created = create_router(router['name'],private_network,public_network)
