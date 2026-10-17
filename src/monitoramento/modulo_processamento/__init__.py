from requests import get, exceptions
from time import time

from src.monitoramento.influxdb import InfluxDBHelper

class ModuloProcessamento():
    ROOT_URL = 'http://localhost:8080'
    InfluxDB = InfluxDBHelper()

    # Memória de estado anterior: {(dpid, port_no): (rx_bytes, timestamp)}
    prevTX = {} # Up
    prevRX = {} # Down

    def tratarRequisicao(self, url):
        request_url = f"{self.ROOT_URL}{url}"
        print(f"[+] Fazendo requisição. url: {request_url}")
        try:
            data = get(request_url)
            print(data)
            if(data):
                print("dados coletados")
                return data.json()
            else:
                print("nada")
        # except exceptions.ConnectionError:
        #     print('[!] Não foi possível Erro de conexão')

        except exceptions.ConnectionError:
            print("[!] Erro: Falha na conexão com o servidor/host.")

        except exceptions.HTTPError as err:
            # Captura erros como 404, 500, 403, etc.
            if data.status_code == 404:
                print("[!] Erro: Endpoint não encontrado (404). Verifique a URL.")
            else:
                print(f"[!] Erro HTTP {data.status_code}: {err}")

        except exceptions.Timeout:
            print("[!] Erro: A requisição excedeu o tempo limite.")

        except exceptions.RequestException as err:
            # Captura genérica para qualquer outro erro da biblioteca requests
            print(f"[!] Erro inesperado no requests: {err}")

    def getRXTXFromSwitch(self, dpid):
        url = f"/stats/port/{dpid}"

        try:
            data = self.tratarRequisicao(url)

            # Checando falha na requisição     
            if not data:
                return

            # Passa por cada interface excluindo a LOCAL
            dpid_str = str(dpid)
            for port in data[dpid_str]:
                port_no = port.get("port_no")
                if port_no != "LOCAL":
                    # print(port.get("port_no"))
                    rx_bytes = port.get('rx_bytes')
                    tx_bytes = port.get('tx_bytes')
                    # print(rx_bytes)
                    # print(tx_bytes)

                    self.throughputUp(dpid, port_no, tx_bytes)
                    self.throughputDown(dpid, port_no, rx_bytes)

                    self.InfluxDB.write_port_rx_tx(dpid, port_no, rx_bytes, tx_bytes)

        except exceptions.ConnectionError:
            print('connection err')

    # Vazão Upload
    def throughputUp(self, dpid, port_no, tx_bytes):
        time_now = time()
        key = (dpid, port_no)

        if key in self.prevTX:
            # tx_bytes_prev, time_prev = self.prevTX[key]
            
            # dt = time_now - time_prev
            # delta_bytes = tx_bytes - tx_bytes_prev

            # if dt > 0 and delta_bytes >= 0:
            #     # Cálculo da vazão instantânea em bits por segundo (bps)
            #     tx_bps = (delta_bytes * 8) / dt
                
            #     # Para converter para Megabits por segundo (Mbps):
            rx_mbps = self.getThroughput(key, tx_bytes, time_now)
                
            print(f"Switch {dpid} Porta {port_no}: {rx_mbps:.2f} Mbps")

        # Atualiza o estado para o próximo ciclo de amostragem
        self.prevTX[key] = (tx_bytes, time_now)

    # Vazão Download
    def throughputDown(self, dpid, port_no, rx_bytes):
        time_now = time()
        key = (dpid, port_no)

        if key in self.prevRX:
            # tx_bytes_prev, time_prev = self.prevTX[key]
            
            # dt = time_now - time_prev
            # delta_bytes = tx_bytes - tx_bytes_prev

            # if dt > 0 and delta_bytes >= 0:
            #     # Cálculo da vazão instantânea em bits por segundo (bps)
            #     tx_bps = (delta_bytes * 8) / dt
                
            #     # Para converter para Megabits por segundo (Mbps):
            rx_mbps = self.getThroughput(key, rx_bytes, time_now)
                
            print(f"Switch {dpid} Porta {port_no}: {rx_mbps:.2f} Mbps")

        # Atualiza o estado para o próximo ciclo de amostragem
        self.prevTX[key] = (rx_bytes, time_now)

    # ((bytes_atual - bytes_anterior) * 8)/t
    def getThroughput(self, key, bytes, time_now):
        bytes_prev, time_prev = self.prevTX[key]
        
        dt = time_now - time_prev
        delta_bytes = bytes - bytes_prev

        mbps = 0
        if dt > 0 and delta_bytes >= 0:
            # Cálculo da vazão instantânea em bits por segundo (bps)
            bps = (delta_bytes * 8) / dt
            
            # Para converter para Megabits por segundo (Mbps):
            mbps = bps / 1_000_000

        return mbps