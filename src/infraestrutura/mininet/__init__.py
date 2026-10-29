#!/usr/bin/env python3
from time import sleep
from functools import partial
from random import uniform, randint, sample, choice 

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

    def __init__(self, bw, topo, test_mode):
        self.bandwidth = bw
        self.topology = topo
        self.test_mode = test_mode

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

        if(self.test_mode == True):
            CLI(net)
            net.pingAll()
        else:
            self.simularTrafego(net)

        info('[*] Finalizando o Mininet \n')
        net.stop()

    def simularTrafego(self, net):
        info('[*] Iniciando geração de tráfego')
        hosts = net.hosts

        # Constantes para comunicacao de todos para todos (hosts)
        PORT = 5001
        NUM_PACOTES = 99999999999
        MIN_DATA_SIZE = 1_000       # 1 KB
        MAX_DATA_SIZE = 50_000_000  # 1 MB
        PAUSA_MIN = 0.5             # Segundos
        PAUSA_MAX = 3.0             # Segundos
        BANDWIDTHS = ['200k', '500k', '1M', '2M', '5M', '10M', '15M']

        print("[*] Subindo servidores iperf em background em todos os hosts...")
        for h in hosts:
            h.cmd(f"iperf -s -p {PORT} -u > /dev/null &")

        print("[*] Servidores iperf prontos")
        sleep(1)
            
        try:
            for i in range(NUM_PACOTES):
                # Randomiza os hosts a serem escolhidos (Origem != Destino)
                origem, destino = sample(hosts, 2)

                # Randomiza o tamanho dos dados (bytes)
                data_size = randint(MIN_DATA_SIZE, MAX_DATA_SIZE)
                
                # Randomiza o intervalo de pausa
                pausa = uniform(PAUSA_MIN, PAUSA_MAX)

                bandwidth = choice(BANDWIDTHS)

                # Dispara o cliente iperf em background (&)
                cmd = f"iperf -c {destino.IP()} -p {PORT} -n {data_size} -u -b {bandwidth} -y c > /dev/null 2>&1 &"
                origem.cmd(cmd)

                print(f"[{i+1}/∞] {origem.name} ({origem.IP()}) -> {destino.name} ({destino.IP()}) | {data_size / 1e6:.2f} MB @ {bandwidth}")

                # Aguardando o tempo aleatorio
                sleep(pausa)

            print("\n[!] Fim da geração de tráfego.")

        except KeyboardInterrupt:
            print("\n[!] Geração de tráfego interrompida pelo usuário.")
        finally:
            print("[*] Encerrando processos iperf nos hosts...")
            for h in hosts:
                h.cmd('killall -9 iperf > /dev/null 2>&1')

    def clean(self):
        info('[*] Limpando residuos de execuções anteriores')
        Cleanup.cleanup()
        