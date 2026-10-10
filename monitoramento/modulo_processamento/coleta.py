from requests import get, exceptions

from monitoramento.influxdb import InfluxDBHelper

def getRXTXFromSwitch(root, dpid):
    InfluxDB = InfluxDBHelper()
    url = f"{root}/stats/port/{dpid}"
    print(url)

    try:
        response = get(url)
        data = response.json()

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
                InfluxDB.write_port_rx_tx(dpid, port_no, rx_bytes, tx_bytes)

    except exceptions.ConnectionError:
        print('connection err')
