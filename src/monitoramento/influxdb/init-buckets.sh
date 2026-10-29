#!/bin/bash
set -e

echo "[*] Criando buckets adicionais no InfluxDB v2..."

# O InfluxDB CLI já lê automaticamente a ORG e o TOKEN do ambiente do container
influx bucket create --name sdn_ports --retention 30d || true
influx bucket create --name sdn_meters --retention 7d || true
influx bucket create --name sdn_flows --retention 48h || true
influx bucket create --name sdn_events --retention 0 || true # 0 = retenção infinita

echo "[+] Buckets 'sdn_ports', 'sdn_flows' e 'sdn_events' criados com sucesso!"