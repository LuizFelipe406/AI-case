README para API Mestre de RPG
Introdução
Bem-vindo à API do Mestre de RPG, uma interface de programação de aplicativos que integra a capacidade criativa da OpenAI para construir e conduzir sessões de RPG. Esta API permite que você crie partidas de RPG dinâmicas e envolventes para até 4 jogadores, gerenciando personagens e histórias através de interações com a inteligência artificial.

Como começar
Iniciando um Jogo
Para começar um novo jogo de RPG, você deve fazer uma requisição POST para a seguinte rota:

bash
POST /game/start
Requisição
No corpo da sua requisição, inclua um JSON com a seguinte estrutura:

json
{
  "playerList": ["NomeDoJogador1", "NomeDoJogador2", "NomeDoJogador3", "NomeDoJogador4"]
}
Restrições
playerList deve ser um array contendo de 1 a 4 nomes de jogadores.
Resposta
Se a requisição for bem-sucedida, você receberá uma resposta com status 200 OK e um corpo de resposta contendo:

gameId: O ID único da partida criada.
characters: Um array contendo cada personagem do RPG associado aos jogadores fornecidos.
story: A história inicial do RPG.
Jogando uma Partida
Para jogar e avançar na história da sua partida de RPG, envie uma requisição POST para a seguinte rota:

arduino
POST /game/play/<int:game_id>
Requisição
Inclua no corpo da requisição um JSON com a seguinte estrutura:

json
{
  "input": "Texto com as instruções ou ações desejadas para a próxima parte do RPG"
}
Resposta
A resposta bem-sucedida retorna status 200 OK com um corpo de resposta contendo:

game_id: O ID da partida.
characters: Um array atualizado contendo cada personagem do RPG.
full_story: A história completa da partida até o momento.
round_story: A história que aconteceu especificamente na rodada atual.
on_the_next_round: Sugestões do que você pode incluir no seu próximo input para continuar a partida de RPG.
Erros
Em caso de erro, por exemplo, se o GPT não retornar as informações no formato esperado, a rota pode retornar status 500 Internal Server Error acompanhado de uma mensagem explicativa.

Rodando a Aplicação
Para executar a API Mestre de RPG, você deve ter o Docker instalado em sua máquina. Siga os passos abaixo para colocar a aplicação para rodar:

Abra o terminal ou prompt de comando.
Navegue até a pasta raiz do projeto.
Execute o comando:
shell
docker-compose up -d --build
Este comando irá construir e iniciar dois containers Docker:

DB: O container responsável por gerenciar o banco de dados.
API: O container onde a aplicação de fato será executada.