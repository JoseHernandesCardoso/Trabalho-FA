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
#   - Pontos
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
# onde cada linha do arquivo é um elemento de uma lista de str. 
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
class Time:
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
    linha('-=', 40)
    print(' '*10 + 'TABELA DO BRASILEIRÃO' + ' '*10)
    linha('-=', 40)
    # 1 - Tabela
    times = define_times(jogos)
    exibe_tabela(times)
    linha('-', 40)
    # 2 - Melhor aproveitamento como anfitrião
    times_melhor_aprv = melhor_aproveitamento(times, 0)
    aprv = calc_aproveitamento(times_melhor_aprv[0])
    print('O(s) time(s) com o melhor aproveitamento jogando como anfitrião foi(ram):')
    lista_nomes(times_melhor_aprv)
    print('Com ' + porcento(aprv) + ' de aproveitamento.')
    linha('-', 40)
    # 3 - Defesa menos vazada
    times_menos_vazada = menos_vazada(times, 0)
    print('O(s) time(s) com a(s) defesa(s) menos vazada(s) foi(ram):')
    lista_nomes(times_menos_vazada)
    print('Recebendo apenas ' + str(times_menos_vazada[0].gols_sofridos) + \
          ' gols ao longo do campeonato')


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

def define_times(jogos: list[str]) -> list[Time]:
    '''
    Define os times participantes e seus desempenhos em uma série de *jogos*

    Exemplos:
    >>> jogos = ['Palmeiras 2 Flamengo 1', 'Bota-Fogo 0 Santos 0',
    ... 'Santos 0 Palmeiras 3', 'Flamengo 2 Bota-Fogo 1']
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
        dados = separa_no_espaco(jogo)
        # dados = [nome_anf, gols_anf, nome_vis, gols_vis]
        # Cria ou atualiza time anfitrião
        atualiza_time(times=times,
                      nome=dados[0],
                      marcados=int(dados[1]),
                      sofridos=int(dados[3]),
                      anfitriao=True)
        # Cria ou atualiza time vizitante
        atualiza_time(times=times,
                      nome=dados[2],
                      marcados=int(dados[3]),
                      sofridos=int(dados[1]),
                      anfitriao=False)
    return times

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

def atualiza_time(times: list[Time], nome: str, marcados: int, \
                  sofridos: int, anfitriao: bool):
    '''
    Atualiza o desempenho de um time dentro de *times*, dado seu *nome*,
    gols *marcados*, gols *sofridos*, se teve a *vitoria* e se foi o
    *anfitriao* da partida.

    Se o time não for encontrado em *times*, ele será criado e adicionado
    ao final da lista.
    '''
    saldo = marcados - sofridos
    vitoria = False
    pontos = 0
    if saldo > 0:
        pontos = 3
        vitoria = True
    elif saldo == 0:
        pontos = 1
    
    i = procura_indice_time(nome, times)
    if i == -1:
        times.append(Time(
            nome= nome,
            vitorias= int(vitoria),
            pontuacao= pontos,
            saldo_gols= saldo,
            gols_sofridos= sofridos,
            jogos_anfitriao= int(anfitriao),
            pontos_anfitriao= pontos*int(anfitriao),
        ))
    else:
        times[i].vitorias = times[i].vitorias + int(vitoria)
        times[i].pontuacao = times[i].pontuacao + pontos
        times[i].saldo_gols = times[i].saldo_gols + saldo
        times[i].gols_sofridos = times[i].gols_sofridos + sofridos
        times[i].jogos_anfitriao = times[i].jogos_anfitriao + int(anfitriao)
        times[i].pontos_anfitriao = times[i].pontos_anfitriao + pontos*int(anfitriao)
    

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

def exibe_tabela(times: list[Time]):
    '''
    Exibe uma tabela com cada time dentro de *times*. A tabela exibe nome,
    pontuação, vitórias e saldo de gols de cada time, nesta ordem. As colunas
    adaptam sua largura de acordo com o tamanho do maior elemento contido nela.
    A tabela já ordena os times de acordo com sua classificação.

    Exemplo:
    >>> times = [
    ... Time(nome='Palmeiras', vitorias=3, pontuacao=6, saldo_gols=4, gols_sofridos=1,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Bota-Fogo', vitorias=0, pontuacao=1, saldo_gols=-1, gols_sofridos=2,
    ... jogos_anfitriao=1, pontos_anfitriao=1),
    ... Time(nome='Santos', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=3,
    ... jogos_anfitriao=1, pontos_anfitriao=0),
    ... Time(nome='Vasco', vitorias=1, pontuacao=4, saldo_gols=1, gols_sofridos=2,
    ... jogos_anfitriao=2, pontos_anfitriao=3),
    ... Time(nome='Flamengo', vitorias=2, pontuacao=4, saldo_gols=0, gols_sofridos=3,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Atletico-Madrid', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=4,
    ... jogos_anfitriao=0, pontos_anfitriao=0)]
    >>> exibe_tabela(times)
    ___________________________________
    TIME            | PTS | VIT | SGOLS
    ===================================
    Palmeiras       |   6 |   3 |     4
    Flamengo        |   4 |   2 |     0
    Vasco           |   4 |   1 |     1
    Bota-Fogo       |   1 |   0 |    -1
    Atletico-Madrid |   1 |   0 |    -3
    Santos          |   1 |   0 |    -3
    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    '''
    ordem_classificacao(times)
    # Encontra o tamanho ideal para cada coluna
    # Os tamanhos mínimos servem para comportar o nome da coluna
    maior_nome = 4
    maior_ponto = maior_vitoria = 3
    maior_saldo = 5
    for time in times:
        if maior_nome < len(time.nome):
            maior_nome = len(time.nome)

        if maior_ponto < len(str(time.pontuacao)):
            maior_ponto = len(str(time.pontuacao))

        if maior_vitoria < len(str(time.vitorias)):
            maior_vitoria = len(str(time.vitorias))

        if maior_saldo < len(str(time.saldo_gols)):
            maior_saldo = len(str(time.saldo_gols))
    tam_total = maior_nome + maior_ponto + maior_vitoria + maior_saldo + 9
    # Exibe tabela
    linha('_', tam_total)
    print('TIME' + ' '*(maior_nome - 4) + ' |',
          'PTS' + ' '*(maior_ponto - 3) + ' |',
          'VIT' + ' '*(maior_vitoria - 3) + ' |',
          'SGOLS')
    linha('=', tam_total)
    for time in times:
        espaco_nome = ' '*(maior_nome - len(time.nome))
        espaco_ponto = ' '*(maior_ponto - len(str(time.pontuacao)))
        espaco_vitoria = ' '*(maior_vitoria - len(str(time.vitorias)))
        espaco_saldo = ' '*(maior_saldo - len(str(time.saldo_gols)))
        print(time.nome + espaco_nome + ' |',
              espaco_ponto + str(time.pontuacao) + ' |',
              espaco_vitoria + str(time.vitorias)+ ' |',
              espaco_saldo + str(time.saldo_gols))
    linha('‾', tam_total)

def ordem_classificacao(times: list[Time]):
    '''
    Modifica *times* ordenando eles de acordo com suas classificações.
    A ordem de classificação é feita de acordo com a pontuação de cada time.
    Em caso de empate, ganha o time com mais vitórias. Em caso de outro empate,
    ganha o time com melhor saldo de gols. Em caso de mais um empate, o critério
    final é a ordem alfabética do nome dos times.
    '''
    for i in range(len(times)):
        for j in range(i+1, len(times)):
            j_mais_pontos = times[j].pontuacao > times[i].pontuacao
            desempate1 = (times[j].pontuacao == times[i].pontuacao
                          and times[j].vitorias > times[i].vitorias)
            desempate2 = (times[j].pontuacao == times[i].pontuacao
                          and times[j].vitorias == times[i].vitorias
                          and times[j].saldo_gols > times[i].saldo_gols)
            desempate3 = (times[j].pontuacao == times[i].pontuacao
                          and times[j].vitorias == times[i].vitorias
                          and times[j].saldo_gols == times[i].saldo_gols
                          and times[j].nome < times[i].nome)
            if j_mais_pontos or desempate1 or desempate2 or desempate3:
                aux = times[i]
                times[i] = times[j]
                times[j] = aux

def melhor_aproveitamento(times: list[Time], i: int) -> list[Time]:
    '''
    Retorna os times com melhor aproveitamento jogando como anfitrião dentro 
    de *times* a partir do indice *i*. O aproveitamento é a razão entre número
    máximo de pontos possíveis e pontos feitos. Se *i > len(times)-1*, será considerado
    apenas o último elemento da lista, da mesma forma que em *i == len(times) - 1*

    Exemplo:
    >>> times = [
    ... Time(nome='Palmeiras', vitorias=3, pontuacao=6, saldo_gols=4, gols_sofridos=1,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Bota-Fogo', vitorias=0, pontuacao=1, saldo_gols=-1, gols_sofridos=2,
    ... jogos_anfitriao=1, pontos_anfitriao=1),
    ... Time(nome='Santos', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=3,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Vasco', vitorias=1, pontuacao=4, saldo_gols=1, gols_sofridos=2,
    ... jogos_anfitriao=2, pontos_anfitriao=3),
    ... Time(nome='Flamengo', vitorias=2, pontuacao=4, saldo_gols=0, gols_sofridos=3,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Atletico-Madrid', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=4,
    ... jogos_anfitriao=0, pontos_anfitriao=0)]
    >>> melhor_aproveitamento(times, 0) # doctest: +NORMALIZE_WHITESPACE
    [Time(nome='Palmeiras', vitorias=3, pontuacao=6, saldo_gols=4, gols_sofridos=1,
    jogos_anfitriao=1, pontos_anfitriao=3),
    Time(nome='Santos', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=3,
    jogos_anfitriao=1, pontos_anfitriao=3),
    Time(nome='Flamengo', vitorias=2, pontuacao=4, saldo_gols=0, gols_sofridos=3,
    jogos_anfitriao=1, pontos_anfitriao=3)]
    '''
    if  i >= len(times) - 1:
        melhores = [times[len(times) - 1]]
    else:
        melhores_frente = melhor_aproveitamento(times, i+1)
        if calc_aproveitamento(times[i]) > calc_aproveitamento(melhores_frente[0]):
            melhores = [times[i]]
        elif calc_aproveitamento(times[i]) < calc_aproveitamento(melhores_frente[0]):
            melhores = melhores_frente
        else:
            melhores = [times[i]] + melhores_frente
    return melhores
   
def calc_aproveitamento(time: Time) -> float:
    '''
    Calcula o aproveitamento do *time* nos jogos em que ele jogou como anfitrião
    '''
    aproveitamento = 0.0
    if time.jogos_anfitriao != 0:
        aproveitamento = time.pontos_anfitriao/(time.jogos_anfitriao*3)
    return aproveitamento

def porcento(n: float) -> str:
    '''
    Transforma *n* em porcentagem para exibição.
    A porcentagem tem, no máximo, duas casas decimais.

    Exemplos:
    >>> porcento(1.0)
    '100.0%'
    >>> porcento(0.65)
    '65.0%'
    >>> porcento(0.725242)
    '72.52%'
    '''
    return str(round(n*100, 2)) + '%'

def menos_vazada(times: list[Time], i: int) -> list[Time]:
    '''
    Retorna os times com as defesas menos vazadas em *times* a partir
    do indice *i*. Um time tem sua defesa considerada como a menos vazada
    se tiver a menor quantidade de gols sofridos ao longo do campeonato.
    Se *i > len(times)-1* será considerada apens o último elemento da lista,
    assim como em *i == len(times)-1*.
    Exemplo:
    >>> times = [
    ... Time(nome='Palmeiras', vitorias=3, pontuacao=6, saldo_gols=4, gols_sofridos=1,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Bota-Fogo', vitorias=0, pontuacao=1, saldo_gols=-1, gols_sofridos=2,
    ... jogos_anfitriao=1, pontos_anfitriao=1),
    ... Time(nome='Santos', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=3,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Vasco', vitorias=1, pontuacao=4, saldo_gols=1, gols_sofridos=1,
    ... jogos_anfitriao=2, pontos_anfitriao=3),
    ... Time(nome='Flamengo', vitorias=2, pontuacao=4, saldo_gols=0, gols_sofridos=3,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Atletico-Madrid', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=4,
    ... jogos_anfitriao=0, pontos_anfitriao=0)]
    >>> menos_vazada(times, 0) # doctest: +NORMALIZE_WHITESPACE
    [Time(nome='Palmeiras', vitorias=3, pontuacao=6, saldo_gols=4, gols_sofridos=1,
    jogos_anfitriao=1, pontos_anfitriao=3),
    Time(nome='Vasco', vitorias=1, pontuacao=4, saldo_gols=1, gols_sofridos=1,
    jogos_anfitriao=2, pontos_anfitriao=3)]
    '''
    if i >= len(times) - 1:
        menos = [times[len(times) - 1]]
    else:
        menos_frente = menos_vazada(times, i+1)
        if times[i].gols_sofridos < menos_frente[0].gols_sofridos:
            menos = [times[i]]
        elif times[i].gols_sofridos > menos_frente[0].gols_sofridos:
            menos = menos_frente
        else:
            menos = [times[i]] + menos_frente
    return menos

def linha(estilo: str, tamanho: int):
    '''
    Exibe uma linha do tipo *estilo* com o dado *tamanho* de caracteres.

    Exemplos:
    >>> linha('*', 10)
    **********
    >>> linha('-=', 5)
    -=-=-
    '''
    linha = ''
    while len(linha) != tamanho:
        linha = linha + estilo[len(linha)%len(estilo)]
    print(linha)

def lista_nomes(times: list[Time]):
    '''
    Lista o nome de cada time em *times*

    Exemplos
    >>> times = [
    ... Time(nome='Palmeiras', vitorias=3, pontuacao=6, saldo_gols=4, gols_sofridos=1,
    ... jogos_anfitriao=1, pontos_anfitriao=3),
    ... Time(nome='Bota-Fogo', vitorias=0, pontuacao=1, saldo_gols=-1, gols_sofridos=2,
    ... jogos_anfitriao=1, pontos_anfitriao=1),
    ... Time(nome='Santos', vitorias=0, pontuacao=1, saldo_gols=-3, gols_sofridos=3,
    ... jogos_anfitriao=1, pontos_anfitriao=3)]
    >>> lista_nomes(times)
        - Palmeiras
        - Bota-Fogo
        - Santos
    '''
    for t in times:
        print('    - ' + t.nome)


if __name__ == '__main__':
    main()