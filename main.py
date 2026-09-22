from infraestrutura.mininet import criar_rede
from mininet.log import setLogLevel

if __name__ == '__main__':
    setLogLevel('info')
    criar_rede()