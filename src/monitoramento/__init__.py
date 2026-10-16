from time import sleep

from src.monitoramento.modulo_processamento import ModuloProcessamento

CONTROLLER_API_URL = "http://localhost:8080"

class Monitoramento():
    MODULO_PROCESSAMENTO = ModuloProcessamento()
    def __init__(self, topo):
        self.topo = topo

    # Retorna o DPID em base 10
    def getDPID(self, switch):
        # print(topo.nodeInfo(switch))
        # print(topo.nodeInfo(switch).get("dpid"))
        switch_info = self.topo.nodeInfo(switch)
        # print(switch_info.get('dpid'))
        dpid = int(switch_info.get('dpid'), 16)
        return dpid

    def start(self):
        while True:
            for switch in self.topo.switches():
                self.MODULO_PROCESSAMENTO.getRXTXFromSwitch(self.getDPID(switch))
            print()
            sleep(1)
