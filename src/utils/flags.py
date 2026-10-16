import argparse

# Lidando com argumentos
parser = argparse.ArgumentParser()

# --c ou --coleta
parser.add_argument("-c", "--coleta", action="store_true", help="Executa o main.py com modo coleta de dados.")

# --t ou --test
parser.add_argument("-t", "--test", action="store_true", help="Executa o main.py com modo teste. Não gera tráfego no mininet.")

flags = parser.parse_args()