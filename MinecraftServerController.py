# IMPORTE A BIBLIOTECA: pip install mcstatus, mcrcon, psutil, dotenv, requests, pyyaml, wakepy & keyboard
# INCLUA O ARQUIVO: CVLib.py na MESMA pasta do Script!

import subprocess, keyboard, threading, queue, os, sys, signal, psutil, random, requests, socket, discord, asyncio, logging, yaml
import CVLib as CV
from wakepy import keep
from mcstatus import JavaServer
from mcrcon import MCRcon
from discord.ext import commands
from dotenv import load_dotenv, set_key, dotenv_values

CV.Limpar()
arquivoEnv = "server_config.env"
arquivoLog = "controller_log.log"
arquivoMensagens = 'mensagens.yml'

logging.basicConfig(filename=arquivoLog,level=logging.INFO,format='%(asctime)s - %(message)s', filemode='a')

logging.getLogger("discord").setLevel(logging.CRITICAL)
logging.getLogger("discord.client").setLevel(logging.CRITICAL)
logging.getLogger("discord.gateway").setLevel(logging.CRITICAL)
logging.getLogger("discord.ext.commands.bot").setLevel(logging.CRITICAL)

def MandarLog(mensagem):
    logging.info(f"{mensagem}")

def MandarAoConsole(msg, tipo=0, log=True):
    if isinstance(msg, list):
        for i, m in enumerate(msg):
            CV.MensagemDeConsole(m,tipo,title="MINE-SERVER")
            if(i < len(msg) - 1):
                CV.Delay(1)
    else:
        CV.MensagemDeConsole(msg,tipo,title="MINE-SERVER")
    # Gravar Mensagem de Console no Arquivo de Logs
    if(log is True):
        MandarLog(f"[TERMINAL]: {tipo}: {msg}")

def LerServerProperties(setting=''):
    try:
        with open('server.properties', 'r') as cfgs:
            linhas = cfgs.readlines()
            for linha in linhas:
                linhaConvertida = linha.replace('\n','').split('=')
                if(setting in linhaConvertida):
                    return linhaConvertida[1] or ''
    except:
        pass

def ModificarServerProperties(setting='',value=''):
    if(len(setting) < 1 or len(value) < 1):
        return
    try:
        with open('server.properties', 'r', encoding='utf-8') as cfgs:
            linhas = cfgs.readlines()
        with open('server.properties', 'r+', encoding='utf-8') as cfgs:
            for linha in linhas:
                    linhaConvertida = linha.replace('\n','').split('=')
                    if(setting in linhaConvertida and linhaConvertida[1] != value):
                        linhaConvertida[1] = value
                        cfgs.write(f"{'='.join(linhaConvertida)}\n")
                    else:
                        cfgs.write(linha)
    except:
        pass

# Checar Existência do Arquivo .env"
if not os.path.isfile(arquivoEnv):
    MandarAoConsole(f"O Arquivo do Servidor '{arquivoEnv}' NÃO Pôde Ser Encontrado!\nGerando um Automático...",2,False)
    try:
        with open(arquivoEnv,'w',encoding='utf-8') as env:
            env.write("""# Nome do Servidor (Padrão: "Mine-Server")
NOMESERV=

# Nome do Arquivo .jar (Padrão: "server.jar")
JAVA=

# Qtd. de RAM a ser Utilizada (Padrão: "4GB / 4096M")
RAM=

# IP p/ Conexão ao RCON (Padrão: IP Do Servidor)
RCONIP=

# Porta p/ Conexão ao RCON (Padrão: "25575")
RCONPORT=

# Senha p/ Login ao RCON (Atribuir no Arquivo 'server.properties')
RCONPASS=
                      
# Porta p/ Conexão ao Query (Padrão: "25565")
QUERYPORT=

# IP do Servidor (Padrão: "localhost")
IPSERVER=

# Porta do Servidor (Padrão: "25565")
PORTSERVER=

# Habilitar/Desabilitar Integração ao Discord (Opções: Yes/No)
DISCOBOT=Yes

# Chave Secreta p/ Acessar o Bot
BOTTOKEN=

# ID do Canal do Servidor p/ Interação do Bot
BOTCHANNEL=

# Nome do Cargo p/ Controlar o Bot Via Comandos
ADMROLE=Adm

# Atalho p/ Iniciar o Servidor
HOTSTART=ctrl+i

# Atalho p/ Fechar o Servidor
HOTSTOP=ctrl+p

# Atalho p/ Forçar o Servidor à Fechar
HOTFSTOP=ctrl+shift+p

# Atalho p/ Reiniciar o Servidor
HOTRESTART=ctrl+r

# Atalho p/ Fechar o Controlador (RECOMENDADO!)
HOTCLOSE=ctrl+l

# NÃO ALTERAR!... <3
SOFTSHUT=Yes""")
    except:
        CV.Limpar()
        MandarAoConsole(f"O Arquivo do Servidor '{arquivoEnv}' NÃO Pôde Ser Gerado!\nO Terminal NÃO Poderá ser Aberto!",2,False)
        keyboard.wait('esc')
        sys.exit()
    CV.Delay(2)
    CV.Limpar()

envVar = dotenv_values(arquivoEnv)
arquivoExecucao = envVar.get('JAVA') or "server.jar"
''
try:
    quantidadeDeRAM = int(envVar.get('RAM'))
except:
    quantidadeDeRAM = 4096

server = None
abrindoFechando = False

nomServidor = envVar.get("NOMESERV") or os.path.basename(os.getcwd()) or "Menu-Servidor"

ipServidor = envVar.get('IPSERVER') or LerServerProperties('server-ip') or 'localhost'
portaServidor = envVar.get('PORTSERVER') or LerServerProperties('server-port') or 25565

portaQuery = envVar.get('QUERYPORT') or LerServerProperties('query.port') or 25565

ipRcon = envVar.get('RCONIP') or ipServidor
portaRcon = envVar.get('RCONPORT') or LerServerProperties('rcon.port') or 25575
senhaRcon = envVar.get('RCONPASS') or LerServerProperties('rcon.password')

set_key(arquivoEnv, "IPSERVER", str(arquivoExecucao), quote_mode="never")

set_key(arquivoEnv, "IPSERVER", str(ipServidor), quote_mode="never")
set_key(arquivoEnv, "PORTSERVER", str(portaServidor), quote_mode="never")

set_key(arquivoEnv, "RCONIP", str(ipRcon), quote_mode="never")
set_key(arquivoEnv, "RCONPORT", str(portaRcon), quote_mode="never")

set_key(arquivoEnv, "RAM", str(quantidadeDeRAM), quote_mode="never")
set_key(arquivoEnv, "JAVA", str(arquivoExecucao), quote_mode="never")
set_key(arquivoEnv, "NOMESERV", str(nomServidor), quote_mode="never")

if senhaRcon is not None:
    set_key(arquivoEnv, "RCONPASS", str(senhaRcon), quote_mode="never")

ModificarServerProperties('enable-rcon','true')
ModificarServerProperties('enable-status','true')
ModificarServerProperties('enable-query','true')

clientJava = None
clientRcon = MCRcon(ipRcon,senhaRcon,int(portaRcon),timeout=10)

mensagens = CV.ObterYML(arquivoMensagens)
if(mensagens is None):
    keyboard.wait('esc')
    sys.exit()  

tempoAutoDesligamento = 60

TOKEN = envVar.get('BOTTOKEN',"")
try:
    canalDoBot = int(envVar.get('BOTCHANNEL'))
except:
    canalDoBot = 0
cargoPermitido = envVar.get('ADMROLE',"Adm")
prefixComandos = '/'

ints = discord.Intents.default()
ints.message_content = True
bot = commands.Bot(command_prefix=prefixComandos, intents=ints,case_insensitive=True)
botIniciado = False
channel = None

def TestarConexaoAoRcon(tentativasMax=5):
    for i in range(tentativasMax):
        if(EstadoServidor() is False):
            return False
        try:
            clientRcon.command('\n')
            return True
        except:
            continue
    return False

def MandarComando(mensagem):
    def ComandoRCON(comando,q):
        resposta = clientRcon.command(comando)
        q.put((resposta,"OK"))
        
    if(TestarConexaoAoRcon() is False):
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Erro-Comunicacao","Console",i=mensagem),2)
        return
    q = queue.Queue()
    threading.Thread(target=ComandoRCON,args=(mensagem,q),daemon=True).start()
    try:
        respostaRCON = q.get(timeout=5)
        respostaServidor, estado = respostaRCON
        if(estado == "OK"):
            logging.info(f"[RCON]: foi Inserido o Comando: '{mensagem}'.")
            if(respostaServidor):
                MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Resposta-Servidor","Console",i=respostaServidor),1)
                return respostaServidor
    except queue.Empty:
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Comando-Timeout","Console-Discord",i=mensagem),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"RCON-Comando-Timeout","Console-Discord",i=mensagem))
    except Exception as e:
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Erro-Generico","Console-Discord",i=mensagem),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"RCON-Erro-Generico","Console-Discord",i=mensagem))

def ConectarRcon(tempoMaximo=140):
    if (EstadoServidor() is False):
            return False
    timeoutEvent = threading.Event()
    def TentativaConexao(q):
        while not timeoutEvent.is_set():
            if(EstadoServidor() is False):
                q.put("FALHA")
                break
            try:
                clientRcon.connect()
                q.put("OK")
                break
            except Exception:
                CV.Delay(1)
                continue
    q = queue.Queue()
    threading.Thread(target=TentativaConexao,args=(q,),daemon=True).start()
    try:
        respostaRCON = q.get(timeout=tempoMaximo)
        if(respostaRCON == "OK"):
            timeoutEvent.set()
            return True
        elif(respostaRCON == "FALHA"):
            return False
    except queue.Empty:
        timeoutEvent.set()
        return False
    return False

def MandarComando(mensagem):
    def ComandoRCON(comando,q):
        resposta = clientRcon.command(comando)
        q.put((resposta,"OK"))
        
    if(TestarConexaoAoRcon() is False):
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Erro-Comunicacao","Console",i=mensagem),2)
        return
    q = queue.Queue()
    threading.Thread(target=ComandoRCON,args=(mensagem,q),daemon=True).start()
    try:
        respostaRCON = q.get(timeout=5)
        respostaServidor, estado = respostaRCON
        if(estado == "OK"):
            logging.info(f"[RCON]: foi Inserido o Comando: '{mensagem}'.")
            if(respostaServidor):
                MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Resposta-Servidor","Console",i=respostaServidor),1)
                return respostaServidor
    except queue.Empty:
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Comando-Timeout","Console-Discord",i=mensagem),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"RCON-Comando-Timeout","Console-Discord",i=mensagem))
    except Exception as e:
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Erro-Generico","Console-Discord",i=mensagem),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"RCON-Erro-Generico","Console-Discord",i=mensagem))

def MandarAoDiscord(mensagem, author=None):
    if(EstadoBot() is False):
        if(envVar["DISCOBOT"] == "Yes" and botIniciado):
            MandarAoConsole(CV.LerDataYML(mensagens,"Falha-Mensagem-Discord","Console"),2)
        return
    if isinstance(mensagem, list):
        for i, msg in enumerate(mensagem):
            asyncio.run_coroutine_threadsafe(send_message(msg,author), bot.loop) if author else asyncio.run_coroutine_threadsafe(send_message(msg), bot.loop)
            if(i < len(mensagem) - 1):
                CV.Delay(3)
    else:
        asyncio.run_coroutine_threadsafe(send_message(mensagem,author), bot.loop) if author else asyncio.run_coroutine_threadsafe(send_message(mensagem), bot.loop)

def MandarAoChat(mensagem):
    if(mensagens is None):
        return
    prefixoChat = CV.LerDataYML(mensagens,"Prefixo-Chat")
    if isinstance(mensagem, list):
        for i, msg in enumerate(mensagem):
            MandarComando(f'tellraw @a "{prefixoChat}{msg}"')
            if(i < len(mensagem) - 1):
                CV.Delay(2)
    else:
        MandarComando(f'tellraw @a "{prefixoChat}{mensagem}"')

def MandarComoTitulo(mensagem):
    if(mensagens is None):
        return
    prefixoTitulo = CV.LerDataYML(mensagens,"Prefixo-Titulo","Comeco"),CV.LerDataYML(mensagens,"Prefixo-Titulo","Final")
    if isinstance(mensagem, list):
        for i, msg in enumerate(mensagem):
            MandarComando(f'title @a title "{prefixoTitulo[0]}{msg.upper()}{prefixoTitulo[1]}"')
            if(i < len(mensagem) - 1):
                CV.Delay(3)
    else:
        MandarComando(f'title @a title "{prefixoTitulo[0]}{mensagem.upper()}{prefixoTitulo[1]}"')

# EVENTOS DO BOT
def ChecarComandoDeUsuario(ctx):
    if(not ctx or ctx.author == bot.user):
        return False
    cargo = discord.utils.get(ctx.guild.roles, name=cargoPermitido)
    if(not cargo or cargo not in ctx.author.roles):
        MandarAoDiscord(CV.LerDataYML(mensagens,"Comando-Sem-Permissao","Console-Discord",i=ctx.author.display_name))
        MandarAoConsole(CV.LerDataYML(mensagens,"Comando-Sem-Permissao","Console-Discord",i=ctx.author.display_name),1)
        return False
    if(ctx.channel.id != canalDoBot):
        MandarAoDiscord(CV.LerDataYML(mensagens,"Comando-Canal-Errado","Console-Discord",i=ctx.author.display_name))
        MandarAoConsole(CV.LerDataYML(mensagens,"Comando-Canal-Errado","Console-Discord",i=ctx.author.display_name),1)
        return False
    return True

def EstadoBot():
    if(bot.is_ready() and not bot.is_closed() and botConectado and channel):
        return True
    return False

def NomeIconeServidor():
    if(EstadoBot()):
        iconeServidor = channel.guild.icon.url
        nomeServidor = channel.guild.name
        if(iconeServidor):
            return nomeServidor,iconeServidor


async def send_message(message,author=None):
    if (EstadoBot() is False and envVar["DISCOBOT"] == "Yes"):
        MandarAoConsole(CV.LerDataYML(mensagens,"Erro-Mensagem-Discord","Console",i=message),2)
        return

    mensagemDiscord = discord.Embed()
    if(author):
        mensagemDiscord.set_author(name=f"[{author[0]}]:",icon_url=author[1])
    else:
        mensagemDiscord.set_author(name=f"[{bot.user.name}]:",icon_url=bot.user.avatar.url)

    mensagemDiscord.title = f"'{bot.user.name}' lhe enviou um recado:"
    mensagemDiscord.description = f'**-** "{message}"'
    mensagemDiscord.color=discord.Color.blurple()
    await channel.send(embed=mensagemDiscord)


botConectado = False 
@bot.event
async def on_disconnect():
    global botConectado
    await asyncio.sleep(5)
    if(not bot.is_closed()):
        return
    MandarAoConsole(CV.LerDataYML(mensagens,"Bot-Perdeu-Conexao","Console"),1)
    botConectado = False

@bot.event
async def on_resumed():
    global botConectado
    if(not botConectado):
        MandarAoConsole(CV.LerDataYML(mensagens,"BOT-Recuperou-Conexao","Console"),1)
        await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"BOT-Recuperou-Conexao","Discord"))
    botConectado = True

@bot.event
async def on_connect():
    global botConectado
    if(not botConectado):
        MandarAoConsole(CV.LerDataYML(mensagens,"Bot-Estabeleceu-Conexao","Console"))
    botConectado = True

@bot.event
async def on_ready():
    global channel, botIniciado
    MandarAoConsole(f"Bot Conectado com Sucesso Como: '{bot.user.display_name}'!")
    botIniciado = True
    channel = bot.get_channel(canalDoBot)
    if(channel):
        MandarAoConsole(CV.LerDataYML(mensagens,"Bot-Conectado-Ao-Canal","Console",i=channel.name))
        await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"Bot-Conectado-Ao-Canal","Discord"))
    else:
        MandarAoConsole(CV.LerDataYML(mensagens,"Bot-Nao-Conectou-Ao-Canal","Console"),2)
        return

@bot.command(name='iniciar')
async def ComandoIniciar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"Bot-Comando-Iniciar","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    IniciarServidor()
    
@bot.command(name='parar')
async def ComandoParar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"Bot-Comando-Parar","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    PararServidor()
    
@bot.command(name='fparar')
async def ComandoForcarParar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"Bot-Comando-Forcar-Parada","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    PararServidor(True)
    
@bot.command(name='reiniciar')
async def ComandoReiniciar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"Bot-Comando-Reiniciar","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    ReiniciarServidor()

@bot.command(name='jogadores')
async def ComandoReiniciar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    if(EstadoServidor() is False):
        await asyncio.to_thread (MandarAoDiscord,f"O Servidor **NÃO** Está **LIGADO**!")
        return
    await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"Bot-Comando-Jogadores","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    MostrarTotalDeJogadores()

@bot.command(name='rcon')
async def ComandoRcon(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    if(EstadoServidor() is False):
        await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"RCON-Servidor-Inativo","Discord"))
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Servidor-Inativo","Console"),2)
        return
    comandoDigitado = ctx.message.content.replace(f'{prefixComandos}rcon ','').strip()
    if(comandoDigitado and len(comandoDigitado) > 0):
        respostaComando = MandarComando(comandoDigitado)
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Comando-Discord","Console",i=comandoDigitado,j=ctx.author.name),1)
        await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"RCON-Comando-Discord","Discord",i=comandoDigitado,j=ctx.author.name),
                                 [ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
        if(respostaComando):
            await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"RCON-Resposta-Servidor","Discord",i=respostaComando),NomeIconeServidor())
    else:
        await asyncio.to_thread (MandarAoDiscord,CV.LerDataYML(mensagens,"RCON-Erro-Digitacao","Discord"),NomeIconeServidor())
        MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Erro-Digitacao","Console",i=ctx.author.name),1)
        
# FIM EVENTOS DO BOT

def IniciarBot(q):
    if(not TOKEN or not canalDoBot or not cargoPermitido):
        MandarAoConsole("Informações do BOT do Discord INCOMPLETAS ou INVÁLIDAS!\nO BOT NÃO Será Iniciado!...",2)
        q.put("FALHA")
        return False
    try:
        MandarAoConsole(CV.LerDataYML(mensagens,"Bot-Iniciando","Console"),1)
        bot.run(TOKEN)
    except Exception as e:
        MandarAoConsole(CV.LerDataYML(mensagens,"Bot-Erro-Generico","Console",i=e),2)
        q.put("FALHA")
    MandarAoConsole(CV.LerDataYML(mensagens,"BOT-Desligado","Console"),1)

def EstadoServidor():
    if(server):
        if isinstance(server, subprocess.Popen):
            return server.poll() is None
        if isinstance(server, psutil.Process):
            return server.is_running()
    return False

def TestarConexaoAoServidor(tentativasMax=5):
    global clientJava
    for i in range(tentativasMax):
        if(EstadoServidor() is False):
            return
        try:
            if(portaServidor != '80' or portaServidor.upper() != 'HTTPS'):
                clientJava = JavaServer(ipServidor,int(portaServidor))
            else:
                clientJava = JavaServer(ipServidor)
            clientJava.status()
            clientJava.query_port = int(portaQuery)
            return True
        except Exception:
            pass
        CV.Delay(10)
    return False 

def MostrarTotalDeJogadores():
    if(TestarConexaoAoServidor()):
        statusServidor = clientJava.status()
        quantidadeDeJogadores = statusServidor.players.online
        mensagemConsole = f"Há {quantidadeDeJogadores} {'Jogador' if quantidadeDeJogadores <= 1 else 'Jogadores'} Online no Servidor!" if quantidadeDeJogadores > 0 else "Não há Nenhum Jogador Online no Servidor!"
        mensagemDiscord = f"Há **{quantidadeDeJogadores}** {'Jogador' if quantidadeDeJogadores <= 1 else 'Jogadores'} Online no **Servidor**!" if quantidadeDeJogadores > 0 else "Não há **Nenhum Jogador Online** no **Servidor**!"
        if(quantidadeDeJogadores > 0):
            try:
                queryServidor = clientJava.query()
                listaConsole = []
                listaDiscord = []
                for jogador in queryServidor.players.list:
                    listaConsole.append(f"| {CV.Style.BRIGHT}{jogador}{CV.Style_Extra.ITALICO}")
                    listaDiscord.append(f"**|** ***`{jogador}`***")
                mensagemConsole += f"\n\nLista de Jogadores Online:\n{',\n'.join(listaConsole)}"
                mensagemDiscord += f"\n\nLista de Jogadores Online:\n{',\n'.join(listaDiscord)}"
            except:
                pass
        MandarAoConsole(mensagemConsole,3)
        MandarAoDiscord(mensagemDiscord,NomeIconeServidor())

def ChecarEstadoServidor():
    servidorFechou = threading.Event()
    
    def ChecarEssenciais():
        estadoInternet = True
        servidorNoAr = True
        rconConectado = True
        quantidadeDeJogadores = 0
        listaDeJogadores = []

        def OrdenarJogadores(jogadores):
            jogadoresOrdenados = []
            for jogador in jogadores:
                jogadoresOrdenados.append(f"'**{jogador}**'")
            return ', '.join(jogadoresOrdenados[:-1]) + f' e {jogadoresOrdenados[-1]}' if len(jogadoresOrdenados) > 1 else f'{''.join(jogadoresOrdenados)}'

        while not servidorFechou.is_set():
            if(not abrindoFechando):
                if(CV.TestarConexaoAInternet() is False):
                    MandarAoConsole(CV.LerDataYML(mensagens,"Estado-Internet-Perdida","Console"),1) if estadoInternet is True else None
                    estadoInternet = False
                else:
                    MandarAoConsole(CV.LerDataYML(mensagens,"Estado-Internet-Recuperada","Console-Discord")) if estadoInternet is False else None
                    MandarAoConsole(CV.LerDataYML(mensagens,"Estado-Internet-Recuperada","Console-Discord")) if estadoInternet is False else None
                    estadoInternet = True
            
            if servidorFechou.wait(1):
                break

            if(not abrindoFechando):
                if(TestarConexaoAoServidor() is False):
                    MandarAoConsole(CV.LerDataYML(mensagens,"Estado-Servidor-Caido","Console-Discord"),1) if servidorNoAr is True else None
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Estado-Servidor-Caido","Console-Discord")) if servidorNoAr is True else None
                    servidorNoAr = False
                else:
                    MandarAoConsole(CV.LerDataYML(mensagens,"Estado-Servidor-Reativo","Console-Discord")) if servidorNoAr is False else None
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Estado-Servidor-Reativo","Console-Discord")) if servidorNoAr is False else None
                    servidorNoAr = True
                    try:
                        quantidadeAtual = clientJava.status().players.online
                        if(quantidadeDeJogadores != quantidadeAtual):
                            try:
                                queryServidor = clientJava.query()
                                listaAtual = []
                                for jogador in queryServidor.players.list:
                                    listaAtual.append(jogador)

                                jogadoresLogados = list(set(listaAtual).difference(listaDeJogadores))
                                jogadoresDeslogados = list(set(listaDeJogadores).difference(listaAtual))

                                mensagemPlayersLogados = (f"{'Os **Jogadores**' if len(jogadoresLogados) > 1 else 'O **Jogador**'} {OrdenarJogadores(jogadoresLogados)} " 
                                f"{'**Entraram**' if len(jogadoresLogados) > 1 else '**Entrou**'} no **Servidor**!")
                                mensagemPlayersDeslogados = (f"{'Os **Jogadores**' if len(jogadoresDeslogados) > 1 else 'O Jogador'} {OrdenarJogadores(jogadoresDeslogados)} " 
                                f"{'**Quitaram**' if len(jogadoresDeslogados) > 1 else '**Quitou**'} no **Servidor**!")
                                
                                mensagemSemPlayers = "O **Servidor** Está **Vazio**!"
                                
                                if len(jogadoresLogados) > 0:
                                    MandarAoConsole(mensagemPlayersLogados.replace('**',''),3) 
                                    MandarAoDiscord(mensagemPlayersLogados,NomeIconeServidor())

                                if len(jogadoresDeslogados) > 0:
                                    MandarAoConsole(mensagemPlayersDeslogados.replace('**',''),3) 
                                    MandarAoDiscord(mensagemPlayersDeslogados,NomeIconeServidor())

                                if len(listaAtual) < 1:
                                    MandarAoConsole(mensagemSemPlayers.replace('**',''),3) 
                                    MandarAoDiscord(mensagemSemPlayers,NomeIconeServidor())
                                
                                listaDeJogadores = listaAtual
                            except:
                                MostrarTotalDeJogadores()

                            quantidadeDeJogadores = quantidadeAtual
                    except:
                        pass

            if servidorFechou.wait(1):
                break

            if(not abrindoFechando):
                if(TestarConexaoAoRcon() is False):
                    MandarAoConsole(CV.LerDataYML(mensagens,"Estado-RCON-Caido","Console"),1) if rconConectado is True else None
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Estado-RCON-Caido","Discord")) if rconConectado is True else None
                    rconConectado = False
                    ConectarRcon(12) if rconConectado is False else None
                else:
                    MandarAoConsole(CV.LerDataYML(mensagens,"Estado-RCON-Reativo","Console")) if rconConectado is False else None
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Estado-RCON-Reativo","Discord")) if rconConectado is False else None
                    rconConectado = True

            servidorFechou.wait(3)
    
    checarEssen = threading.Thread(target=ChecarEssenciais,daemon=True).start()
    with keep.running():
        while EstadoServidor():
            CV.Delay(0.1)
    servidorFechou.set()

    MandarAoConsole(CV.LerDataYML(mensagens,"Estado-Servidor-Fechado","Console-Discord"),1)
    MandarAoDiscord(CV.LerDataYML(mensagens,"Estado-Servidor-Fechado","Console-Discord"),NomeIconeServidor())

def ChecarBateria():
    bateria = psutil.sensors_battery()
    if bateria is None:
        return
    return bateria


def MonitorarBateria():
    bateria = psutil.sensors_battery()
    if bateria is None:
        return
    aviso_console = False
    aviso_jogadores = False
    aviso_nivelCritico = False
    aviso_contagemFinal = False
    nivelDeAvisoAtual = 0
    contagemParaDesligar = tempoAutoDesligamento

    while (EstadoServidor()):
        bateria = psutil.sensors_battery()
        naTomada = bateria.power_plugged
        nivel = bateria.percent

        if(naTomada is False):
            if(aviso_console is False):
                MandarAoConsole(CV.LerDataYML(mensagens,"Aviso-Modo-Bateria","Console-Discord"),1)
                MandarAoDiscord(CV.LerDataYML(mensagens,"Aviso-Modo-Bateria","Console-Discord"),NomeIconeServidor())
                MandarAoChat(CV.LerDataYML(mensagens,"Aviso-Modo-Bateria","Chat"))
                aviso_console = True
            match nivel:
                case 90 | 80 | 70 | 60 | 50 | 45 | 40 | 35 | 30 | 25 | 20:
                    if(nivel != nivelDeAvisoAtual):
                        MandarAoConsole(CV.LerDataYML(mensagens,"Nivel-Bateria","Console-Discord",i=nivel),1)
                        MandarAoDiscord(CV.LerDataYML(mensagens,"Nivel-Bateria","Console-Discord",i=nivel),NomeIconeServidor())
                        MandarAoChat(CV.LerDataYML(mensagens,"Nivel-Bateria","Chat",i=nivel))
                        if(nivel <= 20 and aviso_jogadores is False):
                            MandarAoChat(CV.LerDataYML(mensagens,"Nivel-Bateria-Baixa","Chat"))
                            MandarAoConsole(CV.LerDataYML(mensagens,"Nivel-Bateria-Baixa","Console"),1)
                            aviso_jogadores = True
                        nivelDeAvisoAtual = nivel
                case _ if nivel <= 15:
                    porAmbientacao = "execute at @a run playsound minecraft:ambient.cave ambient @a" # SFXs Pois... Deu vontade. '-'
                    if(aviso_nivelCritico is False):
                        MandarAoConsole(CV.LerDataYML(mensagens,"Nivel-Critico","Console-Discord",i=nivel),1)
                        MandarAoDiscord(CV.LerDataYML(mensagens,"Nivel-Critico","Console-Discord",i=nivel),NomeIconeServidor())
                        MandarComando(porAmbientacao)
                        MandarAoChat(CV.LerDataYML(mensagens,"Nivel-Critico","Chat",i=nivel,j=tempoAutoDesligamento))

                        MandarComando(porAmbientacao)
                        MandarComoTitulo(CV.LerDataYML(mensagens,"Contagem-Para-Desligar","Titulo",i=tempoAutoDesligamento))
                        aviso_nivelCritico = True

                    if(contagemParaDesligar > 0):
                        contagemParaDesligar -= 1
                        MandarAoConsole(CV.LerDataYML(mensagens,"Tempo-Auto-Desligamento","Console-Discord",i=contagemParaDesligar), 1)
                        MandarAoDiscord(CV.LerDataYML(mensagens,"Tempo-Auto-Desligamento","Console-Discord",i=contagemParaDesligar), NomeIconeServidor())
                        match contagemParaDesligar:
                            case 50 | 40 | 30 | 20 | 10:
                                MandarAoConsole(CV.LerDataYML(mensagens,"Contagem-Para-Desligar","Console-Discord",i=contagemParaDesligar),1)
                                MandarAoChat(CV.LerDataYML(mensagens,"Contagem-Para-Desligar","Chat",i=contagemParaDesligar))
                                MandarComoTitulo(CV.LerDataYML(mensagens,"Contagem-Para-Desligar","Titulo",i=contagemParaDesligar))
                                MandarComando(porAmbientacao)
                            case _ if contagemParaDesligar <= 10:
                                if(aviso_contagemFinal is False):
                                    MandarAoConsole(CV.LerDataYML(mensagens,"Contagem-Final-Iniciada","Console-Discord"),1)
                                    MandarAoDiscord(CV.LerDataYML(mensagens,"Contagem-Final-Iniciada","Console-Discord"),NomeIconeServidor())
                                    MandarComando(porAmbientacao)
                                    aviso_contagemFinal = True
                                MandarAoChat(CV.LerDataYML(mensagens,"Contagem-Final","Chat",i=contagemParaDesligar))
                                MandarComoTitulo(f"{CV.LerDataYML(mensagens,"Contagem-Final","Titulo",i=contagemParaDesligar)} {"!.." if contagemParaDesligar <= 5 else "..."}")
                    else:
                        CV.Delay(3)
                        MandarComando(porAmbientacao)
                        MandarAoChat(CV.LerDataYML(mensagens,"Fim-Da-Contagem","Chat"))
                        MandarComoTitulo(f"{random.choice(CV.LerDataYML(mensagens,"Ultimas-Palavras"))}")
                        CV.Delay(2)
                        MandarAoConsole(CV.LerDataYML(mensagens,"Fim-Da-Contagem","Console-Discord"),1)
                        MandarAoDiscord(CV.LerDataYML(mensagens,"Fim-Da-Contagem","Console-Discord"),NomeIconeServidor())
                        PararServidor()
                        break
        else:
            if(aviso_console is True):
                MandarAoConsole(CV.LerDataYML(mensagens,"Aviso-Na-Energia","Console-Discord"))
                MandarAoDiscord(CV.LerDataYML(mensagens,"Aviso-Na-Energia","Console-Discord"),NomeIconeServidor())
                MandarAoChat(CV.LerDataYML(mensagens,"Aviso-Na-Energia","Chat"))
            aviso_console = False
            aviso_nivelCritico = False
            aviso_contagemFinal = False
            nivelDeAvisoAtual = 0
            contagemParaDesligar = tempoAutoDesligamento
        CV.Delay(1)

def IniciarServidor():
    def Iniciar():
        global server, abrindoFechando
        abrindoFechando = True
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar","Console-Discord"),1)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar","Console-Discord"),NomeIconeServidor())
        openServer =  None
        RAM=f"{quantidadeDeRAM}{'G' if len(str(quantidadeDeRAM)) <= 1 else 'M'}"
        linhasExecucao = ['JAVA', f'-Xmx{RAM}',f'-Xms{RAM}', '-jar', arquivoExecucao, 'nogui']
        for processo in psutil.process_iter(['pid','cmdline']):
            try:
                linhaProcesso = " ".join(processo.info['cmdline']).lower()
                if(any (linha in linhaProcesso for linha in linhasExecucao) and arquivoExecucao in linhaProcesso and processo.cwd() == os.getcwd()):
                    openServer = processo
            except:
                pass
        if(openServer):
            MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Ja-Aberto","Console",i=processo.pid),1)
            server = openServer
        else:
            server = subprocess.Popen(linhasExecucao,creationflags=subprocess.CREATE_NEW_CONSOLE)
            CV.Delay(5)
        servidorConectado = False
        tentativasDeConexao = 0
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Conexao-IP","Console-Discord",i=ipServidor,j=portaServidor),1)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Conexao-IP","Console-Discord",i=ipServidor,j=portaServidor))
        while(tentativasDeConexao < 60 and EstadoServidor()):
            if(TestarConexaoAoServidor()):
                MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-IP-Ativo","Console-Discord"))
                MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar-IP-Ativo","Console-Discord"))
                servidorConectado = True
                break
            tentativasDeConexao += 1
            CV.Delay(1)
        if(EstadoServidor()):
            CV.Delay(3)
            if(servidorConectado):
                MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Conexao-RCON","Console-Discord",i=ipRcon,j=portaRcon),1)
                MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Conexao-RCON","Console-Discord",i=ipRcon,j=portaRcon))
                if(ConectarRcon()):
                    MandarAoConsole(CV.LerDataYML(mensagens,"RCON-Conectado","Console"))
                    MandarAoDiscord(CV.LerDataYML(mensagens,"RCON-Conectado","Discord"),NomeIconeServidor())
                    CV.Delay(2)
                    MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Concluida","Console-Discord"))
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Concluida","Console-Discord"),NomeIconeServidor())
                else:
                    MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-RCON-Falha","Console"),2)
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar-RCON-Falha","Discord"),NomeIconeServidor())
            else:
                    MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-IP-Falha","Console-Discord"),2)
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar-IP-Falha","Console-Discord"),NomeIconeServidor())
            threading.Thread(target=MonitorarBateria, daemon=True).start()
            threading.Thread(target=ChecarEstadoServidor, daemon=True).start()
        else:
            MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Falha","Console-Discord"),2)
            MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Falha","Console-Discord"),NomeIconeServidor())
        abrindoFechando = False

    if not os.path.isfile(arquivoExecucao):
        MandarAoConsole(f"O Arquivo do Servidor '{arquivoExecucao}' NÃO Pôde Ser Encontrado!",2)
        return

    if(abrindoFechando):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"),NomeIconeServidor())
        return
    
    if(CV.TestarConexaoAInternet() is False):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Sem-Internet","Console"),2)
        return
        
    if(EstadoServidor()):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Ja-Aberto","Console-Discord"),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Ja-Aberto","Console-Discord"),NomeIconeServidor())
        return
    
    threading.Thread(target=Iniciar,daemon=True).start()

    if(ChecarBateria() and not ChecarBateria().power_plugged):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Modo-Bateria","Console-Discord"),1)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Iniciar-Modo-Bateria","Console-Discord"),NomeIconeServidor())
            

def PararServidor(forcarParada = False):
    def Parar(f):
        global server, abrindoFechando
        abrindoFechando = True
        tempoLimite = 90
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Parar","Console-Discord"),1)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Parar","Console-Discord"),NomeIconeServidor())
        
        contagem = 0
        while(EstadoServidor()):
            if(f):
                break
            match contagem:
                case 0:
                    if(TestarConexaoAoRcon() is False):
                        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Parar-RCON-Inativo","Console-Discord"),2)  
                        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Parar-RCON-Inativo","Console-Discord"),NomeIconeServidor())
                        break
                    else:
                        MandarComando("stop")
                case _ if contagem == (tempoLimite / 2):
                    MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Parar-Longo-Tempo","Console-Discord",i=CV.ConverterEmTempo(tempoLimite-contagem,True)),1)
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Parar-Longo-Tempo","Console-Discord",i=CV.ConverterEmTempo(tempoLimite-contagem,True)),NomeIconeServidor())
                case _ if contagem == tempoLimite:
                    MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Parar-Tempo-Limite","Console-Discord"),1)
                    MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Parar-Tempo-Limite","Console-Discord"),NomeIconeServidor())
                    break
            CV.Delay(1)
            contagem += 1

        if(EstadoServidor()):
            MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Parar-Forcar-Parada","Console-Discord"),1)
            MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Parar-Forcar-Parada","Console-Discord"),NomeIconeServidor())
            subprocess.Popen("TASKKILL /F /PID {} /T".format(server.pid), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
            server.wait()

        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Parar-Concluida","Console-Discord"))
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Parar-Concluida","Console-Discord"))
        abrindoFechando = False

    if(abrindoFechando):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"))
        return

    if(EstadoServidor() is False):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Nao-Aberto","Console-Discord"),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Nao-Aberto","Console-Discord"),NomeIconeServidor())
        return
    
    threading.Thread(target=lambda: Parar(forcarParada),daemon=True).start()

def ReiniciarServidor():
    def Reiniciar():
        global abrindoFechando
        PararServidor()
        while(EstadoServidor() and abrindoFechando):
            CV.Delay(1)
        CV.Delay(2)
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Reiniciar","Console-Discord"),1)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Reiniciar","Console-Discord"))
        CV.Delay(5)
        abrindoFechando = False
        IniciarServidor()

    if(abrindoFechando):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"))
        return

    if(EstadoServidor() is False):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Nao-Aberto","Console-Discord"),2)
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Nao-Aberto","Console-Discord"),NomeIconeServidor())
        return

    threading.Thread(target=Reiniciar,daemon=True).start()

def FecharControlador():
    global abrindoFechando
    if(EstadoServidor() is True or abrindoFechando):
        MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Terminal-Servidor-Aberto","Console"),2)
        return
    abrindoFechando = True
    MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Terminal","Console-Discord"),1)
    CV.Delay(1)
    if(EstadoBot()):
        MandarAoDiscord(CV.LerDataYML(mensagens,"Tarefa-Terminal","Console-Discord"))
        MandarAoDiscord(CV.LerDataYML(mensagens,"BOT-Desligado","Discord"))
        asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
        CV.Delay(2)
    MandarAoConsole(CV.LerDataYML(mensagens,"Tarefa-Terminal-Concluida","Console"))
    CV.Delay(1)
    CV.Creditos()
    envVar["SOFTSHUT"] = "Yes"
    set_key(arquivoEnv,"SOFTSHUT",envVar["SOFTSHUT"],quote_mode="never")
    CV.Delay(2)
    os.kill(os.getpid(), signal.SIGTERM)

def Main():
    try:
        hotkeysPadrao = {'HOTSTART':'ctrl+i','HOTSTOP':'ctrl+p','HOTFSTOP':'ctrl+shift+p','HOTRESTART':'ctrl+r','HOTCLOSE':'ctrl+l'}
        for hotkeyPadrao, atalho in hotkeysPadrao.items():
            if(not hotkeyPadrao in envVar or not atalho):
                envVar[hotkeyPadrao] = atalho
                set_key(arquivoEnv,hotkeyPadrao,envVar[hotkeyPadrao])
        hotkeys = {
            envVar.get("HOTSTART", hotkeysPadrao["HOTSTART"]): IniciarServidor,
            envVar.get("HOTSTOP", hotkeysPadrao["HOTSTOP"]): PararServidor,
            envVar.get("HOTFSTOP", hotkeysPadrao["HOTFSTOP"]): lambda: PararServidor(True),
            envVar.get("HOTRESTART", hotkeysPadrao["HOTRESTART"]): ReiniciarServidor,
            envVar.get("HOTCLOSE", hotkeysPadrao["HOTCLOSE"]): FecharControlador
        }
        for hotkey, funcao in hotkeys.items():
            if(hotkey and funcao):
                keyboard.add_hotkey(str(hotkey),funcao)
    except Exception as e:
        print(e)

    CV.MenuOpcoes(f'{CV.Style.BRIGHT}{envVar.get("HOTSTART").upper()}{CV.Style.NORMAL}{CV.Style_Extra.ITALICO}: Iniciar o Servidor',
            f'{CV.Style.BRIGHT}{envVar.get("HOTSTOP").upper()}{CV.Style.NORMAL}{CV.Style_Extra.ITALICO}: Parar o Servidor', 
            f'{CV.Style.BRIGHT}{envVar.get("HOTFSTOP").upper()}{CV.Style.NORMAL}{CV.Style_Extra.ITALICO}: Forçar Parar o Servidor', 
            f'{CV.Style.BRIGHT}{envVar.get("HOTRESTART").upper()}{CV.Style.NORMAL}{CV.Style_Extra.ITALICO}: Reiniciar o Servidor',
            f'{CV.Style.BRIGHT}{envVar.get("HOTCLOSE").upper()}{CV.Style.NORMAL}{CV.Style_Extra.ITALICO}: Saída Suave (Recomendado!)',
            titulo=nomServidor)
    
    if(EstadoBot()):
        MandarAoDiscord(f'**{prefixComandos}iniciar** - _Abrir o Servidor_\n**{prefixComandos}parar** -' 
        f'_Fechar o Servidor_\n**{prefixComandos}fparar** - _Forçar o Fechamento_\n**{prefixComandos}reiniciar** -' 
        f'_Reiniciar o Servidor_\n**{prefixComandos}rcon "comando"** - _Enviar Comandos ao Servidor_'
        f'\n**{prefixComandos}jogadores** - _Mostrar Jogadores Atuais no Servidor_'
        )

    keyboard.wait()

CV.BinaryFill(15)
CV.Limpar()
    
if not os.path.isfile(arquivoExecucao):
    MandarAoConsole(f"O Arquivo do Servidor '{arquivoExecucao}' NÃO Pôde Ser Encontrado!",2,False)
    keyboard.wait('esc')
    sys.exit()

if(not 'SOFTSHUT' in envVar or envVar["SOFTSHUT"] == "Yes"):
    envVar["SOFTSHUT"] = "No"
    set_key(arquivoEnv,"SOFTSHUT",envVar["SOFTSHUT"],quote_mode="never")
else:
    MandarAoConsole(CV.LerDataYML(mensagens,"Terminal-Fechado-Abruptamente","Console"),2)
    CV.Delay(2)
    CV.Limpar()

tentativasConexao = 0
tempoAteNovaTentativa = 10
while(CV.TestarConexaoAInternet() is False):
    MandarAoConsole(CV.LerDataYML(mensagens,"Terminal-Sem-Internet","Intro"),2) if tentativasConexao < 3 else MandarAoConsole(random.choice(CV.LerDataYML(mensagens,"Terminal-Sem-Internet","Nag")),2)
    CV.Delay(2)
    MandarAoConsole(CV.LerDataYML(mensagens,"Terminal-Sem-Internet","Loop",i=tempoAteNovaTentativa),1)
    tentativasConexao += 1
    CV.Delay(tempoAteNovaTentativa)
    CV.Limpar()

if(not 'DISCOBOT' in envVar or envVar["DISCOBOT"] == "Yes"):
    envVar["DISCOBOT"] = "Yes"
    set_key(arquivoEnv,"DISCOBOT",envVar["DISCOBOT"],quote_mode="never")
    q = queue.Queue()
    threading.Thread(target=IniciarBot,args=(q,),daemon=True).start()
    while(EstadoBot() is False):
        try:
            statusBot = q.get(timeout=1)
            if(statusBot == "FALHA"):
                CV.Delay(1)
                break
        except queue.Empty:
            pass
else:
    MandarAoConsole(CV.LerDataYML(mensagens,"Terminal-Sem-Discord","Console",i=arquivoEnv),1)

CV.Delay(2)
CV.Limpar()
Main()