from os import getenv

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBHelper:
    def __init__(
        self, 
        url="http://localhost:8086", 
        token="5208d80fce61660a91651d355f54712f6a414f84b61da9289bcb678ce9e1aa0a", 
        org="sdn_org", 
        bucket="sdn_metrics"
    ):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        
        # Inicializa o cliente InfluxDB v2
        self.client = InfluxDBClient(
            url=self.url, 
            token=self.token, 
            org=self.org
        )
        
        # Modo SYNCHRONOUS garante que a métrica é gravada imediatamente a cada ciclo de polling
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_port_rx_tx(self, dpid, port_no, rx_bytes, tx_bytes):
        point = (
            Point("port_throughput")
            .tag("dpid", f"{dpid:016x}")          # DPID no formato hexadecimal de 16 dígitos
            .tag("port_no", str(port_no))         # Número da porta no switch
            .field("rx_bytes", int(rx_bytes))     # Total acumulado de bytes recebidos
            .field("tx_bytes", int(tx_bytes))     # Total acumulado de bytes transmitidos
        )

        try:
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        except Exception as e:
            print(f"[!] Erro ao enviar métricas para o InfluxDB: {e}")
        
    def write_port_throughput(self, dpid, port_no, rx_bps, tx_bps, rx_bytes, tx_bytes):
        """
        Escreve as métricas de vazão calculadas para uma porta específica no InfluxDB.
        """
        point = (
            Point("port_throughput")
            .tag("dpid", f"{dpid:016x}")          # DPID no formato hexadecimal de 16 dígitos
            .tag("port_no", str(port_no))         # Número da porta no switch
            .field("rx_bps", float(rx_bps))       # Vazão de recepção (bits/s)
            .field("tx_bps", float(tx_bps))       # Vazão de transmissão (bits/s)
            .field("rx_bytes", int(rx_bytes))     # Total acumulado de bytes recebidos
            .field("tx_bytes", int(tx_bytes))     # Total acumulado de bytes transmitidos
        )
        
        try:
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        except Exception as e:
            print(f"[!] Erro ao enviar métricas para o InfluxDB: {e}")

    def close(self):
        """Encerra o cliente de forma limpa."""
        self.client.close()