import os
import sys
import subprocess
import time

def startRyu(app_path="ryu.app.simple_switch_13", porta=6653, venv_path=".venv", arquivo_log="ryu.log"):
    # OPÇÃO A: Pega automaticamente o binário do .venv que está executando este script
    # ryu_bin = os.path.join(sys.prefix, 'bin', 'ryu-manager')
    
    # OPÇÃO B: Caso você queira forçar um caminho relativo específico para a pasta do .venv
    ryu_bin = os.path.abspath(os.path.join(venv_path, 'bin', 'ryu-manager'))

    # Valida se o binário realmente existe na pasta do .venv
    print(ryu_bin)
    if not os.path.isfile(ryu_bin):
        raise FileNotFoundError(f"Binário do ryu-manager não encontrado em: {ryu_bin}")

    print(f"[*] Executando ryu-manager via .venv: {ryu_bin}")

    cmd = [
        ryu_bin,
        '--ofp-tcp-listen-port', str(porta),
        '--verbose',
        'ryu.app.ofctl_rest',
        app_path
    ]

    log_file = open(arquivo_log, "w")

    # Passa as variáveis de ambiente atuais para manter o contexto do .venv
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = sys.prefix
    env["PATH"] = f"{os.path.join(sys.prefix, 'bin')}:{env.get('PATH', '')}"

    processo = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
        env=env # Garante as variáveis de ambiente do .venv no subprocesso
    )

    time.sleep(2)

    if processo.poll() is not None:
        log_file.close()
        raise RuntimeError(f"Falha ao iniciar o ryu-manager. Verifique {arquivo_log}")

    return processo, log_file
