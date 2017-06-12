import sys
from colorama import init
from termcolor import *

init()

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
    print(cor + texto + RESET, end="")

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
    if(extras == []):
        return "";

    elemento = extras.pop(0);
    return elemento +" "+ concatenarExtras(extras);

def adicionar(descricao, extras):
    # não é possível adicionar uma atividade que não possui descrição.
    if descricao == '':
        return False
    else:
        novaAtividade = descricao + concatenarExtras([x for x in extras]);

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
    if(len(char) == 1):
        if (ord(char) >= ord('A') and ord(char) <= ord('Z')) or (ord(char) >= ord('a') and ord(char) <= ord('z')):
            return True;

    return False;

# Valida a prioridade.
def prioridadeValida(tokens,i):
    if(i == len(tokens)):
        return "";

    if len(tokens[i]) == 3:
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

def auxiliarLeituraPrioridades(tokens,i):

    if i == len(tokens):
        return tokens;

    if(len(tokens[i]) == 3):
        if(tokens[i][0] == '[' and prioridadeLetraValida(tokens[i][1]) and tokens[i][2] == ']'):
            s = '('+tokens[i][1]+')'
            tokens[i] = s;

    return auxiliarLeituraPrioridades(tokens,i+1);

#Retornará uma lista de tuplas
def organizar(linhas,leitura):
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

        if (leitura):
            tokens = auxiliarLeituraPrioridades(tokens, 0);

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

#Deixando o dicionario como global
dicionario = {};

def numerando(itens):
    i = 1;

    for x in itens:
        dicionario[x] = i;

        i = i + 1;

    return dicionario;

#Auxiliando na filtragem
def checagem(tupla_lista,filtro):

    if tupla_lista == []:
        return False;

    if(prioridadeLetraValida(filtro)):
        if(tupla_lista[0] == '('+filtro+')'):
            return True;
    else:
        if(tupla_lista[0] == filtro):
            return True;

    tupla_lista.pop(0);
    return checagem(tupla_lista,filtro);


def imprimindo(dicionario,itens,filtro):
    for tupla in itens:
        if(filtro != ""):
            #Checando se algum elemento de extras corresponde ao filtro
            if(not checagem([x for x in (y for y in tupla[1])],filtro)):
                continue;
        if (tupla[1][2] == "(A)"):
            COR = BOLD+RED;
        elif(tupla[1][2] == "(B)"):
            COR = GREEN;
        elif(tupla[1][2] == "(C)"):
            COR = BLUE;
        elif(tupla[1][2] == "(D)"):
            COR = CYAN;
        else:
            COR = RESET;

        #imprimindo o número que está no dicionario
        #relacão entre uma tupla e um inteiro
        printCores(str(dicionario[tupla])+" ",COR);

        if(tupla[1][2] != ""):
            printCores(tupla[1][2]+" ",COR);

        if(tupla[1][0] != ""):
            printCores(tupla[1][0][0]+tupla[1][0][1]+"/"+tupla[1][0][2]+tupla[1][0][3]+"/"+tupla[1][0][4]+tupla[1][0][5]+tupla[1][0][6]+tupla[1][0][7]+" ",COR);
        if(tupla[1][1] != ""):
            printCores(tupla[1][1][0]+tupla[1][1][1]+"h"+tupla[1][1][2]+tupla[1][1][3]+"m"+" ",COR);
        printCores(tupla[0]+" ",COR);
        if(tupla[1][3] != ""):
            printCores(tupla[1][3]+" ",COR);
        if(tupla[1][4] != ""):
            printCores(tupla[1][4]+" ",COR);
        print();

def listar(filtro):
    fp = open(TODO_FILE, 'r');

    #Recebendo itens da função Organizar
    itens = organizar(fp.readlines(),True);

    # Numerando com a ajuda de dicionarios
    dicionario = numerando(itens);

    #Ordenacao dos Itens
    itens = ordenarPorPrioridade(itens);
    ordenarPorDataHora(itens);
    #Ordenacao dos Itens

    #Imprimindo na tela
    imprimindo(dicionario,itens,filtro);

    fp.close();

#Verifica se a data1 e menor que data2
def dataMenor(data1,data2):
    if(data1 == "" and data2 != ""):
        return -1;
    elif(data1 != "" and data2 == ""):
        return 1;
    elif(data1 == "" and data2 == ""):
        return 0;
    elif(int(data1[4]+data1[5]+data1[6]+data1[7]) < int(data2[4]+data2[5]+data2[6]+data2[7])):
        return 1;
    elif(int(data1[4] + data1[5] + data1[6] + data1[7]) == int(data2[4] + data2[5] + data2[6] + data2[7])):
        if(int(data1[2]+data1[3]) < int(data2[2]+data2[3])):
            return 1;
        elif (int(data1[2] + data1[3]) == int(data2[2] + data2[3])):
            if(int(data1[0]+data2[1]) < int(data2[0]+data2[1])):
                return 1;
            elif(int(data1[0]+data2[1]) == int(data2[0]+data2[1])):
                return 0;

    return -1;

#Verifica se a hora1 e menor que hora2
def horaMenor(hora1,hora2):
    if(hora1 == "" and hora2 != ""):
        return -1;
    elif(hora1 != "" and hora2 == ""):
        return 1;
    elif(hora1 == "" and hora2 == ""):
        return 0;
    if(int(hora1[0]+hora1[1]) < int(hora2[0]+hora2[1])):
        return 1;
    elif (int(hora1[0] + hora1[1]) == int(hora2[0] + hora2[1])):
        if(int(hora1[2]+hora1[3]) < int(hora2[2]+hora2[3])):
            return 1;
        if (int(hora1[2] + hora1[3]) == int(hora2[2] + hora2[3])):
            return 0;

    return -1;


def swap(item1,item2):

    aux = item1;
    item1 = item2;
    item2 = aux;

    return item1,item2;

#Baseado no Selection Sort
#Supoe-se que os itens ja foram ordenados por prioridade
'''
============================
OBS: Esta funcao NAO retornara algo!!!
===========================
'''
def ordenarPorDataHora(itens):

    i = 0;
    while(i < len(itens)-1):
        j = i + 1;
        while(j < len(itens)):
            if(itens[i][1][2] == itens[j][1][2]):
                if(dataMenor(itens[i][1][0],itens[j][1][0]) == 0):
                    if(horaMenor(itens[i][1][1],itens[j][1][1]) == -1):
                        itens[i],itens[j] = swap(itens[i],itens[j]);
                if(dataMenor(itens[i][1][0],itens[j][1][0]) == -1):
                    itens[i],itens[j] = swap(itens[i],itens[j]);
            j = j + 1;

        i = i + 1;

#Baseado em QuickSort
def ordenarPorPrioridade(itens):

    if len(itens) == 0:
        return itens;

    pivo = itens[len(itens)//2];

    if(pivo[1][2] == ""):
        p = " ";
    else:
        p = pivo[1][2][1];

    maiores = [];
    menores = [];
    iguais = [];
    SemPrioridade = [];

    for x in itens:
        if(x[1][2] == ""):
            SemPrioridade.append(x);
        elif(ord(x[1][2][1]) > ord(p)):
            maiores.append(x);
        elif(ord(x[1][2][1]) < ord(p)):
            menores.append(x);
        elif(ord(x[1][2][1]) == ord(p)):
            iguais.append(x);

    return ordenarPorPrioridade(menores) + iguais + ordenarPorPrioridade(maiores) + SemPrioridade;

def fazerAuxiliar(dicionario,num):
    g = open(ARCHIVE_FILE,"a");

    encontrou = False;

    for key,value in dicionario.items():
        if(int(value) == int(num)):
            g.write(key[0] + concatenarExtras([x for x in key[1]]));
            g.write('\n');
            encontrou = True;

    if (not encontrou):
        printCores("Nao foi possivel encontrar uma atividade com o numero dado!\n", CYAN);

    g.close();

def fazer(num):

    f = open(TODO_FILE,"r");

    backup = f.readlines();

    itens = organizar(backup,True);

    dicionario = numerando(itens);

    f.close();

    '''Jogando para a funcao remover Remover do arquivo todo.txt'''
    remover(num);

    fazerAuxiliar(dicionario,num);

def removerAuxiliar(dicionario,num):
    g = open(TODO_FILE,"w");

    encontrou = False;

    for key,value in dicionario.items():
        #print(key,value);
        if (int(value) != int(num)):
            g.write(key[0] + concatenarExtras([x for x in key[1]]));
            g.write("\n");
        else:
            encontrou = True;

    if(not encontrou):
        printCores("Nao foi possivel encontrar uma atividade com o numero dado!\n",CYAN);
    g.close();

def remover(num):

    f = open(TODO_FILE,"r");

    #Salvando arquivo na memoria
    backup = f.readlines();

    #transformando em tuplas
    itens = organizar(backup,True);

    #Numerando e salvando em um dicionario
    dicionario = numerando(itens);

    f.close();

    removerAuxiliar(dicionario,num);


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'.

def priorizar_auxiliar(dicionario,num,p):
    g = open(TODO_FILE,"w");

    encontrou = False;

    for key,value in dicionario.items():
        if(int(value) != int(num)):
            g.write(key[0] + concatenarExtras([x for x in key[1]]));
            g.write('\n');
        else:
            g.write(key[0] + key[1][0] + " " + key[1][1] + " " + p + " " + key[1][3] + key[1][4]);
            g.write('\n');
            encontrou = True;

    if (not encontrou):
        printCores("Nao foi possivel modificar uma atividade com o numero dado!\n", CYAN);

    g.close();

def priorizar(num, p):

    f = open(TODO_FILE,"r");

    backup = f.readlines();

    itens = organizar(backup,True);

    dicionario = numerando(itens);

    #imprimindo(dicionario,itens);

    f.close();

    priorizar_auxiliar(dicionario,num,p);


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos.


#Verificando o comando de remover
def verificar(comando):
    s = ""

    for x in comando:
        s = s + x;

    if(soDigitos(s)):
        return int(s);
def toString(comando):
    if(comando == []):
        return "";

    elemento = comando.pop(0);
    return elemento + toString(comando);
def processarComandos(comandos):

    if comandos[1] == ADICIONAR:
        comandos.pop(0)  # remove 'agenda.py'
        comandos.pop(0)  # remove 'adicionar'

        itemParaAdicionar = organizar([' '.join(comandos)],False)[0]

        # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
        adicionar(itemParaAdicionar[0], itemParaAdicionar[1])  # novos itens não têm prioridade
    elif comandos[1] == LISTAR:
        comandos.pop(0) #remove 'agenda.py'
        comandos.pop(0) #remove 'listar'

        listar(toString(comandos));

    elif comandos[1] == REMOVER:
        comandos.pop(0) #remove 'agenda.py'
        comandos.pop(0) #remove 'remover'

        if(verificar(comandos) != -1):
            remover(verificar(comandos));

    elif comandos[1] == FAZER:
        comandos.pop(0) #remove 'agenda.py'
        comandos.pop(0) #remove 'fazer;

        if(verificar(comandos) != -1):
            fazer(verificar(comandos));

    elif comandos[1] == PRIORIZAR:
        comandos.pop(0) #remove 'agenda.py';
        comandos.pop(0) #remove 'priorizar'

        priorizar(comandos[0],comandos[1]);

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