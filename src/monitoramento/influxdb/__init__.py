from os import getenv

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBHelper:
    PORTS_DATA_BUCKET="sdn_ports"
    METERS_DATA_BUCKET="sdn_meters"
    FLOW_DATA_BUCKET="sdn_flows"

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
            print(f"[!] Erro ao enviar métricas de portas para o InfluxDB: {e}")
        
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
            print(f"[!] Erro ao enviar métricas do medidor para o InfluxDB: {e}")

    def write_flow_data(self, dpid, flows):
    
        try:
            # 2. Inicializar o cliente do InfluxDB
            # client = InfluxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
            # write_api = client.write_api(write_options=SYNCHRONOUS)

            points = []
            for flow in flows:
                # Extrair contadores principais
                packet_count = flow.get("packet_count", 0)
                byte_count = flow.get("byte_count", 0)
                priority = flow.get("priority", 0)
                cookie = flow.get("cookie", 0)
                
                # Extrair informações do Match (critérios da regra)
                match = flow.get("match", {})
                in_port = match.get("in_port", "unknown")
                nw_src = match.get("ipv4_src", match.get("nw_src", "all"))
                nw_dst = match.get("ipv4_dst", match.get("nw_dst", "all"))

                # Exemplo de extração do meter_id nas instruções do fluxo retornado pelo Ryu
                meter_id = "none" # Valor padrão caso o fluxo não tenha QoS

                if "actions" in flow:
                    for action in flow.get("actions", None):
                        # print("action: ")
                        # print(action)
                        # if "type" in action and action["type"] == "METER":
                        #     meter_id = str(action.get("meter_id", "unknown"))
                        action_split = action.split(":")
                        print("action split: ", action_split)
                        if action_split[0] == "METER":
                            meter_id = action_split[1] # Pega o ID do meter em "METER:ID"
                            print(meter_id)

                # Construir o Point para o InfluxDB v2
                point = Point("flow_stats") \
                    .tag("dpid", str(dpid)) \
                    .tag("meter_id", meter_id) \
                    .tag("priority", str(priority)) \
                    .tag("cookie", str(cookie)) \
                    .tag("in_port", str(in_port)) \
                    .tag("nw_src", str(nw_src)) \
                    .tag("nw_dst", str(nw_dst)) \
                    .field("packet_count", int(packet_count)) \
                    .field("byte_count", int(byte_count))
                
                print("point: ")
                print(point)
                points.append(point)

            self.write_api.write(bucket=self.FLOW_DATA_BUCKET, org=self.org, record=points)
            print(f"[+] Sucesso: {len(points)} fluxos do DPID {dpid} registados no InfluxDB.")
        except Exception as e:
            print(f"[!] Erro ao processar/enviar dados de fluxo para o InfluxDB: {e}")

    def close(self):
        """Encerra o cliente de forma limpa."""
        self.client.close()