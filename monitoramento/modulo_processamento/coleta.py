from requests import get

def getRXFromSwitchPort(root, dpid, switchPort = None):
    port = ''
    if(switchPort):
        port = f"[{switchPort}]"

    url = f"{root}/stats/port/{dpid}{port}"

    print(url)

    response = get(url)

    data = response.json()
    # print(data["2"][1])

    port = 1
    print(f"Switch {dpid} Port #{port}")
    print(f"rx: { data[str(dpid)][port]['rx_bytes'] }")
    print(f"tx: { data[str(dpid)][port]['tx_bytes'] }")

    port = 2
    print(f"Switch {dpid} Port #{port}")
    print(f"rx: { data[str(dpid)][port]['rx_bytes'] }")
    print(f"tx: { data[str(dpid)][port]['tx_bytes'] }")

    port = 3
    print(f"Switch {dpid} Port #{port}")
    print(f"rx: { data[str(dpid)][port]['rx_bytes'] }")
    print(f"tx: { data[str(dpid)][port]['tx_bytes'] }")

    # print(data["rx_bytes"])
    # print(data["tx_bytes"])
    # print(response.content)
    # for r in response.json():
    #     print(r.get("rx_bytes"))
    #     print(r.get("tx_bytes"))
    #     print()
    # print(response["rx_bytes"])
    # print(response["tx_bytes"])

