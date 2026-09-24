from infraestrutura.mininet import start
from mininet.log import setLogLevel

if __name__ == '__main__':
    setLogLevel('info')

    # Inicia o mininet
    start() 