# run using sudo mn --custom a2.py --topo=a2_topo --link tc --controller remote,ip=172.17.0.5
#
#
from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from mininet.topo import Topo

class A2Topology( Topo ):

    def build( self ):
        # Add hosts and switches
        usr = self.addHost( 'usr', ip= '10.0.0.69')
        h1 = self.addHost( 'h1',ip='10.0.0.1' )
        h2 = self.addHost( 'h2',ip='10.0.0.2' )
        h3 = self.addHost( 'h3',ip='10.0.0.3' )
        h4 = self.addHost( 'h4',ip='10.0.0.4' )
        h5 = self.addHost( 'h5',ip='10.0.0.5' )
        h6 = self.addHost( 'h6',ip='10.0.0.6' )
        h7 = self.addHost( 'h7',ip='10.0.0.7' )
        h8 = self.addHost( 'h8',ip='10.0.0.8' )
        h9 = self.addHost( 'h9',ip='10.0.0.9' )
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' ) #high bw
        s3 = self.addSwitch( 's3' ) #poor bw
        s4 = self.addSwitch( 's4' ) #low bw

        # Add links
        self.addLink( usr, s1)
        self.addLink( h1, s2 )
        self.addLink( h2, s2 )
        self.addLink( h3, s2 )
        self.addLink( h4, s3 )
        self.addLink( h5, s3 )
        self.addLink( h6, s3 )
        self.addLink( h7, s4 )
        self.addLink( h8, s4 )
        self.addLink( h9, s4 )
        
        
        
        # Set BW
        self.addLink( s1, s2, bw=12 ) # high bw = 2-4Mbps per user (video + voice)
        self.addLink( s1, s3, bw=0.3,delay='5ms', jitter='5ms', loss=2) # poor bw = 100kbps (min) per user (voice)
        self.addLink( s1, s4, bw=3 ,delay='0.5ms', jitter='2ms', loss=0.5) # low bw = 1Mbps per user (datanetwork)


topos = {
    "a2_topo": A2Topology,
}

if __name__ == '__main__':
    setLogLevel( 'info' )
    Topo = A2Topology()
