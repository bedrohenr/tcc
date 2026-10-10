from src.monitoramento import startMonitoramento

from src.infraestrutura.mininet.topologia import ArvoreTopo

topo = ArvoreTopo()

startMonitoramento(topo)
