<h1>API Mestre de RPG</h1>

<section>
    <h2>Introdução</h2>
    <p>Bem-vindo à API do Mestre de RPG, uma interface de programação de aplicativos que integra a capacidade criativa da OpenAI para construir e conduzir sessões de RPG. Esta API permite que você crie partidas de RPG dinâmicas e envolventes para até 4 jogadores, gerenciando personagens e histórias através de interações com a inteligência artificial.</p>
</section>

<section>
    <h2>Como começar</h2>
    <h3>Iniciando um Jogo</h3>
    <p>Para começar um novo jogo de RPG, você deve fazer uma requisição POST para a seguinte rota:</p>
    <pre><code>POST /game/start</code></pre>
    <h4>Requisição</h4>
    <p>No corpo da sua requisição, inclua um JSON com a seguinte estrutura:</p>
    <pre><code>{
  "playerList": ["NomeDoJogador1", "NomeDoJogador2", "NomeDoJogador3", "NomeDoJogador4"]
}</code></pre>
    <h4>Restrições</h4>
    <p><code>playerList</code> deve ser um array contendo de 1 a 4 nomes de jogadores.</p>
    <h4>Resposta</h4>
    <p>Se a requisição for bem-sucedida, você receberá uma resposta com status <code>200 OK</code> e um corpo de resposta contendo:</p>
    <ul>
        <li><code>gameId</code>: O ID único da partida criada.</li>
        <li><code>story</code>: A história inicial do RPG.</li>
        <li><code>characters</code>: Um array contendo cada personagem do RPG associado aos jogadores fornecidos.</li>
    </ul>
    <h3>Jogando uma Partida</h3>
    <p>Para jogar e avançar na história da sua partida de RPG, envie uma requisição POST para a seguinte rota:</p>
    <pre><code>POST /game/play/&lt;int:game_id&gt;</code></pre>
    <h4>Requisição</h4>
    <p>Inclua no corpo da requisição um JSON com a seguinte estrutura:</p>
    <h4>Caso essa seja a primeira rodada da partida, não é necessário enviar nenhum Input.</h4>
    <pre><code>{
  "input": "Texto com as instruções ou ações desejadas para a próxima parte do RPG"
}</code></pre>
    <h4>Resposta</h4>
    <p>A resposta bem-sucedida retorna status <code>200 OK</code> com um corpo de resposta contendo:</p>
    <ul>
        <li><code>game_id</code>: O ID da partida.</li>
        <li><code>round_story</code>: A história que aconteceu especificamente na rodada atual.</li>
        <li><code>on_the_next_round</code>: Sugestões do que você pode incluir no seu próximo input para continuar a partida de RPG.</li>
        <li><code>ending</code>: Final da história caso o Vilão tenha sido derrotado</li>
        <li><code>characters</code>: Um array atualizado contendo cada personagem do RPG.</li>
    </ul>
    <h4>Erros</h4>
    <p>Em caso de erro, por exemplo, se o GPT não retornar as informações no formato esperado, a rota pode retornar status <code>500 Internal Server Error</code> acompanhado de uma mensagem explicativa.</p>
    <h3>Acessando a história de uma partida</h3>
    <p>Para ver a história completa da sua partida de RPG, envie uma requisição GET para a seguinte rota:</p>
    <pre><code>GET /game/story/&lt;int:game_id&gt;</code></pre>
    <h4>Resposta</h4>
    <p>A resposta bem-sucedida retorna status <code>200 OK</code> com um corpo de resposta contendo:</p>
    <ul>
        <li><code>game_id</code>: O ID da partida.</li>
        <li><code>statu</code>: O status atual da partida</li>
        <li><code>story</code>: A história completa da partida</li>
        <li><code>characters</code>: Um array contendo cada personagem da partida</li>
    </ul>
</section>

<section>
    <h2>Rodando a Aplicação</h2>
    <p>Para executar a API Mestre de RPG, você deve ter o Docker instalado em sua máquina. Siga os passos abaixo para colocar a aplicação para rodar:</p>
    <ol>
        <li>Abra o terminal ou prompt de comando.</li>
        <li>Navegue até a pasta raiz do projeto.</li>
        <li>Execute o comando:</li>
    </ol>
    <pre><code>docker-compose up -d --build</code></pre>
    <p>Este comando irá construir e iniciar dois containers Docker:</p>
    <ul>
        <li><code>DB</code>: O container responsável por gerenciar o banco de dados.</li>
        <li><code>Aplicação</code>: O container onde a aplicação de fato será executada.</li>
    </ul>
</section>
