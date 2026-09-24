from mininet.topo import Topo

class ArvoreTopo(Topo):
    """
    Topologia em Arvore com Depth=2 e Fanout=2
    
                      [ s1 ]             <-- Nível 1: Switch Raiz
                    /        \
                [ s2 ]        [ s3 ]      <-- Nível 2: Switches Folha
               /      \      /      \
            (h1)      (h2) (h3)     (h4)  <-- Hosts
    """

    def build(self):
        # Switches
        s1 = self.addSwitch('s1', dpid="s1", protocols='OpenFlow13')
        s2 = self.addSwitch('s2', dpid="s2", protocols='OpenFlow13')
        s3 = self.addSwitch('s3', dpid="s3",protocols='OpenFlow13')

        # Hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')

        # Enlaces entre switches
        self.addLink(s1, s2)
        self.addLink(s1, s3)

        # Enlaces entre hosts e switches folha
        self.addLink(s2, h1)
        self.addLink(s2, h2)
        self.addLink(s3, h3)
        self.addLink(s3, h4)