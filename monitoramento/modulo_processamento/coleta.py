from requests import get, exceptions

from monitoramento.influxdb import InfluxDBHelper

def getRXTXFromSwitch(root, dpid, switchPort = None):
    InfluxDB = InfluxDBHelper()
    port = ''
    if(switchPort):
        port = f"[{switchPort}]"

    url = f"{root}/stats/port/{dpid}{port}"

    print(url)

    try:
        response = get(url)

        data = response.json()
        # Porta 0 = local

        port_no = 1
        rx_bytes = data[str(dpid)][port_no]['rx_bytes']
        tx_bytes = data[str(dpid)][port_no]['tx_bytes']
        print(f"Switch s{dpid} Port #{port_no}")
        print(f"rx: { data[str(dpid)][port_no]['rx_bytes'] }")
        print(f"tx: { data[str(dpid)][port_no]['tx_bytes'] }")

        InfluxDB.write_port_rx_tx(dpid, port_no, rx_bytes, tx_bytes)

        port_no = 2
        rx_bytes = data[str(dpid)][port_no]['rx_bytes']
        tx_bytes = data[str(dpid)][port_no]['tx_bytes']
        print(f"Switch s{dpid} Port #{port_no}")
        print(f"rx: { data[str(dpid)][port_no]['rx_bytes'] }")
        print(f"tx: { data[str(dpid)][port_no]['tx_bytes'] }")

        InfluxDB.write_port_rx_tx(dpid, port_no, rx_bytes, tx_bytes)

        port_no = 3
        rx_bytes = data[str(dpid)][port_no]['rx_bytes']
        tx_bytes = data[str(dpid)][port_no]['tx_bytes']
        print(f"Switch s{dpid} Port #{port_no}")
        print(f"rx: { data[str(dpid)][port_no]['rx_bytes'] }")
        print(f"tx: { data[str(dpid)][port_no]['tx_bytes'] }")

        InfluxDB.write_port_rx_tx(dpid, port_no, rx_bytes, tx_bytes)

    except exceptions.ConnectionError:
        print('connection err')
