from time import sleep

from src.monitoramento.modulo_processamento.coleta import getRXTXFromSwitch

CONTROLLER_API_URL = "http://localhost:8080"

def startMonitoramento(topo):

    for i in range(0,999999):
        for switch in topo.switches():
            # print(topo.nodeInfo(switch))
            # print(topo.nodeInfo(switch).get("dpid"))
            switch_info = topo.nodeInfo(switch)
            print(switch_info.get('dpid'))
            dpid = int(switch_info.get('dpid'), 16)

            getRXTXFromSwitch(CONTROLLER_API_URL, dpid)
        print()
        sleep(1)
