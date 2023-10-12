from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController, Host
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import requests
import json


class NetworkTopo( Topo ):


    def build( self ):

        # Add switches
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')
        s4 = self.addSwitch('s4', protocols='OpenFlow13')

        # Add hosts
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1/24')
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2/24')
        h3 = self.addHost('h3', cls=Host, ip='10.0.0.3/24')
        h4 = self.addHost('h4', cls=Host, ip='10.0.0.4/24')
        h5 = self.addHost('h5', cls=Host, ip='10.0.0.5/24')
        h6 = self.addHost('h6', cls=Host, ip='10.0.0.6/24')
        h7 = self.addHost('h7', cls=Host, ip='10.0.0.7/24')
        h8 = self.addHost('h8', cls=Host, ip='10.0.0.8/24')
        h9 = self.addHost('h9', cls=Host, ip='10.0.0.9/24')

        # Add links
        for h, s in [ (h1, s2), (h2, s2), (h3, s2), (h4, s3), (h5, s3), (h6, s3), (h7, s4), (h8, s4), (h9, s4) ]:
            self.addLink( h, s )
        
        # Set BW
        self.addLink( s1, s2, bw=12, addr1='00:00:00:00:01:00', addr2='00:00:00:00:02:00') # high bw = 2-4Mbps per user (video + voice)
        self.addLink( s1, s3, bw=0.3, addr1='00:00:00:00:03:00', addr2='00:00:00:00:04:00') # poor bw = 100kbps (min) per user (voice)
        self.addLink( s1, s4, bw=3, addr1='00:00:00:00:05:00', addr2='00:00:00:00:06:00' ) # low bw = 1Mbps per user (datanetwork)

        

def run():
    topo = NetworkTopo()

    net = Mininet(topo=topo, controller=RemoteController, switch=OVSKernelSwitch)

    net.start()

    # Device ID
    switch1 = 'of:0000000000000001'
    switch2 = 'of:0000000000000002'
    switch3 = 'of:0000000000000003'
    switch4 = 'of:0000000000000004'

    session = requests.Session()
    session.auth = ('onos', 'rocks')

    flow_rule = '''{
                    "flows": [
                        {
                        "priority": 40000,
                        "timeout": 0,
                        "isPermanent": true,
                        "deviceId": "of:0000000000000002",
                        "treatment": {
                            "instructions": [
                            {
                                "type": "NOACTION"
                            }
                            ]
                        },
                        "selector": {
                            "criteria": [
                            {
                                "type": "ETH_SRC",
                                "mac": "00:00:00:00:02:00"
                            },
                            {
                                "type": "ETH_DST",
                                "mac": "00:00:00:00:03:00"
                            }
                            ]
                        }
                        },
                        {
                        "priority": 40000,
                        "timeout": 0,
                        "isPermanent": true,
                        "deviceId": "of:0000000000000002",
                        "treatment": {
                            "instructions": [
                            {
                                "type": "NOACTION"  
                            }
                            ]
                        },
                        "selector": {
                            "criteria": [
                            {
                                "type": "ETH_SRC",
                                "mac": "00:00:00:00:02:00"
                            },
                            {
                                "type": "ETH_DST",
                                "mac": "00:00:00:00:04:00"
                            }
                            ]
                        }
                        }
                    ]
                    }'''
                    
    
    response = requests.post('http://127.0.0.1:8181/onos/v1/flows', json=flow_rule)

    url = 'http://127.0.0.1:8181/onos/v1/flows'

    response = session.get('http://127.0.0.1:8181/onos/v1/flows')

    if response.status_code == 200:
        print('dat big succ')

    else:
        print('Request failed with status code:', response.status_code)
    
    
    # Start the Mininet CLI for further interaction
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
