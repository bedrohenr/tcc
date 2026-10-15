from src.infraestrutura.mininet.topologia import ArvoreTopo
from src.infraestrutura import Infraestrutura
from src.infraestrutura.mininet import MininetExt
from src.infraestrutura.ryu import Ryu


if __name__ == '__main__':
    topo = ArvoreTopo()

    infraestrutura = Infraestrutura(100, topo)

    try:
        infraestrutura.up()
    except KeyboardInterrupt:
        print("\n[!] Simulação interrompida pelo usuário.")