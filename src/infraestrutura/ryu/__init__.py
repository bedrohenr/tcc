import os
import sys
import subprocess
import time

class Ryu():

    VENV_PATH = '.venv'
    APP_PATH = 'ryu.app.simple_switch_13'
    APP_REST_API = 'ryu.app.ofctl_rest'
    APP_PORT = '6653'
    APP_LOG_FILE = 'src/infraestrutura/ryu/logs/ryu.log'

    # Preenchidos quando criado o processo
    process = None 
    log = None

    def __init__(self):
        self.bin = self.getBinary(self.VENV_PATH)

    def getBinary(self, venv_path):

        # OPÇÃO A: Pega automaticamente o binário do .venv que está executando este script
        # return = os.path.join(sys.prefix, 'bin', 'ryu-manager')
        
        # OPÇÃO B: Caso você queira forçar um caminho relativo específico para a pasta do .venv
        # precisa dessa opção pois o sistema roda o main em sudo
        return os.path.abspath(os.path.join(venv_path, 'bin', 'ryu-manager'))
    
    def start(self):

        if not os.path.isfile(self.bin):
            raise FileNotFoundError(f"[!] Binário do ryu-manager não encontrado em: {self.bin}")

        print(f"[*] Executando ryu-manager via .venv: {self.bin}")

        cmd = [
            self.bin,
            '--ofp-tcp-listen-port', self.APP_PORT,
            '--verbose',
            self.APP_PATH,
            self.APP_REST_API,
        ]

        self.log = open(self.APP_LOG_FILE, "w")

        # Passa as variáveis de ambiente atuais para manter o contexto do .venv
        env = os.environ.copy()
        env["VIRTUAL_ENV"] = sys.prefix
        env["PATH"] = f"{os.path.join(sys.prefix, 'bin')}:{env.get('PATH', '')}"

        self.process = subprocess.Popen(
            cmd,
            stdout=self.log,
            stderr=subprocess.STDOUT,
            text=True,
            env=env # Garante as variáveis de ambiente do .venv no subprocesso
        )

        time.sleep(2)

        if self.process.poll() is not None:
            self.log.close()
            raise RuntimeError(f"[!] Falha ao iniciar o ryu-manager. Verifique {self.APP_LOG_FILE}")
        
        print(f"[*] ryu-manager iniciado.")
    
    def end(self):
        # Garante o encerramento do ryu-manager ao final (mesmo se ocorrer erro)
        if self.process:
            print("[*] Encerrando o ryu-manager...")
            self.process.terminate() # Envia SIGTERM
            self.process.wait()      # Aguarda o processo fechar totalmente
        
        if self.log:
            self.log.close()
            
        print("[*] Processo do Ryu finalizado com sucesso.")

# def startRyu(app_path="ryu.app.simple_switch_13", porta=6653, venv_path=".venv", arquivo_log="ryu.log"):
#     # OPÇÃO A: Pega automaticamente o binário do .venv que está executando este script
#     # ryu_bin = os.path.join(sys.prefix, 'bin', 'ryu-manager')
    
#     # OPÇÃO B: Caso você queira forçar um caminho relativo específico para a pasta do .venv
#     ryu_bin = os.path.abspath(os.path.join(venv_path, 'bin', 'ryu-manager'))

#     # Valida se o binário realmente existe na pasta do .venv
#     print(ryu_bin)
#     if not os.path.isfile(ryu_bin):
#         raise FileNotFoundError(f"Binário do ryu-manager não encontrado em: {ryu_bin}")

#     print(f"[*] Executando ryu-manager via .venv: {ryu_bin}\n\n")

#     cmd = [
#         ryu_bin,
#         '--ofp-tcp-listen-port', str(porta),
#         '--verbose',
#         'ryu.app.ofctl_rest',
#         app_path
#     ]

#     log_file = open(arquivo_log, "w")

#     # Passa as variáveis de ambiente atuais para manter o contexto do .venv
#     env = os.environ.copy()
#     env["VIRTUAL_ENV"] = sys.prefix
#     env["PATH"] = f"{os.path.join(sys.prefix, 'bin')}:{env.get('PATH', '')}"

#     processo = subprocess.Popen(
#         cmd,
#         stdout=log_file,
#         stderr=subprocess.STDOUT,
#         text=True,
#         env=env # Garante as variáveis de ambiente do .venv no subprocesso
#     )

#     time.sleep(2)

#     if processo.poll() is not None:
#         log_file.close()
#         raise RuntimeError(f"Falha ao iniciar o ryu-manager. Verifique {arquivo_log}")

#     return processo, log_file
