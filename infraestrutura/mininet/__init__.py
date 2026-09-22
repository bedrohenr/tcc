#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import info

def criar_rede():
    # Instancia a rede informando que usará controlador remoto e Open vSwitch
    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    info('*** Adicionando Controlador Remoto (Ryu) ***\n')
    # Aponta para o seu controlador Ryu (porta padrão OpenFlow: 6653)
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    info('*** Adicionando Switches ***\n')
    # Força o uso do protocolo OpenFlow 1.3
    s1 = net.addSwitch('s1', protocols='OpenFlow13')

    info('*** Adicionando Hosts ***\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')

    info('*** Criando Enlaces ***\n')
    # net.addLink(h1, s1)
    # net.addLink(h2, s1)

    info('*** Iniciando a Rede ***\n')
    net.start()

    info('*** Executando CLI do Mininet ***\n')
    # CLI(net)

    info('*** Finalizando a Rede ***\n')
    net.stop()
