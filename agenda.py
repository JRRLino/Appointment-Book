import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'


# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor):
    print(cor + texto + RESET)


# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z,
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração.


def concatenarExtras(extras):
    s = "";
    for x in extras:
        if(x != '' and x != ' '):
            s = s + " " + x;

    return s;

def adicionar(descricao, extras):
    # não é possível adicionar uma atividade que não possui descrição.
    if descricao == '':
        return False
    else:
        novaAtividade = descricao + concatenarExtras(extras);

    # Escreve no TODO_FILE.
    try:
        # Abre o arquivo no modo Append
        fp = open(TODO_FILE, 'a')

        # Escreve sobre o arquivo uma novaAtividade
        fp.write(novaAtividade + "\n")

        fp.close()
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return False

    return True


# Valida a letra da contida na prioridade
def prioridadeLetraValida(char):
    if (ord(char) >= ord('A') and ord(char) <= ord('Z')) or (ord(char) >= ord('a') and ord(char) <= ord('z')):
        return True;

    return False;


# Valida a prioridade.
def prioridadeValida(tokens,i):
    print(tokens);

    if(i == len(tokens)):
        return "";

    if len(tokens[i]) == 3:
        print("Encontrado!",tokens[i]);
        if(tokens[i][0] == '(' and prioridadeLetraValida(tokens[i][1]) and tokens[i][2] == ')'):
            return tokens[i];

    return prioridadeValida(tokens,i+1);

def HoradoisPrimeiros(horaMin):
    inteiro = int(horaMin[0] + horaMin[1]);

    if (inteiro >= 0 and inteiro <= 23):
        return True;
    return False;


def HoradoisUltimos(horaMin):
    inteiro = int(horaMin[2] + horaMin[3]);

    if (inteiro >= 00 and inteiro <= 59):
        return True;

    return False;


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(tokens,i):

    if i == len(tokens):
        return "";

    if len(tokens[i]) == 4 and soDigitos(tokens[i]) and HoradoisPrimeiros(tokens[i]) and HoradoisUltimos(tokens[i]):
        return tokens[i];

    return horaValida(tokens,i+1);


# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto.

def DataMesValido(data):
    soma = int(data[2] + data[3]);

    if (soma >= 0 and soma <= 12):
        return True;

    return False;


def DataDiaValido(data):
    soma = int(data[0] + data[1]);

    if (soma >= 0 and soma <= 30):
        if (soma == 30 and data[2] + [3] == "02"):
            return False;
        return True;

    return False;


def dataValida(tokens,i):

    if(i == len(tokens)):
        return "";

    if len(tokens[i]) == 8 and soDigitos(tokens[i]) and DataDiaValido(tokens[i]) and DataMesValido(tokens[i]):
        return tokens[i]

    return dataValida(tokens,i+1);


# Valida que o string do projeto está no formato correto.
def projetoValido(tokens,i):

    if(i == len(tokens)):
        return "";

    if len(tokens[i]) >= 2 and tokens[i][0] == '+':
        return tokens[i];

    return projetoValido(tokens,i+1);


# Valida que o string do contexto está no formato correto.
def contextoValido(tokens,i):

    if(i == len(tokens)):
        return "";

    if len(tokens[i]) >= 2 and tokens[i][0] == '@':
        return tokens[i];

    return contextoValido(tokens,i+1);


# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero):
    if type(numero) != str:
        return False
    for x in numero:
        if x < '0' or x > '9':
            return False
    return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.
def TokensToString(tokens):
    if (tokens == []):
        return "";

    elemento = tokens.pop(0);
    return elemento + " " + TokensToString(tokens);

def find(array,index,elemento):

    if(index == len(array)):
        return -1;

    if(array[index] == elemento):
        return index;

    return find(array,index+1,elemento);

#Retornará uma lista de tuplas
def organizar(linhas):
    itens = []

    for l in linhas:
        data = ''
        hora = ''
        pri = ''
        desc = ''
        contexto = ''
        projeto = ''

        l = l.strip()  # remove espaços em branco e quebras de linha do começo e do fim
        tokens = l.split()  # quebra o string em palavras

        # Processa os tokens um a um, verificando se são as partes da atividade.
        # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
        # na variável data e posteriormente removido a lista de tokens. Feito isso,
        # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
        # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
        # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
        # corresponde à descrição. É só transformar a lista de tokens em um string e
        # construir a tupla com as informações disponíveis.

        # Checando prioridade
        if (prioridadeValida(tokens,0) != ""):
            pri = prioridadeValida(tokens,0);
            tokens.pop(find(tokens,0,pri));

        # Checando data
        if (dataValida(tokens,0) != ""):
            data = dataValida(tokens,0);
            tokens.pop(find(tokens,0,data));

        # Checando hora
        if (horaValida(tokens,0) != ""):
            hora = horaValida(tokens,0);
            tokens.pop(find(tokens,0,hora));

        # Checando Projeto
        if (projetoValido(tokens,0) != ""):
            projeto = projetoValido(tokens,0);
            tokens.pop(find(tokens,0,projeto));

        # Checando Contexto
        if (contextoValido(tokens,0) != ""):
            contexto = contextoValido(tokens,0);
            tokens.pop(find(tokens,0,contexto));

        desc = TokensToString(tokens);

        itens.append((desc, (data, hora, pri, contexto, projeto)))

    return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados).
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém.
def listar():
    fp = open(TODO_FILE, 'r');

    itens = organizar(fp.readlines());

    print("Desordenada: ",itens);

    itens = ordenarPorPrioridade(itens);

    print("Ordenada:", itens);

def ordenarPorDataHora(itens):
    ################ COMPLETAR

    return itens

def ordenarPorPrioridade(itens):
    ordenada = [];

    while(itens != []):
        i = 0;
        maior_index = -1;
        maior_pri = '(Z)';

        for (desc,(data,hora,pri,contexto,projeto)) in itens:
            if len(pri) == 3:
                if ord(pri[1]) < ord(maior_pri[1]):
                    maior_pri = pri;
                    maior_index = i;
            i = i + 1;

        ordenada.append(itens[maior_index]);
        itens.pop(maior_index);

    return ordenada;

def fazer(num):
    ################ COMPLETAR

    return "";

def remover():
    ################ COMPLETAR

    return "";


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'.
def priorizar(num, prioridade):
    ################ COMPLETAR

    return "";


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos.
def processarComandos(comandos):
    # print(comandos);

    if comandos[1] == ADICIONAR:
        comandos.pop(0)  # remove 'agenda.py'
        comandos.pop(0)  # remove 'adicionar'
        itemParaAdicionar = organizar([' '.join(comandos)])[0]

        print(itemParaAdicionar)

        # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
        adicionar(itemParaAdicionar[0], itemParaAdicionar[1])  # novos itens não têm prioridade
    elif comandos[1] == LISTAR:
        listar();

        ################ COMPLETAR

    elif comandos[1] == REMOVER:
        return

        ################ COMPLETAR

    elif comandos[1] == FAZER:
        return

        ################ COMPLETAR

    elif comandos[1] == PRIORIZAR:
        return

        ################ COMPLETAR

    else:
        print("Comando inválido.")


# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)