from src.infraestrutura.mininet.topologia import ArvoreTopo
from src.infraestrutura import Infraestrutura
from src.monitoramento import Monitoramento

from src.utils.flags import flags

if __name__ == '__main__':
    topo = ArvoreTopo()


    if(flags.coleta == True):
        print("flags coleta true")
        monitoramento = Monitoramento(topo)
        monitoramento.start()
        exit()

    infraestrutura = Infraestrutura(100, topo, flags.test)

    try:
        infraestrutura.up()
    except KeyboardInterrupt:
        print("\n[!] Simulação interrompida pelo usuário.")