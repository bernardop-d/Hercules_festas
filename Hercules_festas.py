import json

PRECOS = {
    "Conjunto": 20.00, "Mesa": 10.00, "Cadeira": 4.00,
    "Pula-pula pequeno": 200.00, "Pula-pula medio": 230.00,
    "Pula-pula grande": 250.00, "Piscina de bolinhas": 210.00,
    "Tina": 35.00, "Toboga": 690.00, "Ping-pong pro": 380.00,
    "Tamancobol": 190.00, "Air game": 350.00, "Pebolim": 250.00,
    "Castelinho": 650.00, "Fliperama": 360.00, "Pranchao": 120.00
}

def carregar_dados():
    try:
        with open("Materiais_alugados.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(dados):
    with open("Materiais_alugados.json", "w") as file:
        json.dump(dados, file, indent=1)

def processar_conjuntos(itens):
    mesas = sum(item['quantidade'] for item in itens if item['item'] == "Mesa")
    cadeiras = sum(item['quantidade'] for item in itens if item['item'] == "Cadeira")
    conjuntos = min(mesas, cadeiras // 4)
    cadeiras_restantes = cadeiras - (conjuntos * 4)
    
    novos_itens = []
    if conjuntos > 0:
        novos_itens.append({"item": "Conjunto", "quantidade": conjuntos})
    if cadeiras_restantes > 0:
        novos_itens.append({"item": "Cadeira", "quantidade": cadeiras_restantes})
    for item in itens:
        if item['item'] not in ["Mesa", "Cadeira"]:
            novos_itens.append(item)
    return novos_itens

def registrar_aluguel():
    try:
        nome = entrada_valida("Nome do cliente: ")
        contato = entrada_valida("Número de contato: ", int)
        endereco = entrada_valida("Endereço: ")
        data_entrega = entrada_valida("Data de entrega: ")

        itens_escolhidos = []
        print("\nItens disponíveis:")
        for i, (item, preco) in enumerate(PRECOS.items(), start=1):
            print(f"{i}. {item:<25} R$ {preco:.2f}")

        while True:
            try:
                escolha = int(input("\nDigite o número do item que deseja alugar (0 para finalizar): "))
                if escolha == 0:
                    break
                if 1 <= escolha <= len(PRECOS):
                    item_escolhido = list(PRECOS.keys())[escolha - 1]
                    quantidade = int(input(f"Quantas unidades de ({item_escolhido}) você deseja alugar? "))
                    
                    if quantidade > 0:
                        for item in itens_escolhidos:
                            if item['item'] == item_escolhido:
                                item['quantidade'] += quantidade
                                break
                        else:
                            itens_escolhidos.append({"item": item_escolhido, "quantidade": quantidade})
                        print(f"{quantidade} unidade(s) de {item_escolhido} adicionada(s) ao seu aluguel.")
                    else:
                        print("Quantidade inválida! Tente novamente.")
                else:
                    print("Opção inválida! Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        if not itens_escolhidos:
            print("Nenhum item foi selecionado. O aluguel não será registrado.")
            return

        itens_escolhidos = processar_conjuntos(itens_escolhidos)
        total = sum(PRECOS[item['item']] * item['quantidade'] for item in itens_escolhidos)
        
        aluguel = {"nome": nome.strip(), "endereco": endereco.strip(), "itens": itens_escolhidos, "total": total}
        
        alugueis = carregar_dados()
        alugueis.append(aluguel)
        salvar_dados(alugueis)

        print(f"\nAluguel de {nome} registrado com sucesso!")
        print(f"Valor total: R$ {total:.2f}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
def entrada_valida(mensagem, tipo=str):
    while True:
        try:
            valor = tipo(input(mensagem).strip())
            if valor:
                return valor
        except ValueError:
            pass
        print("Entrada inválida! Tente novamente.")

def gerar_nota(nome, contato, endereco, data_entrega, itens, total):
    with open(f"Nota_{nome.replace(' ', '_')}.txt", "w", encoding="utf-8") as file:
        file.write(f"Nome: {nome}\n")
        file.write(f"Cel de contato: {contato}\n")
        file.write(f"Endereço: {endereco}\n")
        file.write(f"Data de entrega: {data_entrega}\n\n")
        file.write("Itens alugados:\n")
        file.write("=" * 40 + "\n")
        file.write(f"{'Item':<25}{'Qtd':>5}{'Preço (R$)':>12}\n")
        file.write("=" * 40 + "\n")
        for item in itens:
            file.write(f"{item['item']:<25}{item['quantidade']:>5}{PRECOS[item['item']] * item['quantidade']:>12.2f}\n")
        file.write("=" * 40 + "\n")
        file.write(f"Total: R$ {total:.2f}\n")

def visualizar_alugueis():
    try:
        alugueis = carregar_dados()
        if alugueis:
            print("\nLista de aluguéis registrados:")
            for idx, aluguel in enumerate(alugueis, start=1):
                print(f"\n{idx}. Nome: {aluguel['nome']}")
                print(f"   Endereço: {aluguel['endereco']}")
                print("   Itens alugados:")
                for item in aluguel['itens']:
                    print(f"   - {item['quantidade']} unidade(s) de {item['item']}")
                
                if 'total' not in aluguel:
                    aluguel['total'] = sum(PRECOS[item['item']] * item['quantidade'] for item in aluguel['itens'])
                print(f"   Total: R$ {aluguel['total']:.2f}")
        else:
            print("\nNão há aluguéis registrados.")
    except Exception as e:
        print(f"Erro ao carregar os aluguéis: {e}")

def menu():
    while True:
        try:
            print("\n============= HERCULES FESTAS ==============")
            print("1. REGISTRAR ALUGUEL")
            print("2. VISUALIZAR NOTA")
            print("3. SAIR")
            print("\n============================================")
            opcao = input("Escolha uma opção (1/2/3): ").strip()

            if opcao == "1":
                registrar_aluguel()
            elif opcao == "2":
                visualizar_alugueis()
            elif opcao == "3":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    menu()
