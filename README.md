# btax
## Desenvolvedores
- Lauro Pimentel
- João Henrique
## Requisitos para rodar o projeto
- **Python 3.6+**
- **Django 3.2**
- Banco de dados **PostgreSQL**
- **PIP** para gerenciamento dos pacotes python
- **Virtualenv** para isolamento do ambiente

## Configurações necessárias para funcionamento do projeto
### **Introdução**
Para seu correto funcionamento em ambientes de desenvolvimento e produção diferentes, o projeto busca algumas variáveis de ambiente. Isso pode ser visto dentro dos arquivos **btax/settings.py** através do usuo do comando **os.environ['nome_variavel']**.

Como estamos usando o **virtualenv** para criação dos ambientes virtuais, podemos criar essas variáveis isoladamente dentro de cada um deles. Essas varíáveis são criadas dentro do arquivo **postactivate** e destruídas dentro do arquivo **predeactivate**, que se encontra na pasta **bin** dentro da pasta criada pelo virtualenv para o projeto. Por exemplo, se a configuração do virtualenv está setada para criar as pastas dos ambientes virtuais dentro de **/[pasta_do_usuario]/envs**, então os arquivos se encontram em **/[pasta_do_usuario]/envs/btax/bin**.

### **Configuração**
Como o projeto necessita de algumas variáveis booleanas para ativar ou não determinada função, no arquivo settings.py fazemos apenas uma verificação se a variável existe ou não no ambiente, retornando assim um True ou False para usarmos nas variáveis do sistema que necessitam desse tipo de valor. Por exemplo, para a variável DEBUG, verificamos dentro do settings.py:
```python
# Verificamos se a variável de ambiente DEBUG existe dentro de environ.
# Se sim, DEBUG recebe True. Se não, DEBUG recebe False.
DEBUG = 'DEBUG' in os.environ
```
- **DEBUG:** Valor Booleano. Define se o projeto está em modo DEBUG (DESENVOLVIMENTO) ou não (PRODUÇÃO).

- **ALLOWED_HOSTS:** String com dómínios separados por vírgula. Informa os domínios aceitos pelo projeto.

- **USE_AWS_S3:** Valor booleano. Define se o projeto deve usar as configurações do S3 ou não. Se em ambiente de desenvolvimento, essa variável não deve ser setada, fazendo com que o projeto salve arquivos localmente.

- **IN_PRODUCTION:** Valor booleano. Usado para diferenciar o projeto principal (produção) do de testes (desenvolvimento) no servidor, mantendo as pastas separadas dentro do bucket do S3. Em ambiente de desenvolvimento local, essa varíavel não deve ser setada nas variáveis de ambiente.

- **DATABASE_NAME:** Nome da database no banco de dados usada pelo sistema.

- **DATABASE_USER:** Usuário usado na conexão com o banco de dados.

- **DATABASE_PASSWORD:** Senha do usuário usado na conexão com o banco de dados.

- **DATABASE_HOST:** Host onde está localizado o banco de dados.

- **DATABASE_PORT:** Porta do banco de dados

- **STATIC_ROOT:** Caminho para os arquivos estáticos do sistema (CSS, JS, imagens)

- **DATABASE_MONGODB_NAME:** Nome do database que será criado no MongoDb Cloud, em desenvolvimento, usar o valor 'testes'

- **TS_CNPJ:** CNPJ da conta na TecnoSpeed que será usada para conexão com a API.

- **TS_TOKEN:** TOKEN da conta na TecnoSpeed que será usada para conexão com a API.

- **TS_PLUGBOELTO_BASE_URL:** URL da api de boletos da TecnoSpeed. Em ambiente dev, usar https://homologacao.plugboleto.com.br/api/v1/

### **Ambiente Configurado no Servidor AWS**

Além das configurações acima, apenas no servidor de produção e de testes na AWS, são usadas as seguintes tecnologias:
- **Supervisor:** Gerenciador de processos usado para controlar **start**, **stop** e **restart** do projeto.
- **Gunicorn:** Servidor para aplicações Django.
- **Ngnix:** Servidor web que funciona como proxy entre as requisições dos clientes e o Gunigorn.
