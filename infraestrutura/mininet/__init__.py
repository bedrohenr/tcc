#!/usr/bin/env python3

from functools import partial

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import info

from infraestrutura.mininet.topologia import ArvoreTopo

def startMininet():
    # Configuração da topologia customizada
    topo = ArvoreTopo()

    # Configuração do controlador Ryu na porta 6653
    RyuController = partial(
        RemoteController,
        ip='127.0.0.1',
        port=6653
    )
    
    # Configura o switch para usar sempre o OpenFlow 1.3
    OVS13Switch = partial(
        OVSSwitch, 
        protocols='OpenFlow13'
    )

    # Instancia a rede informando que usará a topologia customizada, o Ryu corretamente e o Open vSwitch com OpenFlow 1.3
    net = Mininet(
        topo=topo,
        controller=RyuController,
        switch=OVS13Switch
    )

    info('[*] Iniciando o Mininet \n')
    net.start()

    info('[*] Pingando todos os hosts \n')
    net.pingAll()

    info('[*] Finalizando o Mininet \n')
    net.stop()