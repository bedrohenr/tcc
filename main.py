from src.infraestrutura.mininet.topologia import ArvoreTopo
from src.infraestrutura.mininet import MininetExt
from src.infraestrutura.ryu import Ryu

from src.monitoramento import startMonitoramento

from mininet.log import setLogLevel

def startInfraestrutura(topo):
    ryu = Ryu()
    mininet = MininetExt(100, topo)

    mininet.clean()

    try:

        ryu.start()
        mininet.start()

    finally:
        ryu.end()

if __name__ == '__main__':
    setLogLevel('info')

    topo = ArvoreTopo()

    startInfraestrutura(topo)
    # startMonitoramento()
