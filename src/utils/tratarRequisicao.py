from requests import get, post, exceptions

def tratarRequisicao(req, url, req_headers = None, req_body = None):
    print(f"[+] Fazendo requisição. url: {url}")

    data = {}
    print("cabecalhos")
    print(req_headers)
    print("body")
    print(req_body)
    try:
        if(req == 'get'):
            print("get req")
            data = get(url)
        elif(req == 'post'):
            print("post req")
            data = post(
                url,
                headers=req_headers,
                json=req_body
            )

        print(data)
        if(isJsonResponse(data)):
            return data.json()
        else:
            return data

    except exceptions.ConnectionError:
        print("[!] Erro: Falha na conexão com o servidor/host.")
        return data

    except exceptions.HTTPError as err:
        # Captura erros como 404, 500, 403, etc.
        if data.status_code == 404:
            print("[!] Erro: Endpoint não encontrado (404). Verifique a URL.")
        else:
            print(f"[!] Erro HTTP {data.status_code}: {err}")
        return data

    except exceptions.Timeout:
        print("[!] Erro: A requisição excedeu o tempo limite.")
        return data

    except exceptions.RequestException as err:
        # Captura genérica para qualquer outro erro da biblioteca requests
        print(f"[!] Erro inesperado no requests: {err}")
        return data
    
def isJsonResponse(response):

    content_type = response.headers.get("Content-Type", "")

    if "application/json" in content_type:
        # print("[+] A resposta é um JSON (verificado pelo cabeçalho).")
        return True
    else:
        # print(f"[-] A resposta NÃO é um JSON. Content-Type recebido: {content_type}")
        return False