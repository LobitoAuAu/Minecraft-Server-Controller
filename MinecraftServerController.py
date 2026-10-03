# === | BIBLIOTECAS NATIVAS | ===
import subprocess,threading,queue,os,sys,signal,random,asyncio,logging,shutil,traceback,ctypes,uuid
import tkinter as tk

from tkinter import ttk, messagebox

# === | MINHAS BIBLIOTECAS | ===
from Bibliotecas import CVLib as CV

# === | BIBLIOTECAS EXTERNAS | ===
CV.InstalarAtualizarBiblio("keyboard","psutil","discord","pygame","wakepy","mcstatus","mcrcon","python-dotenv",
                           "Pillow","sv-ttk")

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import keyboard,psutil,discord,pygame,sv_ttk
from wakepy import keep
from mcstatus import JavaServer
from mcrcon import  MCRcon
from discord.ext import commands
from dotenv import set_key, dotenv_values
from PIL import ImageTk, Image

pastaData = CV.ProcessarPastaDeDados(CV.DiretorioAtual(),"MSCData")

arquivoMensagens = 'mensagens.yml'
dirArquivoMensagens = rf"{pastaData}/{arquivoMensagens}"

dirEfeitosSonoros = rf"{pastaData}/SOUNDS"
arquivoLog = "controller_log.log"
dirArquivoLog = rf"{pastaData}/{arquivoLog}"
logging.basicConfig(filename=dirArquivoLog,level=logging.INFO,format='%(asctime)s - %(message)s', filemode='a')

logging.getLogger("discord").setLevel(logging.CRITICAL)
logging.getLogger("discord.client").setLevel(logging.CRITICAL)
logging.getLogger("discord.gateway").setLevel(logging.CRITICAL)
logging.getLogger("discord.ext.commands.bot").setLevel(logging.CRITICAL)

tempoInicial = CV.DataAtual().date()

def TempoRodando():
    tempoDecorrido = CV.DataAtual().date() - tempoInicial
    return tempoDecorrido.days + 1

def TocarSom(SOMATOCAR,vol=0.1):
        try:
            som = pygame.mixer.Sound(SOMATOCAR)
            pygame.mixer.Sound.play(som)
            pygame.mixer.SoundType.set_volume(som,vol)
            return som
        except:
            pass

def MandarLog(mensagem):
    logging.info(f"{mensagem}")

def ModYML(d,c,v):
    CV.ModificarDadosYML(d,c,valor=v)


lockConsole = threading.Lock()
def MandarAoConsole(msg, tipo=0, log=True):
    with lockConsole:
        def SomMensagem():
            match tipo:
                case 0:
                    TocarSom(somMsgSucesso,0.1)
                case 1:
                    TocarSom(somMsgAviso,0.15)
                case 2:
                    TocarSom(somMsgErro,0.15)
                case 3:
                    TocarSom(somMsgInfo,0.15)
        if isinstance(msg, list):
            for i, m in enumerate(msg):
                CV.MensagemDeConsolePro(m,tipo,titulo=nomServidor.upper() or "MINE-SERVER",horario=True,data=True,prefixoRotulo=f"DIA {TempoRodando()} ၊| ")
                SomMensagem()
                if(i < len(msg) - 1):
                    CV.Delay(1)
        else:
            CV.MensagemDeConsolePro(msg,tipo,titulo=nomServidor.upper() or "MINE-SERVER",horario=True,data=True,pularLinha=True,prefixoRotulo=f"DIA {TempoRodando()} ၊| ")
            SomMensagem()
        # Gravar Mensagem de Console no Arquivo de Logs
        if(log is True):
            MandarLog(f"[TERMINAL]: {tipo}: {msg}")

def LerServerProperties(setting=''):
    try:
        with open('server.properties', 'r', encoding='utf-8') as cfgs:
            linhas = cfgs.readlines()
            for linha in linhas:
                linhaConvertida = linha.replace('\n','').split('=')
                if(setting in linhaConvertida):
                    return linhaConvertida[1] or ''
    except Exception as e:
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
arquivoConfigs = "mscserver_config.yml"
dirArquivoConfigs = rf"{pastaData}/{arquivoConfigs}"
if not os.path.isfile(dirArquivoConfigs):
    CV.Limpar()
    CV.Write(f"\033[1;31mO Arquivo do Servidor '{arquivoConfigs}' NÃO Pôde Ser Encontrado!\nGerando um Automático...")
    CV.Delay(0.5)
    try:
        nomeCfgBackup = "mscserver_config_backup.yml"
        dir = rf"{pastaData}/{nomeCfgBackup}"
        if(os.path.isfile(dir)):
            shutil.copy(dir,rf"{pastaData}/{arquivoConfigs}")
    except Exception as e:
        if(e == FileExistsError):
            pass
        else:
            CV.Limpar()
            CV.Write(f"\033[1;31mO Arquivo do Servidor '{arquivoConfigs}' NÃO Pôde Ser Gerado Por Causa do Seguinte Erro:\n\033[0m")
            traceback.print_exc()
            CV.Write(f"\033[1;31mO Terminal NÃO Poderá ser Aberto!")
            keyboard.wait()
            sys.exit()
    CV.Limpar()

somMsgInfo = os.path.join(dirEfeitosSonoros,CV.LerDadosYML(dirArquivoConfigs, "INFO", dadoPadrao="Info.mp3"))
somMsgAviso = os.path.join(dirEfeitosSonoros,CV.LerDadosYML(dirArquivoConfigs, "AVISO", dadoPadrao="Aviso.mp3"))
somMsgErro = os.path.join(dirEfeitosSonoros,CV.LerDadosYML(dirArquivoConfigs, "FALHA", dadoPadrao="Falha.mp3"))
somMsgSucesso = os.path.join(dirEfeitosSonoros,CV.LerDadosYML(dirArquivoConfigs, "SUCESSO", dadoPadrao="Sucesso.mp3"))
somBinaryFill = os.path.join(dirEfeitosSonoros,CV.LerDadosYML(dirArquivoConfigs, "BINARYFILL", dadoPadrao="BinaryFill.mp3"))
somPainelOpcoes = os.path.join(dirEfeitosSonoros,CV.LerDadosYML(dirArquivoConfigs, "PAINELOPCOES", dadoPadrao="PainelOpcoes.mp3"))
musicaCreditos = os.path.join(dirEfeitosSonoros,CV.LerDadosYML(dirArquivoConfigs, "MUSICCREDITOS", dadoPadrao="MusicaCreditos.mp3"))
musicaTarefa = os.path.join(dirEfeitosSonoros,CV.LerDadosYML(dirArquivoConfigs, "MUSICTAREFA", dadoPadrao="MusicaTarefa.mp3"))

argumentosDeExecucao = CV.LerDadosYML(dirArquivoConfigs,"JAVARGS")
tempoInativoLimite = CV.LerDadosYML(dirArquivoConfigs,'AUTOSHUT',dadoPadrao=0)

arquivoExecucao = CV.LerDadosYML(dirArquivoConfigs, "JAVA", dadoPadrao="server.jar")
ModYML(dirArquivoConfigs,"JAVA",arquivoExecucao)

nomServidor = CV.LerDadosYML(dirArquivoConfigs,"NOMESERV",dadoPadrao=os.path.basename(os.getcwd()) or "Menu-Servidor")
ModYML(dirArquivoConfigs, "NOMESERV", nomServidor)

ipServidor = CV.LerDadosYML(dirArquivoConfigs, "IPSERVER", dadoPadrao=LerServerProperties('server-ip') or "localhost")
ModYML(dirArquivoConfigs, "IPSERVER", ipServidor)
 
portaServidor = (CV.LerDadosYML(dirArquivoConfigs, "PORTSERVER", dadoPadrao=LerServerProperties('server-port') or 25565))
ModYML(dirArquivoConfigs, "PORTSERVER", portaServidor)

portaQuery = (CV.LerDadosYML(dirArquivoConfigs, "QUERYPORT", dadoPadrao=LerServerProperties('query.port') or 25565))
ModYML(dirArquivoConfigs, "QUERYPORT", portaQuery)

ipRcon = CV.LerDadosYML(dirArquivoConfigs, "RCONIP", dadoPadrao=ipServidor)
ModYML(dirArquivoConfigs, "RCONIP", ipRcon)

portaRcon = (CV.LerDadosYML(dirArquivoConfigs, "RCONPORT", dadoPadrao=LerServerProperties('rcon.port') or 25575))
ModYML(dirArquivoConfigs, "RCONPORT", portaRcon)

senhaRcon = CV.LerDadosYML(dirArquivoConfigs, "RCONPASS",dadoPadrao=LerServerProperties('rcon.password'))
ModYML(dirArquivoConfigs, "RCONPASS",senhaRcon)

tempoInativoLimite = CV.LerDadosYML(dirArquivoConfigs,'AUTOSHUT',dadoPadrao=0)

server = None
clientJava = None
abrindoFechando = False

clientRcon = MCRcon(ipRcon,senhaRcon,int(portaRcon),timeout=10)
lockRcon = threading.Lock()

ModificarServerProperties('enable-rcon','true')
ModificarServerProperties('enable-status','true')
ModificarServerProperties('enable-query','true')

mensagens = CV.LerArquivoYML(dirArquivoMensagens)
if(mensagens is None):
    keyboard.wait('esc')
    sys.exit()  

TOKEN = CV.LerDadosYML(dirArquivoConfigs,'BOTTOKEN')
canalDoBot = CV.LerDadosYML(dirArquivoConfigs,'BOTCHANNEL')

cargoPermitido = CV.LerDadosYML(dirArquivoConfigs,'ADMROLE',dadoPadrao='Adm')

prefixComandos = '!'

ints = discord.Intents.default()
ints.message_content = True
bot = commands.Bot(command_prefix=prefixComandos, intents=ints,case_insensitive=True)
botIniciado = False

def ObterMensagensYML(blocoDeMensagens,nomeMensagem,nomeMidia=None,**args):
    caminhoMensagem = [nomeMensagem]
    caminhoMensagem.append(nomeMidia) if nomeMidia is not None else None
    mensagemObtida = CV.LerDadosYML(blocoDeMensagens,*caminhoMensagem,argumentos=args)
    if(mensagemObtida):
        return mensagemObtida
    return f"{nomeMensagem}: ???"

def LinhasBinarias(vezes=10):
    efeitoSonoro = TocarSom(somBinaryFill,0.4)
    CV.BinaryFill(vezes)
    if(efeitoSonoro):
        efeitoSonoro.stop()
    CV.Delay(0.05)

def ExecutarRCON(comandoDesejado,log=True):
    if(not EstadoProcesso() or not TestarConexaoAoServidor()):
        return False, None
    with lockRcon:
        try:
            respostaRCON = clientRcon.command(comandoDesejado)
            return True, respostaRCON
        except:
            try:
                clientRcon.disconnect()
            except:
                pass
            try:
                clientRcon.connect()
                respostaRCON = clientRcon.command(comandoDesejado)
                if(len(respostaRCON) > 0):
                    MandarAoConsole(f'Resposta do Servidor: {respostaRCON.replace('\n','')}',1) if log else None
                    MandarAoDiscord(f'**Resposta** do Servidor: _{respostaRCON.replace('\n','')}_',NomeIconeServidor()) if log else None
                return True, respostaRCON
            except Exception as e:
                MandarAoConsole(f"O Comando RCON Enviado Retornou em Erro: {e}",2) if log else None
    return False, None


lockDiscord = threading.Lock()
def MandarAoDiscord(mensagem, author=None):
    if(not EstadoBot()):
        if(CV.LerDadosYML(dirArquivoConfigs,"DISCOBOT")== "Yes" and botIniciado):
            MandarAoConsole(ObterMensagensYML(mensagens,"Falha-Mensagem-Discord","Console"),2)
        return 
    with lockDiscord:
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
    prefixoChat = ObterMensagensYML(mensagens,"Prefixo-Chat")
    if isinstance(mensagem, list):
        for i, msg in enumerate(mensagem):
            ExecutarRCON(f'tellraw @a "{prefixoChat}{msg}"')
            if(i < len(mensagem) - 1):
                CV.Delay(2)
    else:
        ExecutarRCON(f'tellraw @a "{prefixoChat}{mensagem}"')

def MandarComoTitulo(mensagem):
    if(mensagens is None):
        return
    prefixoTitulo = CV.LerDadosYML(mensagens,"Prefixo-Titulo","Comeco"),CV.LerDadosYML(mensagens,"Prefixo-Titulo","Final")
    if isinstance(mensagem, list):
        for i, msg in enumerate(mensagem):
            ExecutarRCON(f'title @a title "{prefixoTitulo[0]}{msg.upper()}{prefixoTitulo[1]}"')
            if(i < len(mensagem) - 1):
                CV.Delay(3)
    else:
        ExecutarRCON(f'title @a title "{prefixoTitulo[0]}{mensagem.upper()}{prefixoTitulo[1]}"')

# EVENTOS DO BOT
def ChecarComandoDeUsuario(ctx):
    if(not ctx or ctx.author == bot.user):
        return False
    cargo = discord.utils.get(ctx.guild.roles,id=cargoPermitido)
    if(cargo not in ctx.author.roles or not ctx.author.guild_permissions.administrator):
        MandarAoDiscord(ObterMensagensYML(mensagens,"Comando-Sem-Permissao","Console-Discord",i=ctx.author.display_name))
        MandarAoConsole(ObterMensagensYML(mensagens,"Comando-Sem-Permissao","Console-Discord",i=ctx.author.display_name),1)
        return False
    if(ctx.channel.id != canalDoBot):
        MandarAoDiscord(ObterMensagensYML(mensagens,"Comando-Canal-Errado","Console-Discord",i=ctx.author.display_name))
        MandarAoConsole(ObterMensagensYML(mensagens,"Comando-Canal-Errado","Console-Discord",i=ctx.author.display_name),1)
        return False
    return True

def EstadoBot():
    if(bot.is_ready() and not bot.is_closed() and botConectado):
        return True
    return False

def AdquirirCanal(idDoCanal):
    if(not isinstance(idDoCanal, int)):
        try:
            idDoCanal = int(idDoCanal)
        except:
            MandarAoConsole(f"O ID do Canal Informado: '{idDoCanal}', NÃO é VÁLIDO!",2)
        
    canalDoDiscord = bot.get_channel(idDoCanal)
    if(canalDoDiscord):
        return canalDoDiscord
    MandarAoConsole(f"O Canal Selecionado NÃO Pôde Ser OBTIDO!",2)

def NomeIconeServidor():
    if(not EstadoBot()):
        return
    channel = AdquirirCanal(canalDoBot)
    if(EstadoBot() and channel):
        iconeServidor = channel.guild.icon.url
        nomeServidor = channel.guild.name
        if(iconeServidor):
            return nomeServidor,iconeServidor


async def send_message(message,author=None):
    if (EstadoBot() is False and CV.LerDadosYML(dirArquivoConfigs,"DISCOBOT" == "Yes")):
        MandarAoConsole(ObterMensagensYML(mensagens,"Erro-Mensagem-Discord","Console",i=message),2)
        return
    mensagemDiscord = discord.Embed()
    if(author):
        mensagemDiscord.set_author(name=f"[{author[0]}]:",icon_url=author[1])
    else:
        mensagemDiscord.set_author(name=f"[{bot.user.name}]:",icon_url=bot.user.avatar.url)

    mensagemDiscord.title = f"'{bot.user.name}' lhe enviou um recado:"
    mensagemDiscord.description = f'**-** "{message}"'
    mensagemDiscord.color=discord.Color.blurple()
    channel = AdquirirCanal(canalDoBot)
    if(not channel):
        return
    await channel.send(embed=mensagemDiscord)

botConectado = False
@bot.event
async def on_disconnect():
    global botConectado
    await asyncio.sleep(5)
    if(not bot.is_closed()):
        return
    MandarAoConsole(ObterMensagensYML(mensagens,"Bot-Perdeu-Conexao","Console"),1)
    botConectado = False

@bot.event
async def on_resumed():
    global botConectado
    if(not botConectado):
        MandarAoConsole(ObterMensagensYML(mensagens,"BOT-Recuperou-Conexao","Console"),1)
        await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"BOT-Recuperou-Conexao","Discord"))
    botConectado = True

@bot.event
async def on_connect():
    global botConectado
    if(not botConectado):
        MandarAoConsole(ObterMensagensYML(mensagens,"Bot-Estabeleceu-Conexao","Console"))
    botConectado = True

@bot.event
async def on_ready():
    global botIniciado
    MandarAoConsole(f"Bot Conectado com Sucesso Como: '{bot.user.display_name}'!")
    botIniciado = True

@bot.command(name='iniciar')
async def ComandoIniciar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"Bot-Comando-Iniciar","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    IniciarServidor()
    
@bot.command(name='parar')
async def ComandoParar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"Bot-Comando-Parar","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    PararServidor()
    
@bot.command(name='fparar')
async def ComandoForcarParar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"Bot-Comando-Forcar-Parada","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    PararServidor(True)
    
@bot.command(name='reiniciar')
async def ComandoReiniciar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"Bot-Comando-Reiniciar","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    ReiniciarServidor()

@bot.command(name='jogadores')
async def ComandoReiniciar(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    if(EstadoProcesso() is False):
        await asyncio.to_thread (MandarAoDiscord,f"O Servidor **NÃO** Está **LIGADO**!")
        return
    await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"Bot-Comando-Jogadores","Discord",i=ctx.author.display_name),[ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    MostrarTotalDeJogadores()

@bot.command(name='rcon')
async def ComandoRcon(ctx):
    if(EstadoBot() is False):
        return
    if(not ChecarComandoDeUsuario(ctx)):
        return
    if(EstadoProcesso() is False):
        await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"RCON-Servidor-Inativo","Discord"))
        MandarAoConsole(ObterMensagensYML(mensagens,"RCON-Servidor-Inativo","Console"),2)
        return
    comandoDigitado = ctx.message.content.replace(f'{prefixComandos}rcon ','').strip()
    if(comandoDigitado and len(comandoDigitado) > 0):
        ExecutarRCON(comandoDigitado)
        MandarAoConsole(ObterMensagensYML(mensagens,"RCON-Comando-Discord","Console",i=comandoDigitado,j=ctx.author.name),1)
        await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"RCON-Comando-Discord","Discord",i=comandoDigitado,j=ctx.author.name),
                                 [ctx.author.display_name, (ctx.author.avatar or ctx.author.default_avatar).url])
    else:
        await asyncio.to_thread (MandarAoDiscord,ObterMensagensYML(mensagens,"RCON-Erro-Digitacao","Discord"),NomeIconeServidor())
        MandarAoConsole(ObterMensagensYML(mensagens,"RCON-Erro-Digitacao","Console",i=ctx.author.name),1)
        
# FIM EVENTOS DO BOT

def IniciarBot(q):
    if(not TOKEN or not cargoPermitido or not canalDoBot):
        MandarAoConsole("Informações do BOT do Discord INCOMPLETAS ou INVÁLIDAS!\nO BOT NÃO Será Iniciado!...",2)
        q.put("FALHA")
        return False
    try:
        MandarAoConsole(ObterMensagensYML(mensagens,"Bot-Iniciando","Console"),1)
        bot.run(TOKEN)
    except Exception as e:
        MandarAoConsole(ObterMensagensYML(mensagens,"Bot-Erro-Generico","Console",i=e),2)
        q.put("FALHA")
    MandarAoConsole(ObterMensagensYML(mensagens,"BOT-Desligado","Console"),1)

def EstadoProcesso():
    if(server):
        if isinstance(server, subprocess.Popen):
            return server.poll() is None
        if isinstance(server, psutil.Process):
            return server.is_running()
    return False

testServidorLock = threading.Lock()
def TestarConexaoAoServidor(tentativasMax=5):
    global clientJava
    for i in range(tentativasMax):
        if(EstadoProcesso() is False):
            return
        try:
            if portaServidor != '80' or (isinstance(portaServidor,str) and portaServidor.upper() != 'HTTPS'):
                clientJava = JavaServer(ipServidor,int(portaServidor))
            else:   
                clientJava = JavaServer(ipServidor)
            clientJava.status()
            clientJava.query_port = int(portaQuery)
            return True
        except:
            pass
        CV.Delay(10)
    return False 

def MostrarTotalDeJogadores():
    if(not EstadoProcesso()):
        MandarAoConsole("O Servidor NÃO Está Aberto!",2)
        MandarAoDiscord("O Servidor **NÃO** Está **Aberto**!")
        return

    if(not TestarConexaoAoServidor(1)):
        MandarAoConsole("O Servidor NÃO Está Online e/ou Conectado!",2)
        MandarAoDiscord("O Servidor NÃO Está Online e/ou Conectado!")
        return

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
    semJogadores = threading.Event()

    def CronometroInativo():
        tempoInativoAtual = 0
        tempoLimiteEmSegundos = CV.ConverterEmUnidadeLite(tempoInativoLimite,origem="MINUTOS",modo="SEGUNDOS")

        while tempoInativoAtual < tempoLimiteEmSegundos:
            if(not semJogadores.is_set()):
                tempoInativoAtual = 0
                if(servidorFechou.wait(1)):
                    break
                continue

            tempoInativoAtual += 1
            if(tempoInativoAtual == (tempoLimiteEmSegundos / 2)):
                MandarAoConsole(f"O Servidor Já se Encontra a {CV.FormatarTempo(CV.ConverterEmUnidadeLite(tempoInativoAtual),origem="MINUTOS",desc=True)} Sem Atividade!..",1)
                MandarAoDiscord(f"O Servidor Já se Encontra a **{CV.FormatarTempo(CV.ConverterEmUnidadeLite(tempoInativoAtual),origem="MINUTOS",desc=True)}**  Sem **Atividade**!..",NomeIconeServidor())

            if(servidorFechou.wait(1)):
                break

        if(tempoInativoAtual >= tempoLimiteEmSegundos):
            MandarAoConsole(f"O Servidor Está Inativo por {CV.FormatarTempo((tempoInativoAtual / 60),origem="MINUTOS",desc=True)}!..",1)
            MandarAoDiscord(f"O Servidor Está **Inativo** por **{CV.FormatarTempo((tempoInativoAtual / 60),origem="MINUTOS",desc=True)}**!..",NomeIconeServidor())
            CV.Delay(0.5)
            MandarAoConsole("Dada a Configuração, o Servidor será Fechado por Inatividade!",1)
            MandarAoDiscord("Dada a Configuração, o Servidor será **Fechado** por **Inatividade**!",NomeIconeServidor())
            PararServidor()

    def ChecarJogadores():
        def OrdenarJogadores(jogadores):
            jogadoresOrdenados = []
            for jogador in jogadores:
                jogadoresOrdenados.append(f"'**{jogador}**'")
            return ', '.join(jogadoresOrdenados[:-1]) + f' e {jogadoresOrdenados[-1]}' if len(jogadoresOrdenados) > 1 else f'{''.join(jogadoresOrdenados)}'
        
        quantidadeDeJogadores = 0
        listaDeJogadores = []
        while not servidorFechou.is_set() and TestarConexaoAoServidor():
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
                continue

            semJogadores.clear() if quantidadeDeJogadores > 0 else semJogadores.set()
            servidorFechou.wait(1)

    def ChecarServidor():
        servidorNoAr = True
        while not servidorFechou.is_set():
            if abrindoFechando:
                servidorFechou.wait(3)
                continue
            testeServidor = TestarConexaoAoServidor()
            if testeServidor != servidorNoAr:
                if not testeServidor and not servidorFechou.is_set():
                    if servidorNoAr:
                        msg = ObterMensagensYML(mensagens,"Estado-Servidor-Caido","Console-Discord")
                        MandarAoConsole(msg,1)
                        MandarAoDiscord(msg)
                else:
                    if not servidorNoAr:
                        msg = ObterMensagensYML(mensagens,"Estado-Servidor-Reativo","Console-Discord")
                        MandarAoConsole(msg)
                        MandarAoDiscord(msg)
                servidorNoAr = testeServidor
                servidorFechou.wait(3)

    def ChecarInternet():
        estadoInternet = True
        while not servidorFechou.is_set():
            testarInternet = CV.TestarConexaoAInternet(tempoLimite=5,tentativas=3)
            if estadoInternet != testarInternet:
                if not testarInternet:
                    MandarAoConsole(ObterMensagensYML(mensagens,"Estado-Internet-Perdida","Console"),1)
                else:
                    msg = ObterMensagensYML(mensagens,"Estado-Internet-Recuperada","Console-Discord")
                    MandarAoConsole(msg)
                    MandarAoDiscord(msg)
            estadoInternet = testarInternet
            servidorFechou.wait(3)

    threading.Thread(target=ChecarServidor,daemon=True).start()
    threading.Thread(target=ChecarInternet,daemon=True).start()
    threading.Thread(target=ChecarJogadores,daemon=True).start()

    if(tempoInativoLimite > 0):
        threading.Thread(target=CronometroInativo,daemon=True).start()

    with keep.running():
        while EstadoProcesso():
            CV.Delay(1)
    servidorFechou.set()

    MandarAoConsole(ObterMensagensYML(mensagens,"Estado-Servidor-Fechado","Console-Discord"),1)
    MandarAoDiscord(ObterMensagensYML(mensagens,"Estado-Servidor-Fechado","Console-Discord"),NomeIconeServidor())

def ChecarBateria():
    bateria = psutil.sensors_battery()
    if bateria is None:
        return
    return bateria

def MonitorarBateria():
    if ChecarBateria() is None:
        return
    
    contagemInicial = 60
    contagemParaDesligar = contagemInicial
    tempoEsgotado = False
    estadoAnteriorHostTomada = True
    nivelBateriaAtrasado = 100
    nivelBateria = 100
    nivelCritico = False

    # ATIVE AQUI PARA DEBUG: A Bateria Descerá por 1% à Cada 1 Segundo!
    debugTarefa = False

    # SFXs Pois... Deu vontade. '-'
    porAmbientacao = "execute at @a run playsound minecraft:ambient.cave ambient @a"

    while (True):
        bateriaDoHost = ChecarBateria()
        hostNaTomada = bateriaDoHost.power_plugged if not debugTarefa else False
        nivelBateria = bateriaDoHost.percent if not debugTarefa else nivelBateria -1

        if(hostNaTomada != estadoAnteriorHostTomada):
            if(not hostNaTomada):
                MandarAoConsole(ObterMensagensYML(mensagens,"Aviso-Modo-Bateria", "Console-Discord"),1)
                MandarAoDiscord(ObterMensagensYML(mensagens,"Aviso-Modo-Bateria", "Console-Discord"),NomeIconeServidor())

                if(EstadoProcesso()):
                    MandarAoChat(ObterMensagensYML(mensagens,"Aviso-Modo-Bateria","Chat"))
            else:
                MandarAoConsole(ObterMensagensYML(mensagens,"Aviso-Na-Energia", "Console-Discord"))
                MandarAoDiscord(ObterMensagensYML(mensagens,"Aviso-Na-Energia", "Console-Discord"),NomeIconeServidor())

                if(EstadoProcesso()):
                    MandarAoChat(ObterMensagensYML(mensagens,"Aviso-Na-Energia","Chat")) 
            estadoAnteriorHostTomada = hostNaTomada

        if(not hostNaTomada):
            match nivelBateria:
                case 90 | 80 | 70 | 60 | 50 | 45 | 40 | 35 | 30 | 25 | 20 | 15:
                        if(nivelBateriaAtrasado != nivelBateria):
                            MandarAoConsole(ObterMensagensYML(mensagens,"Nivel-Bateria","Console-Discord",i=nivelBateria),1)
                            MandarAoDiscord(ObterMensagensYML(mensagens,"Nivel-Bateria","Console-Discord",i=nivelBateria),NomeIconeServidor())

                            if(EstadoProcesso()):
                                MandarAoChat(ObterMensagensYML(mensagens,"Nivel-Bateria","Chat",i=nivelBateria))
                                if(nivelBateria == 20):
                                    MandarAoConsole(ObterMensagensYML(mensagens,"Nivel-Bateria-Baixa","Console"),1)
                                    MandarAoChat(ObterMensagensYML(mensagens,"Nivel-Bateria-Baixa","Chat"))

            #OPERAÇÃO DE AUTO-DESLIGAMENTO CASO O SERVER ESTEJA ABERTO
            if(EstadoProcesso()):
                if (nivelCritico):
                    if(nivelBateriaAtrasado != nivelBateria and nivelBateriaAtrasado >= 15):
                        MandarAoConsole(ObterMensagensYML(mensagens,"Nivel-Critico","Console-Discord",i=nivelBateria),1)
                        MandarAoDiscord(ObterMensagensYML(mensagens,"Nivel-Critico","Console-Discord",i=nivelBateria),NomeIconeServidor())
                        ExecutarRCON(porAmbientacao)
                        MandarAoChat(ObterMensagensYML(mensagens,"Nivel-Critico","Chat",i=nivelBateria,j=contagemInicial))

                        ExecutarRCON(porAmbientacao)
                        MandarComoTitulo(ObterMensagensYML(mensagens,"Contagem-Para-Desligar","Titulo",i=contagemInicial))

                    if(not tempoEsgotado):
                        contagemParaDesligar -= 1

                    if(contagemParaDesligar > 0):
                        match contagemParaDesligar:
                            case 50 | 40 | 30 | 20 | 10:
                                MandarAoConsole(ObterMensagensYML(mensagens,"Contagem-Para-Desligar","Console-Discord",i=contagemParaDesligar),1)
                                MandarAoDiscord(ObterMensagensYML(mensagens,"Contagem-Para-Desligar","Console-Discord",i=contagemParaDesligar),NomeIconeServidor())
                                MandarAoChat(ObterMensagensYML(mensagens,"Contagem-Para-Desligar","Chat",i=contagemParaDesligar))
                                MandarComoTitulo(ObterMensagensYML(mensagens,"Contagem-Para-Desligar","Titulo",i=contagemParaDesligar))
                                ExecutarRCON(porAmbientacao)
                            case _ if contagemParaDesligar <= 10:
                                if(contagemParaDesligar == 10):
                                    MandarAoConsole(ObterMensagensYML(mensagens,"Contagem-Final-Iniciada","Console-Discord"),1)
                                    MandarAoDiscord(ObterMensagensYML(mensagens,"Contagem-Final-Iniciada","Console-Discord"),NomeIconeServidor())
                                    ExecutarRCON(porAmbientacao)
                                MandarAoChat(ObterMensagensYML(mensagens,"Contagem-Final","Chat",i=contagemParaDesligar))
                                MandarComoTitulo(f"{ObterMensagensYML(mensagens,"Contagem-Final","Titulo",i=contagemParaDesligar)} {"!.." if contagemParaDesligar <= 5 else "..."}")
                    else:
                        CV.Delay(3)
                        if(not tempoEsgotado):
                            ExecutarRCON(porAmbientacao)
                            MandarAoChat(ObterMensagensYML(mensagens,"Fim-Da-Contagem","Chat"))
                            MandarComoTitulo(random.choice(ObterMensagensYML(mensagens,"Ultimas-Palavras")))
                            MandarAoConsole(ObterMensagensYML(mensagens,"Fim-Da-Contagem","Console-Discord"),1)
                            MandarAoDiscord(ObterMensagensYML(mensagens,"Fim-Da-Contagem","Console-Discord"),NomeIconeServidor())
                            CV.Delay(2)
                            PararServidor()
        else:
            contagemParaDesligar = contagemInicial

        tempoEsgotado = contagemParaDesligar <= 0
        nivelBateriaAtrasado = nivelBateria
        nivelCritico = nivelBateria <= 15
        CV.Delay(1)
        
def IniciarServidor():
    def Iniciar():
        global server, abrindoFechando
        abrindoFechando = True
        musicaDeFundo = TocarSom(musicaTarefa,0.2)

        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar","Console-Discord"),1)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Iniciar","Console-Discord"),NomeIconeServidor())
        openServer =  None
        caminhoJava = shutil.which('java')
        if(caminhoJava):
            linhasExecucao = [caminhoJava, *argumentosDeExecucao, '-jar', arquivoExecucao, 'nogui']
            for processo in psutil.process_iter(['pid','cmdline']):
                try:
                    linhaProcesso = " ".join(processo.info['cmdline']).lower()
                    if(any (linha in linhaProcesso for linha in linhasExecucao) and arquivoExecucao in linhaProcesso and processo.cwd() == os.getcwd()):
                        openServer = processo
                except:
                    pass
            if(openServer):
                MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Ja-Aberto","Console",i=processo.pid),1)
                server = openServer
            else:
                server = subprocess.Popen(linhasExecucao,creationflags=subprocess.CREATE_NEW_CONSOLE)
                CV.Delay(5)
            servidorConectado = False
            tentativasDeConexao = 0
            MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Conexao-IP","Console-Discord",i=ipServidor,j=portaServidor),1)
            MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Conexao-IP","Console-Discord",i=ipServidor,j=portaServidor))
            while(tentativasDeConexao < 60 and EstadoProcesso()):
                if(TestarConexaoAoServidor()):
                    MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar-IP-Ativo","Console-Discord"))
                    MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Iniciar-IP-Ativo","Console-Discord"))
                    servidorConectado = True
                    break
                tentativasDeConexao += 1
                CV.Delay(1)
            if(EstadoProcesso()):
                if(not servidorConectado):
                    MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar-IP-Falha","Console-Discord"),2)
                    MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Iniciar-IP-Falha","Console-Discord"),NomeIconeServidor())
                threading.Thread(target=ChecarEstadoServidor, daemon=True).start()
            else:
                MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Falha","Console-Discord"),2)
                MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Falha","Console-Discord"),NomeIconeServidor())
        if(musicaDeFundo):
            musicaDeFundo.stop()
        abrindoFechando = False

    if not os.path.isfile(arquivoExecucao):
        MandarAoConsole(f"O Arquivo do Servidor '{arquivoExecucao}' NÃO Pôde Ser Encontrado!",2)
        return

    if(abrindoFechando):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"),2)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"),NomeIconeServidor())
        return
    
    if(CV.TestarConexaoAInternet() is False):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Sem-Internet","Console"),2)
        return
        
    if(EstadoProcesso()):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Ja-Aberto","Console-Discord"),2)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Ja-Aberto","Console-Discord"),NomeIconeServidor())
        return

    if(ChecarBateria() and not ChecarBateria().power_plugged):
            MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Modo-Bateria","Console-Discord"),1)
            MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Modo-Bateria","Console-Discord"),NomeIconeServidor())
    
    threading.Thread(target=Iniciar,daemon=True).start()

    tempoConvertidoParaDesligar = CV.FormatarTempo(tempoInativoLimite,origem="MINUTOS",desc=True)

    if(tempoInativoLimite > 0):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Tempo-Inativo","Console-Discord",i=tempoConvertidoParaDesligar),1)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Iniciar-Tempo-Inativo","Console-Discord",i=tempoConvertidoParaDesligar)),NomeIconeServidor()
    

def PararServidor(forcarParada = False):
    def Parar(f):
        global server, abrindoFechando
        abrindoFechando = True
        musicaDeFundo = TocarSom(musicaTarefa,0.2)
        tempoLimite = 90
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Parar","Console-Discord"),1)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Parar","Console-Discord"),NomeIconeServidor())
        
        contagem = 0
        while(EstadoProcesso()):
            if(f):
                break
            match contagem:
                case 0:
                    sucessoRCON, respostaRCON = ExecutarRCON("stop")
                    if(not sucessoRCON):
                        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Parar-RCON-Inativo","Console-Discord"),2)  
                        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Parar-RCON-Inativo","Console-Discord"),NomeIconeServidor())
                        break
                case _ if contagem == (tempoLimite / 2):
                    MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Parar-Longo-Tempo","Console-Discord",i=CV.FormatarTempo(tempoLimite-contagem,desc=True)),1)
                    MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Parar-Longo-Tempo","Console-Discord",i=CV.FormatarTempo(tempoLimite-contagem,desc=True)),NomeIconeServidor())
                case _ if contagem == tempoLimite:
                    MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Parar-Tempo-Limite","Console-Discord"),1)
                    MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Parar-Tempo-Limite","Console-Discord"),NomeIconeServidor())
                    break
            CV.Delay(1)
            contagem += 1
    
        if(EstadoProcesso()):
            MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Parar-Forcar-Parada","Console-Discord"),1)
            MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Parar-Forcar-Parada","Console-Discord"),NomeIconeServidor())
            subprocess.Popen("TASKKILL /F /PID {} /T".format(server.pid), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
            server.wait()

        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Parar-Concluida","Console-Discord"))
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Parar-Concluida","Console-Discord"))

        if(musicaDeFundo):
            musicaDeFundo.stop()
        abrindoFechando = False

    if(abrindoFechando):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"),2)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"))
        return

    if(EstadoProcesso() is False):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Nao-Aberto","Console-Discord"),2)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Nao-Aberto","Console-Discord"),NomeIconeServidor())
        return
    
    threading.Thread(target=lambda: Parar(forcarParada),daemon=True).start()

def ReiniciarServidor():
    def Reiniciar():
        global abrindoFechando
        PararServidor()
        while(EstadoProcesso() or abrindoFechando):
            CV.Delay(1)
        abrindoFechando = True
        CV.Delay(2)
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Reiniciar","Console-Discord"),1)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Reiniciar","Console-Discord"))
        CV.Delay(5)
        abrindoFechando = False
        IniciarServidor()

    if(abrindoFechando):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"),2)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Em-Andamento","Console-Discord"))
        return

    if(EstadoProcesso() is False):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Nao-Aberto","Console-Discord"),2)
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Nao-Aberto","Console-Discord"),NomeIconeServidor())
        return

    threading.Thread(target=Reiniciar,daemon=True).start()

def FecharControlador():
    global abrindoFechando
    if(EstadoProcesso() is True or abrindoFechando):
        MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Terminal-Servidor-Aberto","Console"),2)
        return
    abrindoFechando = True
    MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Terminal","Console-Discord"),1)
    CV.Delay(1)
    if(EstadoBot()):
        MandarAoDiscord(ObterMensagensYML(mensagens,"Tarefa-Terminal","Console-Discord"))
        MandarAoDiscord(ObterMensagensYML(mensagens,"BOT-Desligado","Discord"))
        asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
        CV.Delay(2)
    MandarAoConsole(ObterMensagensYML(mensagens,"Tarefa-Terminal-Concluida","Console"))
    ModYML(dirArquivoConfigs,"SOFTSHUT","Yes")
    CV.Delay(1)
    TocarSom(musicaCreditos,0.1)
    CV.Creditos()
    CV.Delay(2)
    os.kill(os.getpid(), signal.SIGTERM)

def Main():
    def tentouFecharJanela():
        if(EstadoProcesso()):
            messagebox.showerror("Operação Negada",ObterMensagensYML(mensagens,"Tarefa-Terminal-Servidor-Aberto","Console"))
        else:
            FecharControlador()
    
    def JanelaComandos():
        def EnviarComandoDigitado():
            comandoDigitado = entry.get().replace('/','')
            if(len(comandoDigitado) < 1):
                messagebox.showerror("Operação Negada","NENHUM Comando Foi DIGITADO!")
                return
            if(not EstadoProcesso()):
                messagebox.showerror("Operação Negada","O Servidor NÃO Está ABERTO!")
                return
            if(not TestarConexaoAoServidor(1)):
                messagebox.showerror("Operação Negada","O Servidor NÃO Está CONECTADO!")
                return
            MandarAoConsole(f'Comando Enviado Pelo Console: /{comandoDigitado}!',1)
            MandarAoDiscord(f'Comando Enviado Pelo **Console**: _/{comandoDigitado}!_')
            sucessoRCON, respostaRCON = ExecutarRCON(comandoDigitado)
            if(not sucessoRCON):
                messagebox.showerror("Falha na Operação","O RCON do Servidor Apresentou uma Falha!")
                return
            if(respostaRCON):
                messagebox.showinfo("Operação Bem-Sucedida",f"Resposta do Servidor: {respostaRCON}")
            window.destroy()

        window = tk.Toplevel()
        window.title("MSC: Comandos")
        window.resizable(True,True)

        style = ttk.Style(window)
        sv_ttk.set_theme("dark")

        label = ttk.Label(window, text="Insira o Comando Desejado Aqui:")
        label.pack(padx=10, pady=5,expand=True)

        entry = ttk.Entry(window,width=64)
        entry.pack(padx=10, pady=5,expand=True,fill="x")

        button = ttk.Button(window, text="Enviar Para o Servidor!",command=EnviarComandoDigitado)
        button.pack(padx=10, pady=5,expand=True,fill="x")

        try:
            icoServidor = Image.open(os.path.join(CV.DiretorioAtual(),"server-icon.png"))
            diretorioParaSalvar = rf"{pastaData}\server-icon.ico"
            icoServidor.save(diretorioParaSalvar,format="ICO", sizes=[(128,128),(64,64),(32,32),(16,16)],bitmap_format="bmp")
            window.iconbitmap(os.path.abspath(diretorioParaSalvar))
        except:
            if(os.name == "nt"):
                try:
                    window.iconbitmap(sys.executable)
                except:
                    pass
        
        window.update()
        window.minsize(window.winfo_width(),window.winfo_height())
    
    pygame.mixer.init()
    myappid = f'CV.MinecraftServerController.{uuid.uuid4()}'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    CV.Limpar()
    LinhasBinarias(15)
    CV.Limpar()
        
    if not os.path.isfile(arquivoExecucao):
        MandarAoConsole(f"O Arquivo do Servidor '{arquivoExecucao}' NÃO Pôde Ser Encontrado!",2,False)
        keyboard.wait('esc')
        sys.exit()
    if(CV.LerDadosYML(dirArquivoConfigs,"SOFTSHUT") == "Yes"):
        CV.ModificarDadosYML(dirArquivoConfigs,"SOFTSHUT",valor="No")
    else:
        MandarAoConsole(ObterMensagensYML(mensagens,"Terminal-Fechado-Abruptamente","Console"),2)
        CV.Delay(2)
        CV.Limpar()

    tentativasConexao = 0
    tempoAteNovaTentativa = 10
    while(CV.TestarConexaoAInternet() is False):
        MandarAoConsole(ObterMensagensYML(mensagens,"Terminal-Sem-Internet","Intro"),2) if tentativasConexao < 3 else MandarAoConsole(random.choice(ObterMensagensYML(mensagens,"Terminal-Sem-Internet","Nag")),2)
        CV.Delay(2)
        MandarAoConsole(ObterMensagensYML(mensagens,"Terminal-Sem-Internet","Loop",i=tempoAteNovaTentativa),1)
        tentativasConexao += 1
        CV.Delay(tempoAteNovaTentativa)
        CV.Limpar()

    if(CV.LerDadosYML(dirArquivoConfigs,"DISCOBOT") == "Yes"):
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
        MandarAoConsole(ObterMensagensYML(mensagens,"Terminal-Sem-Discord","Console",i=arquivoConfigs),1)        

    threading.Thread(target=MonitorarBateria, daemon=True).start()

    print(f"{(f'『{CV.Fore.GREEN}..:'+nomServidor.upper()+f':..{CV.Style.RESET_ALL}』').center(50,'=')}\n")
    MandarAoConsole("Abrindo Janela de Opções...",3,False)
    TocarSom(somPainelOpcoes,0.1)

    root = tk.Tk()
    root.title("MSC")
    root.resizable(True,True)
    root.eval('tk::PlaceWindow . center')

    try:
        icoServidor = Image.open(os.path.join(CV.DiretorioAtual(),"server-icon.png"))
        diretorioParaSalvar = rf"{pastaData}\server-icon.ico"
        icoServidor.save(diretorioParaSalvar,format="ICO", sizes=[(128,128),(64,64),(32,32),(16,16)],bitmap_format="bmp")
        root.iconbitmap(os.path.abspath(diretorioParaSalvar))
    except:
        if(os.name == "nt"):
            try:
                root.iconbitmap(sys.executable)
            except:
                pass

    style = ttk.Style(root)
    sv_ttk.set_theme("dark")

    nomeDoServidor = ttk.Label(root, text=nomServidor,anchor="center",font=("Arial", 12, "bold")) 
    btnIniciar = ttk.Button(root, text="Iniciar Servidor",command=IniciarServidor)
    btnParar = ttk.Button(root, text="Parar o Servidor",command=PararServidor)
    btnForcar = ttk.Button(root, text="(F) Parar o Servidor",command=lambda:PararServidor(True))
    btnReiniciar = ttk.Button(root, text="Reiniciar o Servidor",command=ReiniciarServidor)
    btnJogadores = ttk.Button(root, text="Mostrar Jogadores",command=MostrarTotalDeJogadores)
    btnComandos = ttk.Button(root, text="Enviar um Comando",command=JanelaComandos)
    btnFechar = ttk.Button(root, text="Fechar o Controlador",command=FecharControlador)
    
    nomeDoServidor.pack(fill="both",padx=10, pady=5,expand=True)
    btnIniciar.pack(fill="both",padx=10, pady=5,expand=True)
    btnParar.pack(fill="both",padx=10, pady=5,expand=True)
    btnForcar.pack(fill="both",padx=10, pady=5,expand=True)
    btnReiniciar.pack(fill="both",padx=10, pady=5,expand=True)
    btnJogadores.pack(fill="both",padx=10, pady=5,expand=True)
    btnComandos.pack(fill="both",padx=10, pady=5,expand=True)
    btnFechar.pack(fill="both",padx=10, pady=5,expand=True)

    root.protocol("WM_DELETE_WINDOW",tentouFecharJanela)

    root.update()
    root.minsize(root.winfo_width(),root.winfo_height())

    if(EstadoBot()):
        MandarAoDiscord(f'**{prefixComandos}iniciar** - _Abrir o Servidor_\n**{prefixComandos}parar** -' 
        f'_Fechar o Servidor_\n**{prefixComandos}fparar** - _Forçar o Fechamento_\n**{prefixComandos}reiniciar** -' 
        f'_Reiniciar o Servidor_\n**{prefixComandos}rcon "comando"** - _Enviar Comandos ao Servidor_'
        f'\n**{prefixComandos}jogadores** - _Mostrar Jogadores Atuais no Servidor_'
        )

    root.mainloop()

Main()