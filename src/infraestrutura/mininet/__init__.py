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

class MininetExt():
    # Configs Ryu
    RYU_IP='127.0.0.1'
    RYU_PORT=6653

    # Config Switch
    OVS13_PROTOCOL='OpenFlow13'

    def __init__(self, bw, topo):
        self.bandwidth = bw
        self.topology = topo

    def getRyu(self):
        # Configuração do controlador Ryu na porta 6653
        return partial(
            RemoteController,
            ip=self.RYU_IP,
            port=self.RYU_PORT
        )
    
    def getSwitchConfig(self):
        # Configura o switch para usar sempre o OpenFlow 1.3
        return partial(
            OVSSwitch, 
            protocols=self.OVS13_PROTOCOL
        )

    def start(self):

        # Configuração do controlador Ryu na porta 6653
        ryuController = self.getRyu()
        
        # Configura o switch para usar sempre o OpenFlow 1.3
        ovs13Switch = self.getSwitchConfig()

        link = custom(TCLink, bw=self.bandwidth)
        # host = custom(CPULimitedHost, cpu=4)

        net = Mininet(
            topo = self.topology,
            controller = ryuController,
            switch = ovs13Switch,
            # host = host,
            link = link
        )

        info('[*] Iniciando o Mininet \n\n')
        net.start()

        net.pingAll()
        # self.simularTrafego(net)

        info('[*] Finalizando o Mininet \n')
        net.stop()

    def simularTrafego(self, net):
        info('[*] Enviando pacotes \n\n')

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


    def clean(self):
        info('[*] Limpando residuos de execuções anteriores \n\n')
        Cleanup.cleanup()