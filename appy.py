import streamlit as st
from scipy.stats import binom

def calcular_probabilidade_aceitacao(tamanho_amostra, itens_aceitos, taxa_defeitos):
    # Calcular a probabilidade de aceitação usando a distribuição binomial
    probabilidade_aceitacao = binom.cdf(itens_aceitos, tamanho_amostra, taxa_defeitos)
    return probabilidade_aceitacao

def calcular_ITM(tamanho_lote, tamanho_amostra, taxa_aceitacao):
    # Calcular o ITM
    ITM = (1 - taxa_aceitacao) * (tamanho_lote - tamanho_amostra) + tamanho_amostra
    return ITM

def calcular_risco_fornecedor(tamanho_amostra, itens_aceitos, taxa_defeitos_aceitaveis):
    # Calcular o risco do fornecedor (probabilidade de rejeitar injustamente um lote aceitável)
    risco_fornecedor = 1 - binom.cdf(itens_aceitos, tamanho_amostra, taxa_defeitos_aceitaveis)
    return risco_fornecedor

def calcular_risco_consumidor(tamanho_amostra, itens_aceitos, taxa_defeitos_inaceitaveis):
    # Calcular o risco do consumidor (probabilidade de aceitar injustamente um lote inaceitável)
    risco_consumidor = binom.cdf(itens_aceitos, tamanho_amostra, taxa_defeitos_inaceitaveis)
    return risco_consumidor

def main():
    # Solicitar ao usuário os valores de entrada
    tamanho_lote = st.number_input("Informe o tamanho do lote (N): ")
    tamanho_amostra = st.number_input("Informe o tamanho da amostra (n): ")
    itens_aceitos = st.number_input("Informe o número de itens aceitáveis (a): ")
    taxa_defeitos_aceitaveis = st.number_input("Informe a taxa de defeitos aceitável (NQA) (0 a 1): ")
    numero_lotes = st.number_input("Informe o número de lotes: ")
    custo_unitario = st.number_input("Informe o custo unitário: R$ ")
    custo_lote_rejeitado = st.number_input("Informe o custo de deslocamento por lote rejeitado: R$ ")
    taxa_defeitos = st.number_input("Informe o histórico da taxa de defeituosos do fornecedor (0 a 1): ")
    taxa_defeitos_inaceitaveis = st.number_input("Informe a taxa de defeitos inaceitável (PTDL) (0 a 1): ")

    # Calcular a probabilidade de aceitação (NQA e Real do Fornecedor)
    taxa_aceitacao = calcular_probabilidade_aceitacao(tamanho_amostra, itens_aceitos, taxa_defeitos)
    taxa_aceitacao_NQA = calcular_probabilidade_aceitacao(tamanho_amostra, itens_aceitos,taxa_defeitos_aceitaveis)

    # Calcular a probabilidade do fornecedor ter um lote injustamente reprovado
    taxa_injustamente_rejeitada = (1 - taxa_aceitacao)
    taxa_injustamente_rejeitada_NQA = (1- taxa_aceitacao_NQA)

    # Calcular o ITM
    ITM = calcular_ITM(tamanho_lote, tamanho_amostra, taxa_aceitacao)

    # Calcular o custo de inspeção
    custo_inspecao = numero_lotes * ITM * custo_unitario

    # Calcular o custo de deslocamento
    custo_deslocamento = numero_lotes * custo_lote_rejeitado * (1 - taxa_aceitacao)

    # Calcular o custo total
    custo_total = custo_inspecao + custo_deslocamento

    # Calcular o risco do fornecedor
    risco_fornecedor = calcular_risco_fornecedor(tamanho_amostra, itens_aceitos, taxa_defeitos_aceitaveis)

    # Calcular o risco do consumidor
    risco_consumidor = calcular_risco_consumidor(tamanho_amostra,itens_aceitos, taxa_defeitos_inaceitaveis)


    # Exibir os resultados
    st.writhe(f"")
    st.writhe(f"A probabilidade de aceitação real (fornecedor) do lote é: {taxa_aceitacao:.4f}")
    st.writhe(f"A probabilidade de rejeição injusta do lote do fornecedor é: {taxa_injustamente_rejeitada:.4f}")
    st.writhe(f"A probabilidade de aceitação desejado do lote é: {taxa_aceitacao_NQA:.4f}")
    st.writhe(f"A probabilidade de rejeição injusta do lote do fornecedor é: {taxa_injustamente_rejeitada_NQA:.4f}")
    st.writhe(f"O ITM (Índice de Tamanho do Lote) é: {ITM:.2f}")
    st.writhe(f"O custo de inspeção é: R$ {custo_inspecao:.2f}")
    st.writhe(f"O custo de deslocamento é: R$ {custo_deslocamento:.2f}")
    st.writhe(f"O custo total é: R$ {custo_total:.2f}")
    st.writhe(f"O risco do consumidor (aceitação injusta) com um lote (PTML: {taxa_defeitos_inaceitaveis}) é: {risco_consumidor:.4f}")


if __name__ == "__main__":
    main()
