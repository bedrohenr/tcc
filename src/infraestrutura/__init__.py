from src.infraestrutura.mininet.topologia import ArvoreTopo
from src.infraestrutura.mininet import MininetExt
from src.infraestrutura.ryu import Ryu

class Infraestrutura():
    def __init__(self, bw, topo, test_mode):
        self.bandwidth=bw
        self.topo = topo
        self.test_mode = test_mode

    def up(self):
        ryu = Ryu()
        mininet = MininetExt(self.bandwidth, self.topo, self.test_mode)

        mininet.clean()

        try:
            ryu.start()
            mininet.start()

        finally:
            ryu.end()