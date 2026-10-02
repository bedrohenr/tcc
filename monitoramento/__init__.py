from time import sleep

from monitoramento.modulo_processamento.coleta import getRXFromSwitchPort

ROOT_URL = "http://localhost:8080"

def startMonitoramento():
    for i in range(0,5):
        getRXFromSwitchPort(ROOT_URL, 2)
        print()
        sleep(1)
