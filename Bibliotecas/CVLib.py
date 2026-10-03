# === | BIBLIOTECAS NATIVAS | ===

import time
import os
import random
import re
import sys
import calendar
import locale
import subprocess
import socket

from enum import Enum
from pathlib import Path
from tkinter import filedialog, Tk, messagebox
from datetime import datetime
from collections.abc import Mapping

# === | BIBLIOTECAS EXTERNAS | ===

# INSTALAR BIBLIOTECAS EXTERNAS!

def InstalarAtualizarPip(modoOculto=False):
    if(getattr(sys, 'frozen', False)):
        return
    pip = subprocess.Popen([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
    for linha in pip.stdout:
        if(modoOculto):
            continue
        if('already satisfied' in linha):
            continue
        print(linha, end='')
        
def InstalarAtualizarBiblio(*bibliotecas,modoOculto=False,pre=False):
    if(getattr(sys, 'frozen', False)):
        return
    if(not bibliotecas):
        return

    argumentos = [sys.executable,'-m', 'pip', 'install', '--upgrade']
    argumentos.append('--pre') if pre else None
    argumentos.extend(bibliotecas)

    processo = subprocess.Popen(argumentos,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
    for linha in processo.stdout:
        if(modoOculto):
            continue
        if('already satisfied' in linha):
            continue
        print(linha, end='')

InstalarAtualizarPip()
InstalarAtualizarBiblio("tzlocal", "requests", "num2words", "colorama", "python-dotenv","ruamel.yaml")

import requests

from num2words import num2words
from colorama import Back, Fore, Style
from tzlocal import get_localzone
from dotenv import set_key, dotenv_values
from ruamel.yaml import YAML


try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'portuguese_brazil')

yaml = YAML(typ="rt")
yaml.preserve_quotes = True
yaml.allow_duplicate_keys = True
yaml.allow_unicode = True
yaml.width = 4096

class Style_Extra:
    ITALICO = "\033[3m"

class formatacaoData(Enum):
    BRUTA = 1
    FORMATADA = 2
    FORMAL = 3
    SEPARADO = 4

def DiretorioAtual(completo=False):
    if getattr(sys, 'frozen',False):
        return os.path.dirname(sys.executable) if not completo else sys.executable
    else:
        return os.path.dirname(os.path.abspath(sys.argv[0])) if not completo else os.path.abspath(sys.argv[0])
    
def DataAtual(formatacao=formatacaoData.BRUTA):
    try:
        fh = get_localzone()
        dataHora = datetime.now(fh)
        match formatacao:
            case formatacaoData.BRUTA:
                return dataHora
            case formatacaoData.FORMATADA:
                return dataHora.strftime('%d/%m/%Y')
            case formatacaoData.FORMAL:
                return f"{dataHora.day} de {calendar.month_name[dataHora.month].title()} de {dataHora.year}"
            case formatacaoData.SEPARADO:
                return dataHora.day, dataHora.month, dataHora.year
    except:
        return None
    
def FusoHorario(formatar=True):
    try:
        fh = get_localzone()
        dataHora = datetime.now(fh)
        horaFormatada = dataHora.strftime('%H:%M:%S')
        if(not formatar):
            return horaFormatada.split(':')
        return horaFormatada
    except:
        return None

def MensagemDeConsole(mensagem, tipo=0,titulo=""):
    corMensagem = ['\033[0m', '\033[0m']
    tipoMensagem = ''
    match tipo:
        case 0: 
            corMensagem[0] = Fore.GREEN
            corMensagem[1] = Back.GREEN
            tipoMensagem = 'SUCESSO'
        case 1:
            corMensagem[0] = Fore.YELLOW
            corMensagem[1] = Back.YELLOW
            tipoMensagem = 'AVISO'
        case 2:
            corMensagem[0] = Fore.RED
            corMensagem[1] = Back.RED
            tipoMensagem = 'FALHA'
        case 3:
            corMensagem[0] = Fore.WHITE
            corMensagem[1] = Back.BLACK
            tipoMensagem = 'INFO'

    titulo = f"{corMensagem[1]}{Style.BRIGHT}[{titulo}]{Style.RESET_ALL}: " if len(titulo) > 0 else ""
    rotulo = f"{corMensagem[0]}{Style.BRIGHT}{tipoMensagem} > {Style.RESET_ALL}" if len(tipoMensagem) > 0 else ""
    mensagem = f"{corMensagem[0]}'{Style_Extra.ITALICO}{mensagem}{corMensagem[0]}{Style_Extra.ITALICO}'{Style.RESET_ALL}"

    print(f"{titulo}{rotulo}{mensagem.strip()}{Style.RESET_ALL}\n")
    
class tipoDeMensagem(Enum):
    INFO = 1
    SUCESSO = 2
    AVISO = 3
    FALHA = 4

def MensagemDeConsolePro(mensagem, tipo=tipoDeMensagem.SUCESSO,titulo="CONSOLE",horario=False,data=False,pularLinha=False,prefixoRotulo="",prefixoMensagem="",retornarMensagem=False):
    corMensagem = ['\033[0m', '\033[0m']
    tipoMensagem = ''
    match tipo:
        case _ if tipo == tipoDeMensagem.SUCESSO or tipo == 0:
            corMensagem[0] = Fore.GREEN
            corMensagem[1] = Back.GREEN
            tipoMensagem = 'SUCESSO'
        case _ if tipo == tipoDeMensagem.AVISO or tipo == 1:
            corMensagem[0] = Fore.YELLOW
            corMensagem[1] = Back.YELLOW
            tipoMensagem = 'AVISO'
        case _ if tipo == tipoDeMensagem.FALHA or tipo ==  2:
            corMensagem[0] = Fore.RED
            corMensagem[1] = Back.RED
            tipoMensagem = 'FALHA'
        case _ if tipo == tipoDeMensagem.INFO or tipo == 3:
            corMensagem[0] = Fore.WHITE
            corMensagem[1] = Back.BLACK
            tipoMensagem = 'INFO'

    dataAtual = f"{Style.DIM}{DataAtual(formatacaoData.FORMAL)}{Style.RESET_ALL} | " if data else ""
    horarioAtual = f"{Style.DIM}{FusoHorario(formatar=True)}{Style.RESET_ALL} | " if horario else ""
    
    inicio = f"{Style.BRIGHT}✿ 「{corMensagem[1]} {titulo} {Style.RESET_ALL}{Style.BRIGHT}」✿  " if len(titulo) > 0 else ""
    rotulo = f"\n╰┈➤  {prefixoRotulo+Style.RESET_ALL}{dataAtual+horarioAtual+Style.RESET_ALL}"
    f"{corMensagem[0]}{Style.BRIGHT}{tipoMensagem} ➤  {Style.RESET_ALL}" if len(tipoMensagem) > 0 else ""

    pulo = f"\n{" "*2}╰ " if pularLinha else ""
    reticencias = [f"{corMensagem[0]}⌞{Fore.RESET}",f"{corMensagem[0]}⌝{Fore.RESET}"]

    estiloPadraoMensagem = f"{Style.RESET_ALL}{Style.BRIGHT}"

    mensagem = f"{Style.BRIGHT}{pulo}{reticencias[0]} ❛{prefixoMensagem}{mensagem}{estiloPadraoMensagem}❜{reticencias[1]}"
    mensagemFinal = (f"{inicio}{rotulo}{mensagem.strip()}{Style.RESET_ALL}\n")
    if(retornarMensagem):
        return mensagemFinal
    print(mensagemFinal)
    
def ObterENV(arquivoEnv, criarSeNaoExistir=True):
    if(not os.path.exists(arquivoEnv)):
        if(criarSeNaoExistir):
            with open(arquivoEnv, 'w') as env:
                MensagemDeConsolePro(f"O Arquivo '{arquivoEnv}' NÃO Existe e foi Criado Automaticamente!",tipoDeMensagem.AVISO)
        else:
            MensagemDeConsolePro(f"O Arquivo '{arquivoEnv}' NÃO Existe!",tipoDeMensagem.FALHA)
            return None
    return dotenv_values(arquivoEnv)

def LerVarENV(variaveisEnv,chaveBuscada,chavePadrao=None):
    if(not variaveisEnv or not chaveBuscada):
        return chavePadrao or None
    else:
        return variaveisEnv.get(chaveBuscada,chavePadrao)
    
def AlterarVarENV(novoValor,chaveBuscada,arquivoEnv,reticencias=False):
    set_key(arquivoEnv,chaveBuscada,novoValor,quote_mode="always" if reticencias else "never")

def LerArquivoYML(dirYML,criarSeNaoExistir=True):
    if(not dirYML or len(dirYML) < 1):
        MensagemDeConsolePro(f"O Diretório '{dirYML}' NÃO é VÁLIDO!",tipoDeMensagem.FALHA)
        return
    nomeArquivoYML = os.path.basename(dirYML)
    if(not os.path.exists(dirYML)):
        if(criarSeNaoExistir):
            with open(dirYML,mode="w",encoding="utf-8") as yml:
                MensagemDeConsolePro(f"O Arquivo '{nomeArquivoYML}' NÃO Existe e foi Criado Automaticamente!",tipoDeMensagem.AVISO)
        else:
            MensagemDeConsolePro(f"O Arquivo '{nomeArquivoYML}' NÃO Existe!",tipoDeMensagem.FALHA)
            return 
    try:
        with open(dirYML ,"r", encoding="utf-8") as arq:
            dados = yaml.load(arq)
            if(dados):
                return dados
            else:
                return {}
    except Exception as e:
        MensagemDeConsolePro(f"O Arquivo '{nomeArquivoYML}' NÃO Pôde ser LIDO!\nErro: {type(e)}: {e}",tipoDeMensagem.FALHA)

def LerDadosYML(dadosYML,*caminho, dadoPadrao=None, argumentos=None):
    if(isinstance(dadosYML, Mapping)):
        dados = dadosYML
    elif(isinstance(dadosYML,(str,os.PathLike))):
        dados = LerArquivoYML(dadosYML)

    if(not isinstance(dados, Mapping)):
        return dadoPadrao

    for chave in caminho:
        if(not isinstance(dados, Mapping)):
            return dadoPadrao

        dados = dados.get(chave)

        if(dados is None):
            return dadoPadrao

    dadosEncontrados = []

    def ProcessarTipo(dado):
        if isinstance(dado,str):
            return dado.format(**(argumentos or {}))
        return dado
    if isinstance(dados,list):
        for i in dados:
            dadosEncontrados.append(ProcessarTipo(i))
        return dadosEncontrados[0] if len(dadosEncontrados) == 1 else dadosEncontrados

    return ProcessarTipo(dados)

def SalvarArquivoYML(dados, dir):
    if(not dados or not dir):
        return
    try:
        with open(dir ,"w", encoding="utf-8") as arq:
            yaml.dump(dados,arq)
    except Exception as e:
        MensagemDeConsolePro(f"O Arquivo {os.path.basename(dir)} NÃO Pôde ser ALTERADO!\nErro: {type(e)}: {e}",tipoDeMensagem.FALHA)

def ModificarDadosYML(dadosYML,*caminho, valor):
    if(dadosYML is None or not caminho): 
        return
    modificandoArquivo = False
    if(isinstance(dadosYML, Mapping)):
        dadosObtidos = dadosYML
    else:
        dadosObtidos = LerArquivoYML(dadosYML)
        if(dadosObtidos is None or not isinstance(dadosObtidos,Mapping)):
            dadosObtidos = {}
        modificandoArquivo = True

    dadosRaiz = dadosObtidos
    
    for chave in caminho[:-1]:
        if(chave not in dadosObtidos or dadosObtidos[chave] is None):
            dadosObtidos[chave] = {}
        if(not isinstance(dadosObtidos[chave],Mapping)):
            return
        dadosObtidos = dadosObtidos[chave]

    chaveFinal = caminho[-1]

    if(chaveFinal not in dadosObtidos or dadosObtidos[chaveFinal] is None):
        dadosObtidos[chaveFinal] = valor

    elif(isinstance(dadosObtidos[chaveFinal],list)):
        if(not isinstance(valor,list)):
            if(valor not in dadosObtidos[chaveFinal]):
                dadosObtidos[chaveFinal].append(valor)
        else:
            dadosObtidos[chaveFinal] = valor
    else:
        dadosObtidos[chaveFinal] = valor

    if(modificandoArquivo):
        SalvarArquivoYML(dadosRaiz,dadosYML)

def SalvarArquivo(titulo="Salvar Como...",extensaoDoArq=".txt",tiposDeArq=("Arquivos de Texto", "*.txt"),dirInicial=DiretorioAtual(),nomeInicial=""):
    dirArq = filedialog.asksaveasfilename(title=titulo,defaultextension=extensaoDoArq,filetypes=(tiposDeArq,("Todos os Arquivos", "*.*")),initialdir=dirInicial,initialfile=nomeInicial)
    if(dirArq):
        return dirArq

def EscolherArquivo(titulo="Selecione um Arquivo...",tiposDeArq=("Arquivos de Texto", "*.txt"),dirInicial=DiretorioAtual(),multiplosArquivos=False):

    arq = filedialog.askopenfilename(title=titulo,filetypes=(tiposDeArq,("Todos os Arquivos", "*.*")),
                                    initialdir=dirInicial) if not multiplosArquivos else filedialog.askopenfilenames(title=titulo,
                                                                                                                     filetypes=(tiposDeArq,("Todos os Arquivos", "*.*")))
    if(arq):
        return arq
    
def EscolherDiretorio(titulo="Selecione um Diretório..",dirInicial=DiretorioAtual()):
    dir = filedialog.askdirectory(title=titulo,mustexist=True) if not dirInicial else filedialog.askdirectory(title=titulo,mustexist=True,initialdir=dirInicial)
    if(dir):
        return dir

def Delay(t=1):
    time.sleep(t)

def Limpar():
    os.system('cls')

def Espaco(qtd=1):
    print(f"{'\n'*qtd}", end='')

def MenuOpcoes(*opcoes,desc=[],titulo="OPÇÕES",corTitulo=Back.RED,corNumeros=Back.RED):
    print(f"{(f'『{corTitulo}..:'+titulo.upper()+f':..{Style.RESET_ALL}』').center(50,'=')}\n")
        
    contagemAteEspaco = 0
    for i, opcao in enumerate(opcoes):
        try:
            descricao = desc[i]
        except:
            descricao = ""

        espacoAposLinha = ""
        contagemAteEspaco += 1
        if contagemAteEspaco % 2 == 0:
            espacoAposLinha = " "*4

        print(f"{espacoAposLinha}｢{corNumeros} {i+1} \033[0m｣ | \033[3;40m'{opcao}'\033[0m")
        print(f'{" "*8}{espacoAposLinha}{Style_Extra.ITALICO}"{descricao}"') if descricao else None
        print(Style.RESET_ALL)

def Write(frase, tempo=0.05):
    asni_regex = re.compile(r'\033\[[0-9;]*m')
    m_frase = frase.replace('\r' or '\n', '')

    chars = asni_regex.split(m_frase)
    asnis = asni_regex.findall(m_frase)

    f_frase = []
    for i, char in enumerate(chars):
        f_frase.append(('texto',char))
        if i < len(asnis):
            f_frase.append(('asni',asnis[i]))

    for i, str in f_frase:
        if str == "ansi":
            print(f"{str}",end='',flush=True)
        else:
            for i, char in enumerate(str):
                print(f"{char}", end='', flush=True)
                Delay(tempo)
    print(Style.RESET_ALL,end='')

def EvilWrite(frase="Não me especificaram uma frase, então eu de fato estou puto.", tempo=0.05):
    def MandarFraseCorrupta(f,t):
        chars = len(f)
        fundoV = '\033[40;31;1m'
        corV = '\033[41;30;3m'
        fraseAlt = [f.upper(), f.lower()]
        btd_ch = 0
        for char in range(0, chars):
            bi = random.randint(0,1)
            print(f"{(fundoV, corV)[bi]}{(fraseAlt[bi])[char]}{Style.RESET_ALL}", end='', flush=True)
            btd_ch += 1
            Delay(t)

    if(isinstance(frase,list)):
        for i, f in enumerate(frase):
            MandarFraseCorrupta(f,tempo)
            Espaco()
    else:
        MandarFraseCorrupta(frase,tempo)

def FormatarTempo(tempo,origem="SEGUNDOS",desc=False,modo="TEXTO"):
    match origem:
        case "SEGUNDOS":
            tempoUsuario = tempo
        case "MINUTOS":
            tempoUsuario = tempo * 60
        case "HORAS":
            tempoUsuario = tempo * 3600
            
    def Format(t,tipo):
        formato = ""
        match tipo:
            case "Horas":
                formato = "Horas" if t > 1 else "Hora"
            case "Minutos":
                formato = "Minutos" if t > 1 else "Minuto"
            case "Segundos":
                formato = "Segundos" if t > 1 else "Segundo"
        return f"{t} {formato}"

    minutos, segundos = divmod(int(tempoUsuario),60)
    horas, minutos = divmod(minutos,60)

    match modo:
        case "HH:MM:SS":
            return horas, minutos, segundos
        case "TEXTO":
            if (not desc):
                if(horas > 0):
                    cronometro = '{:02d}:{:02d}:{:02d}'.format(horas, minutos, segundos)
                elif(minutos > 0):
                    cronometro = '{:02d}:{:02d}'.format(minutos, segundos)
                else:
                    cronometro = '{:02d}'.format(segundos)
                return cronometro
            else:
                cronometro = []
                if(horas > 0):
                    cronometro.append(Format(horas,"Horas"))
                if(minutos > 0):
                    cronometro.append(Format(minutos,"Minutos"))
                if(segundos > 0):
                    cronometro.append(Format(segundos,"Segundos"))
                if(len(cronometro) == 1):
                    return cronometro[0]
                
                if len(cronometro) == 0:
                    return "0"

                cronometroDescritivo = ", ".join(cronometro[:-1]) + " e " + cronometro[-1]
                return cronometroDescritivo
            
def ConverterEmUnidadeLite(tempo=0, origem="SEGUNDOS",modo="MINUTOS",converterParaInt=False):
    tempoConvertido = float(0)
    match origem:
        case "SEGUNDOS":
            tempoUsuario = tempo
        case "MINUTOS":
            tempoUsuario = tempo * 60
        case "HORAS":
            tempoUsuario = tempo * 3600
            
    match modo:
        case "SEGUNDOS":
            tempoConvertido = tempoUsuario
        case "MINUTOS":
            tempoConvertido = tempoUsuario / 60
        case "HORAS":
            tempoConvertido = tempoUsuario / 3600
        case "AUTO":
            if tempoUsuario < 60:
                tempoConvertido = tempoUsuario
            elif tempoUsuario < 3600:
                tempoConvertido = tempoUsuario / 60
            else:
                tempoConvertido = tempoUsuario / 3600

    if tempoConvertido.is_integer() or converterParaInt:
        return(int(tempoConvertido))
    else:
        return tempoConvertido
            
def ConverterEmUnidadePro(horas=0, minutos=0, segundos=0, modo="SEGUNDOS",converterParaInt=False):
    tempoConvertido = float(0)
    match modo:
        case "SEGUNDOS":
            tempoConvertido = (horas * 3600) + (minutos * 60) + segundos
        case "MINUTOS":
            tempoConvertido = (horas * 60) + minutos + (segundos / 60)
        case "HORAS":
            tempoConvertido = horas + (minutos / 60) + (segundos / 3600)

    if tempoConvertido.is_integer() or converterParaInt:
        return(int(tempoConvertido))
    else:
        return tempoConvertido
    
def ConverterNumerosEmPalavras(numero, tipoOrdinal=False, idiomaDesejado="pt-br"):
    try:
        return str(num2words(numero,lang=idiomaDesejado,ordinal=tipoOrdinal))
    except:
        return "X"
    
def BinaryFill(vezes,corUm=Fore.RED,corDois=Back.RED,tempo=0.1):
    opcao_cor = [Style.BRIGHT+corUm, Style.BRIGHT+corDois, Style.RESET_ALL]
    linha = 0
    while(vezes > 0):
        linha += 1
        if(linha >= 40):
            print("\n", end='')
            linha = 0
        print(f"{opcao_cor[random.randint(0,1)]}{random.randint(0,1)}{opcao_cor[2]}", end="", flush=True)
        vezes -= 1
        Delay(tempo)
    print(Style.RESET_ALL)

def BinaryWriteAndFill(frase,corUm=Fore.RED,corDois=Back.RED,tempo=0.1):
    writeCors = [f"{Style_Extra.ITALICO}{corUm}", f"{Style.BRIGHT}{corDois}", "\033[0m"]
    chars = len(frase)
    char = 0
    linha = 0
    while(char < chars):
        linha += 1
        if(linha >= 40):
            print("\n", end='')
            linha = 0
        prob = random.randint(0,100)
        if(prob <= 20):
            print(f"{writeCors[1]}{frase[char]}{writeCors[2]}", end="", flush=True)
            char += 1
            print(f"{writeCors[0]}{random.randint(0,1)}{writeCors[2]}", end="", flush=True)
        else:
            print(f"{writeCors[0]}{random.randint(0,1)}{writeCors[2]}", end="", flush=True)
        Delay(tempo)
    print(Style.RESET_ALL)

def MensagemPersonagem(texto="Eu vou assumir uma frase aleatória,\npois esqueceram de me instruir o que dizer.",
                       nomePerso="Cherry Violet",corPerso="\033[45m",simboloPerso="☪️",t=0.05):
    Write(f'{simboloPerso} ',t)
    Write(f'{corPerso}'+'['+'\033[1m'+nomePerso+'\033[0m'+f'{corPerso}'+']',t)
    Write(f': {simboloPerso}',t)
    Espaco()
    Write(f"\033[3;40m{'"'}{texto}{Style.RESET_ALL}\033[3;40m{'"'}",t)
    Espaco()

def Creditos():
    MensagemPersonagem("Script By:  Blossom 🌙.","Cherry Violet","\033[45m","☪️")

def LerOpcao(opcoes=1,desc="Opção Escolhida"):
    mensagemOpcaoInvalida = "A Opção Escolhida NÃO ESTÁ DISPONÍVEL!"
    mensagemErroDigitacao = "A Opção NÃO foi INFORMADA ou é INVÁLIDA!"
    quantidadeDeErros = 0

    def LidarComErros(mensagem="ERRO DESCONHECIDO!",quantidadeAtualDeErros=0):
        Espaco(1)
        if(quantidadeAtualDeErros != 5):
            MensagemDeConsole(mensagem,2)
        else:
            BinaryFill(20)
            Espaco(1)
            MensagemPersonagem("...")
            Espaco(1)
            MensagemPersonagem("...LEIA...")
            Espaco(1)
            MensagemPersonagem("... A TELA!..")
            Espaco(2)

    while True:
        try:
            opcaoEscolhida = int(input(f"{Style.BRIGHT}「 {Back.BLACK} {desc} \033[39;49m 」{Style.RESET_ALL}:\n{Style.BRIGHT}>>{Style.RESET_ALL} "))
            if opcaoEscolhida >= 1 and opcaoEscolhida <= opcoes:
                return opcaoEscolhida
            else:
                quantidadeDeErros += 1
                LidarComErros(mensagemOpcaoInvalida,quantidadeDeErros)
                continue
        except:
            quantidadeDeErros += 1
            LidarComErros(mensagemErroDigitacao,quantidadeDeErros)
            continue

def LerInput(tipo=1,desc="Digite Aqui"):
    while True:
        inputDigitado = input(f"{Style.BRIGHT}「 {Back.BLACK} {desc} \033[39;49m 」{Style.RESET_ALL}:\n{Style.BRIGHT}>>{Style.RESET_ALL} ")
        if(not inputDigitado):
            MensagemDeConsole("NADA foi Informado!",2)
            continue
        match tipo:
            case 1: # Input do Tipo String
                return(inputDigitado)
            case 2: # Input do Tipo Número (Inteiro)
                try:
                    return int(inputDigitado)
                except:
                    MensagemDeConsole("Digite um Número VÁLIDO!",2)
                    continue
            case 3: # Input do Tipo Número (Float)
                try:
                    return float(inputDigitado)
                except:
                    MensagemDeConsole("Digite um Número VÁLIDO!",1)
                    continue

def ProcessarPastaDeDados(origem="",nomeDaPasta="",aceitarPastaNova=False):
    caminhoParaPasta = os.path.join(origem,nomeDaPasta)
    def ChecarExistencia():
        return os.path.exists(caminhoParaPasta)
    
    novaPastaFalhou = False
    while not ChecarExistencia():
        Limpar()
        MensagemDeConsolePro(f"A Pasta Data NÃO Pôde Ser Encontrada!",
                             tipoDeMensagem.FALHA) if not novaPastaFalhou else MensagemDeConsolePro(f"A Pasta Data Substituta NÃO Pôde Ser Gerada!",tipoDeMensagem.FALHA)
        Delay(2)
        if(aceitarPastaNova and not novaPastaFalhou):
            MensagemDeConsolePro(f"Gerando uma Nova...",tipoDeMensagem.AVISO)
            Delay(2)
            Path.mkdir(caminhoParaPasta,exist_ok=True)
            novaPastaFalhou = True
            continue
        Delay(1)
        sys.exit()
        break
    Limpar()
    return os.path.abspath(caminhoParaPasta)

def CriarPasta(diretorioDesejado=""):
    if(os.path.exists(diretorioDesejado)):
        return os.path.abspath(diretorioDesejado)
    diretorioParaCriar = os.path.abspath(diretorioDesejado)
    Path.mkdir(diretorioParaCriar,exist_ok=True)
    return diretorioParaCriar if os.path.exists(diretorioParaCriar) else None

def TestarConexaoAInternet(tentativas=3,tempoLimite=3,log=False):
    MensagemDeConsolePro("Testando Conexão à Internet...",tipoDeMensagem.AVISO) if log else None
    for tentativa in range(tentativas):
        Delay(0.1)
        MensagemDeConsolePro(f"{tentativa}ª Tentativa...",tipoDeMensagem.AVISO) if tentativa > 1 and log else None
        try:
            socket.create_connection(("8.8.8.8",53),tempoLimite)
            MensagemDeConsolePro("Teste De Conexão à Internet BEM-Sucedido!") if log else None
            return True
        except Exception:
            pass
    MensagemDeConsolePro(f"O Teste de Conexão à Internet FALHOU {f"Após {ConverterNumerosEmPalavras(tentativas)} Tentativas" if tentativas > 0 else ""}!",
                         tipoDeMensagem.FALHA) if log else None
    return False

TestarConexaoAInternet()