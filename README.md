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

Por padrão, o servidor virá utilizando apenas 4GB de RAM. Tal propriedade pode ser alterada no campo **RAM** do arquivo de configuração!
Quaisquer mensagens exibidas pelo controlador podem ser alteradas pelo arquivo de mensagens **'mensagens.yml'**.
  
## 🌐 [TUTORIAL]: Criação e Integração do Bot do Discord

Crie uma Nova Aplicação em https://discord.com/developers/applications/ clicando em: **New Application**, e dê o nome desejado a esta.

Na aplicação criada, vá na aba **Installation** no menu à direita. Desabilite a opção **User Install**, e deixe o campo **Install Link** como **None** (nenhum).

Na aba de configurações do Bot (**Bot**), ative as opções **SERVER MEMBERS INTENT** e **MESSAGE CONTENT INTENT**.

Ainda na mesma aba, para adquirir um token para o Bot, Clique na caixa **Reset Token** para gerar um token novo.

De volta no **server_config.env**, cole o token adquirido na linha **'BOTTOKEN'**.

De volta na página, na aba **General Information**, copie o **Application ID** e o cole - _CTRL+V_ - na seguinte página: https://scarsz.me/authorize. Aberta a Aba no seu Discord, selecione o servidor desejado e clique em **Autorizar**.

No seu Discord, acesse nas **Configurações de Usuário** - Pela engrenagem localizada no canto inferior esquerdo - e vá na aba **Avançado**. Nesta, habilite a checagem **Modo Desenvolvedor**.

No Servidor, clique com o botão direito em cima do canal desejado para o Bot, e clique em: **Copiar ID do Canal**. No **server_config.env**, cole o ID do Canal na linha **'BOTCHANNEL'**.

Para escolher um cargo permitido de usar os comandos do Bot,  No **server_config.env**, digite o nome do cargo na linha **'ADMROLE'**.
