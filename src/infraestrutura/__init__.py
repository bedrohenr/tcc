from src.infraestrutura.mininet.topologia import ArvoreTopo
from src.infraestrutura.mininet import MininetExt
from src.infraestrutura.ryu import Ryu

from src.monitoramento import startMonitoramento

from mininet.log import setLogLevel

class Infraestrutura():
    def __init__(self, bw, topo):
        self.bandwidth=bw
        self.topo = topo

    def up(self):
        ryu = Ryu()
        mininet = MininetExt(self.bandwidth, self.topo)

        mininet.clean()

        try:

            ryu.start()
            mininet.start()

        finally:
            ryu.end()