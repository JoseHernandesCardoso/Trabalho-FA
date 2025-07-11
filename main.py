# ANÁLISE:
# Com base em um arquivo de texto (resultados.txt) que possui os resultados de diversos
# jogos em um campeonato de futebol, cumprir 3 objetivos: 
#    1- Definir a tabela de classificação dos times em um campeonato de futebol
#    2- Definir o(s) melhor(es) time(s) com o melhor aproveitamento jogando como anfitrião(ões)
#    3- Definir o(s) time(s) com a defesa menos vazada
#
# Cada linha do arquivo representa o jogo da seguinte forma:
#   *time anfitrião* *gols do anfitrião* *time visitante* *gols do visitante*
# Os espaços nos nomes dos times foram substituidos por traveções ("-").
#
# Objetivo 1:
# A classificação dos times é feita de acordo com a pontuação de cada um.
# A pontuação é definida de acordo com o resultado de cada jogo:
#   - Vitória: +3 pontos
#   - Empate:  +1 ponto
#   - Derrota:  0 pontos
# Em casos de empate, os critérios para desempatar são, respectivamente:
#   - Número de vitórias
#   - Saldo de gols (marcados menos sofridos)
#   - Ordem alfabética do nome dos times
# A exibição da classificação deve ser em formato de tabela (do primeiro ao último
# colocado) com colunas contendo, respectivamente:
#   - Nome do time
#   - Vitórias
#   - Saldo de gols 
# A formatação de cada coluna da tabela deve se adaptar ao tamanho do maior elemento dela
# 
# Objetivo 2:
# O aproveitamento de um time é um valor da razão entre a máxima pontuação possível e
# a pontuação feita por um time. Neste caso, considerar apenas a pontuação máxima e feita
# do time quando jogou como anfitrião.
# A pontuação máxima será o número de jogos como anfitrião multiplicado por 3 (pontuação
# de vitória).
# A exibição desse valor deve ser feita em forma de porcentagem.
# 
# Objetivo 3: 
# O time com a "defesa menos vazada" é aquele que sofreu a menor quantidade de gols ao longo
# de todo o campeonato e considerando todos os jogos.
# 
# 
# TIPOS DE DADOS:
# Os dados do arquivo resultados.txt serão armazenados em uma lista
# onde cada linha do arquivo é o elemento de uma lista de str. Cada
# string será convertida em um tipo composto Jogo() que contém:
#   - Anfitrião (str)
#   - Gols do anfitrião (int >= 0)
#   - Visitante (str)
#   - Gols do visitante (int >= 0) 
#  
# Cada time será representado por um tipo composto Time() que contem:
#   - Nome (str)
#   - Vitorias (int >= 0)
#   - Pontuação (int >= 0)
#   - Saldo de gols (int)
#   - Gols sofridos (int >= 0)
#   - Jogos como anfitrião (int >=0)
#   - Pontos como anfitrião (int >= 0)
# 
# Os times serão agrupados em uma lista de Time

import sys

def main():
    if len(sys.argv) < 2:
        print('Nenhum nome de arquivo informado.')
        sys.exit(1)
    if len(sys.argv) > 2:
        print('Muitos parâmetro. Informe apenas um nome de arquivo.')
        sys.exit(1)
    jogos = le_arquivo(sys.argv[1])
    # TODO: solução da pergunta 1
    # TODO: solução da pergunta 2
    # TODO: solução da pergunta 3

def le_arquivo(nome: str) -> list[str]:
    '''
    Lê o conteúdo do arquivo *nome* e devolve uma lista onde cada elemento
    representa uma linha.
    Por exemplo, se o conteúdo do arquivo for
    Sao-Paulo 1 Atletico-MG 2
    Flamengo 2 Palmeiras 1
    a resposta produzida é
    [‘Sao-Paulo 1 Atletico-MG 2’, ‘Flamengo 2 Palmeiras 1’]
    '''
    try:
        with open(nome) as f:
            return f.readlines()
    except IOError as e:
        print(f'Erro na leitura do arquivo "{nome}": {e.errno} - {e.strerror}.');
        sys.exit(1)

if __name__ == '__main__':
    main()