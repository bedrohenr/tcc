#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import info

from infraestrutura.mininet.topologia import ArvoreTopo

def start():
    topo = ArvoreTopo()
    # Instancia a rede informando que usará controlador remoto e Open vSwitch
    net = Mininet(
        topo=topo,
        controller=RemoteController,
        switch=OVSSwitch
    )

    # info('*** Adicionando Controlador Remoto (Ryu) ***\n')
    # # Aponta para o seu controlador Ryu (porta padrão OpenFlow: 6653)
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=8080)

    info('*** Iniciando a Rede ***\n')
    net.start()

    info('*** Executando CLI do Mininet ***\n')
    # CLI(net)
    net.pingAll()

    info('*** Finalizando a Rede ***\n')
    net.stop()