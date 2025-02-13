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
        with open("Materiais_alugados.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(dados):
    with open("Materiais_alugados.json", "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=1, ensure_ascii=False)

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
    alugueis = carregar_dados()
    if not alugueis:
        print("Nenhum aluguel registrado.")
        return
    
    print("\nAlugueis registrados:")
    print("=" * 60)
    for aluguel in alugueis:
        print(f"Nome: {aluguel['nome']}")
        print(f"Contato: {aluguel['contato']}")
        print(f"Endereço: {aluguel['endereco']}")
        print(f"Data de entrega: {aluguel['data_entrega']}")
        print("Itens:")
        for item in aluguel['itens']:
            print(f"  - {item['item']} (Qtd: {item['quantidade']})")
        print(f"Total: R$ {aluguel['total']:.2f}")
        print("=" * 60)

def registrar_aluguel():
    try:
        while True:
            nome = input("Qual o nome do cliente? ").strip()
            if nome:
                break
            print("Nome não pode ser vazio!")
        
        while True:
            contato = input(f"Qual o número de contato de {nome}? ").strip()
            if contato:
                break
            print("Número de contato não pode ser vazio!")

        while True:
            endereco = input(f"Qual o endereço de {nome} e n° do local? ").strip()
            if endereco:
                break
            print("Endereço não pode ser vazio!")
        
        while True:
            data_entrega = input("Qual a data de entrega? ").strip()
            if data_entrega:
                break
            print("Data de entrega não pode ser vazia!")

        itens_escolhidos = []
        print("\nItens disponíveis para aluguel:")
        print("=" * 40)
        print(f"{'Nº':<5}{'Item':<25}{'Preço (R$)':>10}")
        print("=" * 40)
        for i, (item, preco) in enumerate(PRECOS.items(), start=1):
            print(f"{i:<5}{item:<25}{preco:>10.2f}")
        print("=" * 40)

        while True:
            try:
                escolha = int(input("\nDigite o número do item que deseja alugar (0 para finalizar): "))
                if escolha == 0:
                    break
                if 1 <= escolha <= len(PRECOS):
                    item_escolhido = list(PRECOS.keys())[escolha - 1]
                    while True:
                        quantidade = int(input(f"Quantas unidades de ({item_escolhido}) você deseja alugar? "))
                        if quantidade > 0:
                            break
                        print("Quantidade deve ser maior que zero!")
                    
                    for item in itens_escolhidos:
                        if item['item'] == item_escolhido:
                            item['quantidade'] += quantidade
                            break
                    else:
                        itens_escolhidos.append({"item": item_escolhido, "quantidade": quantidade})
                    print(f"{quantidade} unidade(s) de {item_escolhido} adicionada(s) ao seu aluguel.")
                else:
                    print("Opção inválida! Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        if not itens_escolhidos:
            print("Nenhum item foi selecionado. O aluguel não será registrado.")
            return

        total = sum(PRECOS[item['item']] * item['quantidade'] for item in itens_escolhidos)
        aluguel = {"nome": nome, "contato": contato, "endereco": endereco, "data_entrega": data_entrega, "itens": itens_escolhidos, "total": total}
        
        alugueis = carregar_dados()
        alugueis.append(aluguel)
        salvar_dados(alugueis)
        gerar_nota(nome, contato, endereco, data_entrega, itens_escolhidos, total)

        print(f"\nAluguel de {nome} registrado com sucesso!")
        print(f"Valor total: R$ {total:.2f}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    while True:
        try:
            print("\n============= HERCULES FESTAS ==============")
            print("1. REGISTRAR ALUGUEL")
            print("2. VISUALIZAR ALUGUEIS")
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
