from src.infraestrutura.mininet.topologia import ArvoreTopo
from src.infraestrutura import Infraestrutura
from src.infraestrutura.mininet import MininetExt
from src.infraestrutura.ryu import Ryu

from src.monitoramento import startMonitoramento

from mininet.log import setLogLevel

if __name__ == '__main__':
    setLogLevel('info')

    topo = ArvoreTopo()

    infraestrutura = Infraestrutura(100, topo)
    infraestrutura.up()