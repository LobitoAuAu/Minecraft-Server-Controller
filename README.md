# Minecraft-Server-Controller

## 📌 [SOBRE]:
Controlador Automatizado de Servidor Minecraft, com Integração ao Discord via BOT! (Programado via Linguagem Python, Ver. 3.13.11).

## 📚 [TUTORIAL]: Instalação + Configuração

Arraste os arquivos 'MinecraftServerController.exe', 'server_config.env' & 'mensagens.yml' para dentro da pasta do servidor. *(A mesma cujo contenha o arquivo .jar do seu servidor. Ex.: "server.jar")*.

Quando aberto o Controlador pela primeira vez *- caso presente o arquivo 'server.properties' -* as configurações já presentes no servidor *(IP, Porta & Senha RCON utilizados)* serão automaticamente atribuidos ao arquivo de configuração 'server_config.env'.

### **Dentro deste arquivo, estarão contidas as seguintes variáveis:**

#### [Configurações do Servidor]
- **`NOMESERV`**  
  Nome do Servidor  
  *Padrão:* `Mine-Server`

- **`JAVA`**  
  Nome do arquivo `.jar` do servidor  
  *Padrão:* `server.jar`

- **`RAM`**  
  Quantidade de memória RAM utilizada pelo servidor  
  *Padrão:* `4GB` ou `4096M`

- **`IPSERVER`**  
  IP do Servidor  
  *Padrão:* `localhost`

- **`PORTSERVER`**  
  Porta do Servidor  
  *Padrão:* `25565`

#### [Configurações RCON]
- **`RCONIP`**  
  IP para conexão ao RCON  
  *Padrão:* IP do servidor

- **`RCONPORT`**  
  Porta para conexão ao RCON  
  *Padrão:* `25575`

- **`RCONPASS`**  
  Senha para login no RCON  
  *Padrão: A mesma configurada no arquivo `server.properties`*
  
#### [Integração com Discord]
- **`DISCOBOT`**  
  Ativa ou desativa a integração com o Discord  
  *Opções:* `Yes` / `No`

- **`BOTTOKEN`**  
  Token secreto do Bot do Discord  
  *NUNCA compartilhe esta chave!*

- **`BOTCHANNEL`**  
  ID do canal do Discord utilizado para interação com o bot

- **`ADMROLE`**  
  Nome do cargo permitido a controlar o bot via comandos  
  *Padrão:* `Adm`

#### [Atalhos de Teclado]
- **`HOTSTART`**  
  Atalho para iniciar o servidor  
  *Padrão:* `ctrl+i`

- **`HOTSTOP`**  
  Atalho para desligar o servidor normalmente  
  *Padrão:* `ctrl+p`

- **`HOTFSTOP`**  
  Atalho para forçar o desligamento do servidor  
  *Padrão:* `ctrl+shift+p`

- **`HOTRESTART`**  
  Atalho para reiniciar o servidor  
  *Padrão:* `ctrl+r`

- **`HOTCLOSE`**  
  Atalho para fechar o Controlador  
  *(FECHE O CONTROLADOR PELO ATALHO!)*  
  *Padrão:* `ctrl+l`
