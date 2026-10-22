from src.infraestrutura.mininet.topologia import ArvoreTopo
from src.infraestrutura import Infraestrutura
from src.monitoramento import Monitoramento

from src.utils.flags import flags

if __name__ == '__main__':
    topo = ArvoreTopo()

    # Monitoramento executara o main em subprocesso com esta flag -c
    if(flags.coleta == True):
        monitoramento = Monitoramento(topo)
        monitoramento.start()
        exit()

    try:
        # Monitoramento    
        monitoramento = Monitoramento(topo)
        monitoramento.startProcess()

        # Infraestrutura
        infraestrutura = Infraestrutura(100, topo, flags.test)
        infraestrutura.up()
    except KeyboardInterrupt:
        print("\n[!] Simulação interrompida pelo usuário.")
    finally:
        monitoramento.endProcess()
