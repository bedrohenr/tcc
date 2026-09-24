#!/usr/bin/env python3
from time import sleep
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

    # info('[*] Pingando todos os hosts \n')
    # net.pingAll()

    # Inicia o teste de comunicacao de todos para todos
    port = 5001
    data_size = 5_000_000_000
    for h in net.hosts:
        h.cmd('iperf -s -p %s > /dev/null &' % port)
        
    h1 = net.get('h1')
    h2 = net.get('h2')
    while(True):
        h1.cmd('iperf -c %s -p %s -n %d -i 1 -yc > /dev/null &' % (h2.IP(), port, data_size))
        sleep(5)

    # for client in net.hosts:
    #     for server in net.hosts:
    #         if client != server:
    #             client.cmd('iperf -c %s -p %s -n %d -i 1 -yc > /dev/null &' % (server.IP(), port, data_size))
                
    info('[*] Finalizando o Mininet \n')
    net.stop()