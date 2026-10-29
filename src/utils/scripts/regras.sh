#!/bin/bash

echo "A criar o medidor..."

curl -i -X POST -H "Content-Type: application/json" -d '{ "dpid": 2, "flags": "KBPS", "meter_id": 1, "bands": [{ "type": "DROP", "rate": 1000 }]}' http://localhost:8080/stats/meterentry/add

echo -e "A aplicar a regra de fluxo..."
curl -i -X POST -H "Content-Type: application/json" -d '{ "dpid": 2, "priority": 100,"match": { "dl_type": 2048, "nw_dst": "10.0.0.2" }, "actions": [ {"type": "METER", "meter_id": 1}, {"type": "OUTPUT", "port": 2}]}' http://localhost:8080/stats/flowentry/add

echo -e "Medidores e regras de fluxo instaladas!"