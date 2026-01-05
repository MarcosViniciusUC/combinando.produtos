import csv
import random

# ----------------------------
# FUNÇÃO PARA CARREGAR PRODUTOS DO CSV
# ----------------------------
def carregar_produtos(arquivo_csv="produtos.csv"):
    produtos = []

    try:
        with open(arquivo_csv, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                codigo = row["codigo"].strip()
                descricao = row["descricao"].strip()
                preco = float(row["preco"])
                estoque = float(row["estoque"])

                if estoque > 0:  # 🔥 FILTRO CRÍTICO
                    produtos.append((codigo, descricao, preco, estoque))

    except Exception as erro:
        print("❌ ERRO AO CARREGAR PRODUTOS DO ARQUIVO!")
        print(erro)

    return produtos


# ----------------------------
# FUNÇÃO PARA GERAR COMBINAÇÃO ALEATÓRIA
# ----------------------------
def gerar_combinacao_aleatoria(produtos, valor_total, usados=[]):
    produtos_disponiveis = [
        p for p in produtos if p[0] not in usados and p[3] > 0
    ]

    tentativa = 0
    max_tentativas = 20000

    while tentativa < max_tentativas:
        tentativa += 1
        random.shuffle(produtos_disponiveis)

        combinacao = []
        soma = 0

        for item in produtos_disponiveis:
            if soma + item[2] <= valor_total:
                combinacao.append(item)
                soma = round(soma + item[2], 2)

            if soma == valor_total:
                return combinacao

    return None


# ----------------------------
# PROGRAMA PRINCIPAL
# ----------------------------
if __name__ == "__main__":

    produtos = carregar_produtos()

    if not produtos:
        print("Nenhum produto carregado!")
        exit()

    produtos_usados = []

    while True:
        valor = input("\nDigite o valor da venda (ou 'sair'): ")
        if valor.lower() == "sair":
            break

        try:
            valor = float(valor)
        except:
            print("Digite um valor válido!")
            continue

        combinacao = gerar_combinacao_aleatoria(produtos, valor, produtos_usados)

        if combinacao:
            print(f"\n🟩 Combinação encontrada para R$ {valor:.2f}:")
            for item in combinacao:
                print(f"- {item[0]} | {item[1]} | R$ {item[2]:.2f}")
                produtos_usados.append(item[0])
        else:
            print(f"\n🟥 Não foi possível encontrar combinação para R$ {valor:.2f}")
