from infraestrutura.mininet import startMininet
from infraestrutura.ryu import startRyu
from mininet.log import setLogLevel

def start():
    ryu_process = None
    log_fd = None

    try:
        # 1. Inicia o ryu-manager apontando para o seu script de monitoramento
        ryu_process, log_fd = startRyu(
            app_path="ryu.app.simple_switch_13", 
            porta=6653,
            arquivo_log="infraestrutura/ryu/logs/ryu.log"
        )

        # 2. Aqui entra a chamada da sua rede Mininet (net.start(), pingAll, etc.)
        # Inicia o mininet
        startMininet() 

    finally:
        # 3. Garante o encerramento do ryu-manager ao final (mesmo se ocorrer erro)
        if ryu_process:
            print("[*] Encerrando o ryu-manager...")
            ryu_process.terminate() # Envia SIGTERM
            ryu_process.wait()      # Aguarda o processo fechar totalmente
        
        if log_fd:
            log_fd.close()
            
        print("[+] Processo do Ryu finalizado com sucesso.")

if __name__ == '__main__':
    setLogLevel('info')
    start()
