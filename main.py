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
from dataclasses import dataclass

@dataclass
class Jogo():
    '''
    Representação do resultado de um jogo de futebol
    *gols_anfitriao* e *gols_visitante* são iguais ou maiores que zero
    '''
    anfitriao: str
    gols_anfitriao: int
    visitante: str
    gols_visitante: int

@dataclass
class Time():
    '''
    Representação das estatísticas de um time de futebol em um campeonato
    Todos os valores int são maiores ou iguais a zero
    '''
    nome: str
    vitorias: int
    pontuacao: int
    saldo_gols: int
    gols_sofridos: int
    jogos_anfitriao: int
    pontos_anfitriao: int


def main():
    if len(sys.argv) < 2:
        print('Nenhum nome de arquivo informado.')
        sys.exit(1)
    if len(sys.argv) > 2:
        print('Muitos parâmetro. Informe apenas um nome de arquivo.')
        sys.exit(1)
    jogos = le_arquivo(sys.argv[1])
    converte_jogos(jogos)
    times = define_times(jogos)

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

def converte_jogos(jogos: list[str]):
    '''
    Modifica *jogos* convertendo cada elemento para o tipo Jogo().

    Exemplos:
    >>> rodada1 = ['Palmeiras 2 Flamengo 1', 'Bota-Fogo 0 Santos 0']
    >>> rodada2 = ['Santos 0 Palmeiras 3', 'Flamengo 2 Bota-Fogo 1']
    >>> converte_jogos(rodada1)
    >>> rodada1 # doctest: +NORMALIZE_WHITESPACE
    [Jogo(anfitriao='Palmeiras', gols_anfitriao=2, visitante='Flamengo', gols_visitante=1), 
    Jogo(anfitriao='Bota-Fogo', gols_anfitriao=0, visitante='Santos', gols_visitante=0)]

    >>> converte_jogos(rodada2)
    >>> rodada2 # doctest: +NORMALIZE_WHITESPACE
    [Jogo(anfitriao='Santos', gols_anfitriao=0, visitante='Palmeiras', gols_visitante=3),
    Jogo(anfitriao='Flamengo', gols_anfitriao=2, visitante='Bota-Fogo', gols_visitante=1)]
    '''
    for i in range(len(jogos)):
        dados = separa_no_espaco(jogos[i])
        jogos[i] = Jogo(anfitriao=dados[0], gols_anfitriao=int(dados[1]),
                        visitante=dados[2], gols_visitante=int(dados[3]))

def separa_no_espaco(string: str) -> list[str]:
    '''
    Separa a *string* em strings menores onde tiver espaço em branco (' ').
    Retorna uma lista dessas strings menores na mesma ordem de palavas da *string*

    Exemplos:
    >>> separa_no_espaco('')
    []
    >>> separa_no_espaco('Python')
    ['Python']
    >>> separa_no_espaco('Hello World!')
    ['Hello', 'World!']
    >>> separa_no_espaco('Escreva uma string')
    ['Escreva', 'uma', 'string']
    '''
    separado = []
    palavra = ''
    for i in range(len(string)):
        if string[i] != ' ':
            palavra = palavra + string[i]
            if i == len(string) - 1:
                separado.append(palavra)
        else:
            separado.append(palavra)
            palavra = ''
    return separado

def define_times(jogos: list[Jogo]) -> list[Time]:
    '''
    Define os times participantes e seus desempenhos em uma série de *jogos*

    Exemplos:
    >>> jogos = [
    ... Jogo(anfitriao='Palmeiras', gols_anfitriao=2, visitante='Flamengo', gols_visitante=1),
    ... Jogo(anfitriao='Bota-Fogo', gols_anfitriao=0, visitante='Santos', gols_visitante=0),
    ... Jogo(anfitriao='Santos', gols_anfitriao=0, visitante='Palmeiras', gols_visitante=3),
    ... Jogo(anfitriao='Flamengo', gols_anfitriao=2, visitante='Bota-Fogo', gols_visitante=1)
    ... ]
    >>> define_times(jogos) # doctest: +NORMALIZE_WHITESPACE
    [Time(nome='Palmeiras', vitorias=2, pontuacao=6, saldo_gols=4, gols_sofridos=1,
    jogos_anfitriao=1, pontos_anfitriao=3),
    Time(nome='Flamengo', vitorias=1, pontuacao=3, saldo_gols=0, gols_sofridos=3,
    jogos_anfitriao=1, pontos_anfitriao=3),
    Time(nome='Bota-Fogo', vitorias=0, pontuacao=1, saldo_gols=-1, gols_sofridos=2,
    jogos_anfitriao=1, pontos_anfitriao=1),
    Time(nome='Santos', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=3,
    jogos_anfitriao=1, pontos_anfitriao=0)]
    '''
    times: list[Time] = []
    for jogo in jogos:
        # Coletando estatisticas do jogo
        vitorias_anf = vitorias_vis = 0
        pontuacao_anf = pontuacao_vis = 0
        if jogo.gols_anfitriao > jogo.gols_visitante:
            vitorias_anf = 1
            pontuacao_anf = 3
        elif jogo.gols_anfitriao == jogo.gols_visitante:
            pontuacao_anf = pontuacao_vis = 1
        else:
            vitorias_vis = 1
            pontuacao_vis = 3
        # Atualizando ou criando (caso não exista) time anfitrião
        i = procura_indice_time(jogo.anfitriao, times)
        if i != -1:
            times[i].vitorias = times[i].vitorias + vitorias_anf
            times[i].pontuacao = times[i].pontuacao + pontuacao_anf
            times[i].saldo_gols = times[i].saldo_gols + jogo.gols_anfitriao - jogo.gols_visitante
            times[i].gols_sofridos = times[i].gols_sofridos + jogo.gols_visitante
            times[i].jogos_anfitriao = times[i].jogos_anfitriao + 1
            times[i].pontos_anfitriao = times[i].pontos_anfitriao + pontuacao_anf
        else:
            times.append(Time(
                nome= jogo.anfitriao,
                vitorias= vitorias_anf,
                pontuacao= pontuacao_anf,
                saldo_gols= jogo.gols_anfitriao - jogo.gols_visitante,
                gols_sofridos= jogo.gols_visitante,
                jogos_anfitriao= 1,
                pontos_anfitriao= pontuacao_anf))
        # Atualizando ou criando (caso não exista) time visitante
        i = procura_indice_time(jogo.visitante, times)
        if i != -1:
            times[i].vitorias = times[i].vitorias + vitorias_vis
            times[i].pontuacao = times[i].pontuacao + pontuacao_vis
            times[i].saldo_gols = times[i].saldo_gols + jogo.gols_visitante - jogo.gols_anfitriao
            times[i].gols_sofridos = times[i].gols_sofridos + jogo.gols_anfitriao
        else:
            times.append(Time(
                nome= jogo.visitante,
                vitorias= vitorias_vis,
                pontuacao= pontuacao_vis,
                saldo_gols= jogo.gols_visitante - jogo.gols_anfitriao,
                gols_sofridos= jogo.gols_anfitriao,
                jogos_anfitriao= 0,
                pontos_anfitriao= 0))    
    return times

def procura_indice_time(nome: str, times: list[Time]) -> int:
    '''
    Retorna o indice de um time dentro de *times* dado o seu *nome*

    Retorna -1 se o time não estiver em *times*
    '''
    indice_time = -1
    i = 0
    while i < len(times) and indice_time == -1:
        if times[i].nome == nome:
            indice_time = i
        i = i + 1
    return indice_time


if __name__ == '__main__':
    main()