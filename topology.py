from mininet.topo import Topo

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

        sA = self.addNode("sA", mac=A)
        sB = self.addNode("sB", mac=B)
        sC = self.addNode("sC", mac=C)
        sD = self.addNode("sD", mac=D)
        sE = self.addNode("sE", mac=E)
        sF = self.addNode("sF", mac=F)
        sG = self.addNode("sG", mac=G)
        sH = self.addNode("sH", mac=H)

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
        
topos = { 'hypercube': ( lambda: HypercubeTopo() ) }
