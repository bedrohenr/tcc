from os import getenv

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBHelper:
    PORTS_DATA_BUCKET="sdn_ports"
    METERS_DATA_BUCKET="sdn_meters"

    def __init__(
        self, 
        url="http://localhost:8086", 
        token="5208d80fce61660a91651d355f54712f6a414f84b61da9289bcb678ce9e1aa0a", 
        org="sdn_org", 
    ):
        self.url = url
        self.token = token
        self.org = org
        
        # Inicializa o cliente InfluxDB v2
        self.client = InfluxDBClient(
            url=self.url, 
            token=self.token, 
            org=self.org
        )
        
        # Modo SYNCHRONOUS garante que a métrica é gravada imediatamente a cada ciclo de polling
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_ports_data(self, dpid, port_no, rx_bytes, tx_bytes, rx_packets, tx_packets, rx_dropped, tx_dropped, rx_errors, tx_errors, timestamp):
        point = (
            Point("port_stats")
            .tag("dpid", f"{dpid}")                 # DPID
            .tag("port_no", f"{port_no}")           # Número da porta no switch
            .field("rx_bytes", int(rx_bytes))       # Total acumulado de bytes recebidos
            .field("tx_bytes", int(tx_bytes))       # Total acumulado de bytes transmitidos
            .field("rx_packets", int(rx_packets))   # Total acumulado de pacotes recebidos
            .field("tx_packets", int(tx_packets))   # Total acumulado de pacotes transmitidos
            .field("rx_dropped", int(rx_dropped))       
            .field("tx_dropped", int(tx_dropped))       
            .field("rx_errors", int(rx_errors))       
            .field("tx_errors", int(tx_errors))       
            .time(timestamp)                        # Timestamp
        )

        try:
            self.write_api.write(bucket=self.PORTS_DATA_BUCKET, org=self.org, record=point)
        except Exception as e:
            print(f"[!] Erro ao enviar métricas para o InfluxDB: {e}")
        
    def write_meter_data(self, dpid, meter_id, flow_count, packet_in_count, byte_in_count, packet_band_count, byte_band_count, timestamp):
        point = (
            Point("meter_stats")
            .tag("dpid", f"{dpid}")                                 # DPID
            .tag("meter_id", f"{meter_id}")                       # ID do medidor
            .field("flow_count", int(flow_count))                   # Quantidade de fluxos utilizando o medidor
            .field("packet_in_count", int(packet_in_count))         # 
            .field("byte_in_count", int(byte_in_count))             # 
            .field("packet_band_count", int(packet_band_count))     # Total acumulado de pacotes transmitidos
            .field("byte_band_count", int(byte_band_count))         # Total acumulado de pacotes transmitidos
            .time(timestamp)                                        # Timestamp
        )

        # print(f"{dpid}, {meter_id}, {flow_count}, {packet_in_count}, {byte_in_count}, {packet_band_count}, {timestamp}")

        try:
            self.write_api.write(bucket=self.METERS_DATA_BUCKET, org=self.org, record=point)
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