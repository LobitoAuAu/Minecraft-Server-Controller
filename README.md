## 📌 [SOBRE]:
Controlador Automatizado de Servidor Minecraft, com Integração ao Discord via BOT! (Programado via Linguagem Python, Ver. 3.13.11).

<img width="1689" height="835" alt="image" src="https://github.com/user-attachments/assets/92032596-de16-4c6c-9c43-a179d8711ea6" />

## 📚 [TUTORIAL]: Instalação + Configuração

Arraste o script 'MinecraftServerController.yml' e a pastas 'MSCData' & 'Bibliotecas' para dentro da pasta do servidor. *(A mesma cujo contenha o arquivo .jar do seu servidor. Ex.: "server.jar")*.

Quando aberto o Controlador pela primeira vez *- caso presente o arquivo 'server.properties' -* as configurações já presentes no servidor *(IP, Porta & Senha RCON utilizados)* serão automaticamente atribuídos ao arquivo de configuração 'mscserver_config.yml'.

### **Dentro deste arquivo, estarão contidas as seguintes variáveis:**

#### [Configurações do Servidor]
- **`NOMESERV`**  
  Nome do Servidor  
  *Padrão:* `Mine-Server`

- **`JAVARGS`**  
  Argumentos do Java (JVM Arguments) na inicialização do servidor

- **`JAVA`**  
  Nome do arquivo `.jar` do servidor  
  *Padrão:* `server.jar`

- **`IPSERVER`**  
  IP do Servidor  
  *Padrão:* `localhost`

- **`AUTOSHUT`**  
  Quando Inativo... Tempo Até Auto-Desligar o Servidor Em Minutos (OPCIONAL!)
  *Padrão:* `45`
  
- **`PORTSERVER`**  
  Porta do Servidor  
  *Padrão:* `25565`

#### [Configurações RCON]
- **`RCONIP`**  
  IP para conexão ao RCON  
  *Padrão: IP do servidor* 

- **`RCONPORT`**  
  Porta para conexão ao RCON  
  *Padrão:* `25575`

- **`RCONPASS`**  
  Senha para login no RCON  
  *Padrão: A mesma configurada no arquivo `server.properties`*

#### [Configurações QUERY]
- **`QUERYPORT`**  
  Porta para conexão ao RCON  
  *Padrão: Porta do Servidor* 
  
#### [Integração com Discord]
- **`DISCOBOT`**  
  Ativa ou desativa a integração com o Discord  
  *Opções:* `Yes` / `No`

- **`BOTTOKEN`**  
  Token secreto do Bot do Discord  
  *NUNCA compartilhe esta chave!*

- **`BOTCHANNEL`**  
  ID do Canal do Servidor p/ Interação do Bot

- **`ADMROLE`**  
  ID do Cargo p/ Controlar o Bot Via Comandos  

Quaisquer mensagens exibidas pelo controlador podem ser alteradas pelo arquivo de mensagens **'mensagens.yml'**.
  
## 🌐 [TUTORIAL]: Criação e Integração do Bot do Discord

Crie uma Nova Aplicação em https://discord.com/developers/applications/ clicando em: **New Application**, e dê o nome desejado a esta.

Na aplicação criada, vá na aba **Installation** no menu à direita. Desabilite a opção **User Install**, e deixe o campo **Install Link** como **None** (nenhum).

Na aba de configurações do Bot (**Bot**), ative as opções **SERVER MEMBERS INTENT** e **MESSAGE CONTENT INTENT**.

Ainda na mesma aba, para adquirir um token para o Bot, Clique na caixa **Reset Token** para gerar um token novo.

De volta no **server_config.env**, cole o token adquirido na linha **'BOTTOKEN'**.

De volta na página, na aba **General Information**, copie o **Application ID** e o cole - _CTRL+V_ - na seguinte página: https://scarsz.me/authorize. Aberta a Aba no seu Discord, selecione o servidor desejado e clique em **Autorizar**.

No seu Discord, acesse nas **Configurações de Usuário** - Pela engrenagem localizada no canto inferior esquerdo - e vá na aba **Avançado**. Nesta, habilite a checagem **Modo Desenvolvedor**.

No Servidor, clique com o botão direito em cima do canal desejado para o Bot, e clique em: **Copiar ID do Canal**. No **'mscserver_config.yml'**, cole o ID do Canal na linha **'BOTCHANNEL'**.

Para escolher um cargo permitido de usar os comandos do Bot, no servidor, clique com o botão direito em cima do cargo desejado, e clique em: **Copiar ID do Cargo**. No **'mscserver_config.yml'**, cole o ID cargo na linha **'ADMROLE'**.
