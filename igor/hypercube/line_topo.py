from mininet.topo import Topo
import sys
sys.path.append(".")
from router_node import Router

class LineTopo(Topo):

  def __init__(self):
    Topo.__init__(self)

    router = self.addNode("r0", cls=Router, ip="10.0.0.1/16")
    switch = self.addSwitch("s0")

    self.addLink(router, switch, intfName2="ro-eth1",
      params2={ "ip": "10.0.1.1/24" })

    s1 = self.addSwitch("s1")
    s2 = self.addSwitch("s2")

    self.addLink(s1, switch)
    self.addLink(s2, switch)

    h1 = self.addNode("h1", ip="10.0.1.100/16", defaultRoute="via 10.0.0.1")
    h2 = self.addNode("h2", ip="10.0.2.100/16", defaultRoute="via 10.0.0.1")

    for h, s in [ (h1, s1), (h2, s2)]:
      self.addLink(h, s)


topos = { "line": ( lambda: LineTopo() ) }
