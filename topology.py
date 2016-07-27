from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch
from mininet.net import Mininet

setLogLevel('info')
controller = RemoteController("c0", ip="127.0.0.1", port=6633)

class HypercubeTopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        A = "00:00:00:00:00:00"
        B = "00:00:00:02:00:00"
        C = "00:00:00:06:00:00"
        D = "00:00:00:07:00:00"
        E = "00:00:00:05:00:00"
        F = "00:00:00:01:00:00"
        G = "00:00:00:03:00:00"
        H = "00:00:00:04:00:00"

        sA = self.addSwitch("s1")
        sB = self.addSwitch("s2")
        sC = self.addSwitch("s3")
        sD = self.addSwitch("s4")
        sE = self.addSwitch("s5")
        sF = self.addSwitch("s6")
        sG = self.addSwitch("s7")
        sH = self.addSwitch("s8")

        self.addLink(sA, sB)
        self.addLink(sA, sF)
        self.addLink(sA, sH)
        self.addLink(sF, sE)
        self.addLink(sF, sG)
        self.addLink(sG, sB)
        self.addLink(sG, sD)
        self.addLink(sD, sE)
        self.addLink(sD, sC)
        self.addLink(sC, sH)
        self.addLink(sC, sB)
        self.addLink(sE, sH)

        # hosts for switches
        hA = self.addHost("h1")
        hB = self.addHost("h2")
        hC = self.addHost("h3")
        hD = self.addHost("h4")
        hE = self.addHost("h5")
        hF = self.addHost("h6")
        hG = self.addHost("h7")
        hH = self.addHost("h8")

        self.addLink(sA, hA)
        self.addLink(sB, hB)
        self.addLink(sC, hC)
        self.addLink(sD, hD)
        self.addLink(sE, hE)
        self.addLink(sF, hF)
        self.addLink(sG, hG)
        self.addLink(sH, hH)

topo = HypercubeTopo()
net = Mininet(topo = topo, switch=OVSSwitch, build = False)
net.addController(controller)
net.build()
net.start()
CLI(net)
net.stop()

#topos = { 'hypercube': ( lambda: HypercubeTopo() ) }
