import os
import sys
import subprocess
from time import sleep

from requests import post
from json import dumps

from src.utils.tratarRequisicao import tratarRequisicao
from src.monitoramento.modulo_processamento import ModuloProcessamento

CONTROLLER_API_URL = "http://localhost:8080"

class Monitoramento():
    MODULO_PROCESSAMENTO = ModuloProcessamento()
    COLETA_LOG_FILE = 'src/monitoramento/logs/coleta.log'
    VENV_PATH = '.venv'

    process = None
    log = None

    medidoresInstalados = False
    regrasInstaladas = False

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

    # Retorna true os medidores e regras foram todos instalados
    def isEnvReady(self):
        print(f"Ready? {self.medidoresInstalados} - {self.regrasInstaladas}")
        return (
            self.medidoresInstalados == True and 
            self.regrasInstaladas == True
        )

    def start(self):
        try:
            sleep(5) # Aguardando inicio da API
            while True:
                if not self.isEnvReady():
                    self.inicializaMedidoresRegras()
                    continue # Nao executa a coleta até configurar o ambiente

                print("Ayooooo")
                for switch in self.topo.switches():
                    self.MODULO_PROCESSAMENTO.collectPortData(self.getDPID(switch))
                    self.MODULO_PROCESSAMENTO.collectMeterData(self.getDPID(switch))
                print()
                sleep(1)
        except KeyboardInterrupt:
            print("\n[!] Coleta de dados interrompida pelo usuário.")


    def getBinary(self, venv_path):
        # OPÇÃO A: Pega automaticamente o binário do .venv que está executando este script
        # return os.path.join(sys.prefix, 'bin', 'python')
        
        # OPÇÃO B: Caso você queira forçar um caminho relativo específico para a pasta do .venv
        # precisa dessa opção pois o sistema roda o main em sudo
        return os.path.abspath(os.path.join(venv_path, 'bin', 'python'))

    def startProcess(self):
        self.bin = self.getBinary(self.VENV_PATH)
        print(self.bin)

        if not os.path.isfile(self.bin):
            raise FileNotFoundError(f"[!] Binário do python não encontrado em: {self.bin}")

        print(f"[*] Executando ryu-manager via .venv: {self.bin}")

        cmd = [
            self.bin,
            './main.py',
            '--coleta',
        ]

        self.log = open(self.COLETA_LOG_FILE, "w")

        # Passa as variáveis de ambiente atuais para manter o contexto do .venv
        env = os.environ.copy()
        env["VIRTUAL_ENV"] = sys.prefix
        env["PATH"] = f"{os.path.join(sys.prefix, 'bin')}:{env.get('PATH', '')}"

        self.process = subprocess.Popen(
            cmd,
            stdout=self.log,
            stderr=subprocess.STDOUT,
            text=True,
            env=env # Garante as variáveis de ambiente do .venv no subprocesso
        )

        # time.sleep(2)

        if self.process.poll() is not None:
            self.log.close()
            raise RuntimeError(f"[!] Falha ao iniciar a coleta de dados. Verifique {self.COLETA_LOG_FILE}")
        
        print(f"[*] Coleta de dados iniciada.")
    
    def endProcess(self):
        # Garante o encerramento da coleta ao final (mesmo se ocorrer erro)
        if self.process:
            print("[*] Encerrando a coleta de dados...")
            self.process.terminate() # Envia SIGTERM
            self.process.wait()      # Aguarda o processo fechar totalmente
        
        if self.log:
            self.log.close()
            
        print("[*] Processo de Coleta de dados finalizado com sucesso.")
    
    def inicializaMedidoresRegras(self):
        print("[*] Configurando Medidores e Regras de Fluxo...")
        self.inicializaMedidores()
        self.inicializaRegrasDeFluxo()

    def inicializaMedidores(self):
        print("[*] Instalando Medidores...")

        if self.medidoresInstalados:
            return

        # Criando o Medidor (Meter ID: 1) no Switch 2 (DPID 2) com limite de 1000 kbps (1 Mbps)
        meter_data = {
            "dpid": 2,
            "flags": "KBPS",
            "meter_id": 1,
            "bands": [
                {
                    "type": "DROP",
                    "rate": 1000
                }
            ]
        }
        
        response = tratarRequisicao(
            "post",
            f"{CONTROLLER_API_URL}/stats/meterentry/add",
            {"Content-Type": "application/json"},
            meter_data
        )
        # print("meter response")
        # print(res)
        # print(dir(res))
        if response and response.status_code == 200:
            self.medidoresInstalados = True
            print("[+] Medidor criado com sucesso!")

    def inicializaRegrasDeFluxo(self):
        print("[*] Instalando Regras de Fluxo no Ryu...")
        # Criando a Regra de Fluxo (Flow Entry) associando o tráfego ao Meter 1
        flow_data = {
            "dpid": 2,
            "priority": 100,
            "match": {
                "dl_type": 2048,
                "nw_dst": "10.0.0.2"
            },
            "actions": [
                {"type": "METER", "meter_id": 1},
                {"type": "OUTPUT", "port": 2}
            ]
        }
        
        # print(dumps(flow_data))
        response = tratarRequisicao(
            "post",
            f"{CONTROLLER_API_URL}/stats/flowentry/add",
            {"Content-Type": "application/json"},
            flow_data
        )
        # print("rule response")
        # print(response)
        # print()
        if response and response.status_code == 200:
            self.regrasInstaladas = True
            print("[+] Regra de Fluxo com medidor adicionada com sucesso!")