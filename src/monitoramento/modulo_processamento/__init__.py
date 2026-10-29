from requests import get, exceptions
from time import time
from datetime import datetime, timezone

from src.utils.tratarRequisicao import tratarRequisicao
from src.monitoramento.influxdb import InfluxDBHelper

class ModuloProcessamento():
    ROOT_URL = 'http://localhost:8080'
    InfluxDB = InfluxDBHelper()

    # Memória de estado anterior: {(dpid, port_no): (rx_bytes, timestamp)}
    prevTX = {} # Up
    prevRX = {} # Down

    # Get RX e TX das portas dos switches
    def collectPortData(self, dpid):
        url = f"{self.ROOT_URL}/stats/port/{dpid}"

        data = tratarRequisicao("get", url)

        # Checando falha na requisição     
        if not data:
            return

        # Passa por cada interface excluindo a LOCAL
        dpid_str = str(dpid)
        for port in data[dpid_str]:
            port_no = port.get("port_no")
            if port_no != "LOCAL":
                # print(port.get("port_no"))
                # rx_bytes = port.get('rx_bytes')
                # tx_bytes = port.get('tx_bytes')
                # rx_packets = port.get('rx_packets')
                # tx_packets = port.get('tx_packets')
                # rx_dropped = port.get()
                # print(rx_bytes)
                # print(tx_bytes)

                # self.throughputUp(dpid, port_no, tx_bytes)
                # self.throughputDown(dpid, port_no, rx_bytes)

                timestamp = datetime.now(timezone.utc)
                self.InfluxDB.write_ports_data(
                    dpid, port_no,
                    port.get('rx_bytes'), port.get('tx_bytes'),
                    port.get('rx_packets'), port.get('tx_packets'), 
                    port.get('rx_dropped'), port.get('tx_dropped'), 
                    port.get('rx_errors'), port.get('tx_errors'), 
                    timestamp
                )

    # Coletando taxa de medidores
    def collectMeterData(self, dpid):
        url = f"{self.ROOT_URL}/stats/meter/{dpid}"

        try:
            data = tratarRequisicao("get", url)

            # Checando falha na requisição     
            if not data:
                return

            dpid_str = str(dpid)
            print(data)
            meter_data = data[dpid_str]

            if not meter_data:
                return

            # for meter in data[dpid_str]:
            meter = meter_data[0]
            print(meter)
            if not meter:
                return

            # print(meter.get("len"))
            # print(meter.get('band_stats'))
            # print(meter.get('band_stats')[0].get('packet_band_count'))
            # print(meter.get('band_stats')[0].get('byte_band_count'))
            packet_band_count = meter.get('band_stats')[0].get('packet_band_count')
            byte_band_count = meter.get('band_stats')[0].get('byte_band_count')
            # print("meter id: " + meter.get("meter_id"))
            timestamp = datetime.now(timezone.utc)
            self.InfluxDB.write_meter_data(
                dpid, meter.get("meter_id"),
                meter.get('flow_count'), 
                meter.get('packet_in_count'),
                meter.get('byte_in_count'), 
                packet_band_count,
                byte_band_count,
                timestamp
            )
        except exceptions.ConnectionError:
            print('connection err')