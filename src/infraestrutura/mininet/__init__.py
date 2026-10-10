#!/usr/bin/env python3
from time import sleep
from functools import partial

from mininet.util import custom
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.clean import Cleanup
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import info

from src.infraestrutura.mininet.topologia import ArvoreTopo

def startMininet(topo):

    # Configuração da topologia customizada
    # topo = ArvoreTopo()

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

    link = custom(TCLink, bw=100)
    # host = custom(CPULimitedHost, cpu=4)
    # Instancia a rede informando que usará a topologia customizada, o Ryu corretamente e o Open vSwitch com OpenFlow 1.3
    net = Mininet(
        topo=topo,
        controller=RyuController,
        switch=OVS13Switch,
        # host=host,
        link=link
    )

    info('[*] Iniciando o Mininet \n\n')
    net.start()

    # info('[*] Pingando todos os hosts \n')
    # net.pingAll()

    # Inicia o teste de comunicacao de todos para todos
    port = 5001
    data_size = 5_000
    for h in net.hosts:
        h.cmd('iperf -s -p %s > /dev/null &' % port)
        
    h1 = net.get('h1')
    h2 = net.get('h2')
    for i in range(0, 99999):
        h1.cmd('iperf -c %s -p %s -n %d -i 1 -yc > /dev/null &' % (h2.IP(), port, data_size))
        print('pacote enviado')
        sleep(1)

    # for client in net.hosts:
    #     for server in net.hosts:
    #         if client != server:
    #             client.cmd('iperf -c %s -p %s -n %d -i 1 -yc > /dev/null &' % (server.IP(), port, data_size))
                
    info('[*] Finalizando o Mininet \n')
    net.stop()

def limparResiduosMininet():
    info('[*] Limpando residuos de execuções anteriores \n\n')
    Cleanup.cleanup()