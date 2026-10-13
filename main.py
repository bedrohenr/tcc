from src.infraestrutura.mininet.topologia import ArvoreTopo
from src.infraestrutura.mininet import startMininet, limparResiduosMininet
from src.infraestrutura.ryu import Ryu

from src.monitoramento import startMonitoramento

from mininet.log import setLogLevel

def startInfraestrutura(topo):

    limparResiduosMininet()

    try:
        # # 1. Inicia o ryu-manager apontando para o seu script de monitoramento
        # ryu_process, log_fd = startRyu(
        #     app_path="ryu.app.simple_switch_13", 
        #     porta=6653,
        #     arquivo_log="src/infraestrutura/ryu/logs/ryu.log"
        # )

        ryu = Ryu()
        ryu.start()

        # 2. Aqui entra a chamada da sua rede Mininet (net.start(), pingAll, etc.)
        # Inicia o mininet
        startMininet(topo) 

    finally:
        ryu.end()

if __name__ == '__main__':
    setLogLevel('info')

    topo = ArvoreTopo()

    startInfraestrutura(topo)
    # startMonitoramento()
