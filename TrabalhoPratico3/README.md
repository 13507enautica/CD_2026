# Trabalho Prático Fase 3 (Grupo 9)  
  
Curso : Computação Distribuída  
Grupo: 9  
Estudantes Autores : Duarte Vale Nº13507, Guilherme Bento Nº13744  
Date : 15/06/2026  
Repository URL : Link(https://github.com/13507enautica/CD_2026)  
---


## Introdução
Este relatório descreve a terceira e última fase do projeto final da unidade curricular de Computação Distribuída, para o qual se pretende finalizar a adaptação do projeto final de Programação Web para este mesmo funcionar através de um ambiente de contentores, desta vez com a interface de uma dashboard por parte front-end do trabalho para verificar continuamente uma série de sensores e atuadores IoT (Internet of Things).  


## Metodologia
O trabalho original para a unidade curricular de Programação Web (2024/2025) há sido realizado pelo Grupo 12 do suposto ano letivo (João Pires, Duarte Vale, Francisca Ricardo, Pedro Vingadas) com o propósito de gestão de uma rede de embarcações e estadías náuticas num porto escolar fictício.  
  
Esta fase do trabalho visa ainda o ambito de alterar o trabalho prático do semestre passado (ano passado neste caso), mas foca-se principalmente na implementação da leitura de sensores e atuadores com base em tópicos MQTT (Message Queuing Telemetry Transport), para o qual foi desenvolvida uma página única pelo front-end da aplicação que demonstra os dados disponibilizados pelo devido tópico fornecido, onde os seus valores serão atualizados a cada 20 segundos de presença na página. Deste modo, a informação dada mantêm-se relativamente consistente com a informação que o dado sensor disponibiliza.  


## Estrutura de Ficheiros
• Ficheiro README.md (Relatório de trabalho)  
• Pasta "docker_rotas"  
- | Pasta "servidor_docker_backend" (Ficheiros de backend do servidor, destinados para o seu próprio contentor)  
- | Pasta "servidor_docker_db" (Ficheiros da base de dados do servidor, destinados para o seu próprio contentor)  
- | Ficheiro "docker-compose.yaml" (Configurações de contentores por modo de um ficheiro docker-compose)  

## Instruções de Uso
O projeto (com exceção do trabalho das aulas 1 e 2) implica não só o uso básico do código desenvolvido, mas o mesmo também deverá ser utilizado dentro de um ambiente de contentores (Docker ou Podman) para o qual existe a presença do ficheiro 'compose'.  
  
• Descarregar o código de projeto presente no repositório  
• Descarregar a aplicação [Docker Desktop](https://www.docker.com/products/docker-desktop/)  
<img src="https://i.imgur.com/LNmSqrW.png" alt="Página de download para a aplicação Docker Desktop" width="400" height="200">  
• Iniciar a aplicação Docker Desktop  
• Iniciar um terminal (PowerShell) na pasta onde o ficheiro docker-compose.yaml estiver presente (neste caso, docker_sockets)  
<img src="https://i.imgur.com/VsQviWe.png" alt="Exemplo de como abrir o terminal pretendido" width="300" height="200">  
• Neste terminal, correr o comando:
`````docker
docker compose up --build
`````
(usos futuros do comando não necessitaram do parametro "--build")  
  
• Aceder à página pelo IP fornecido no terminal __OU__ pela aplicação Docker Desktop (específicamente pelo contentor associado ao __backend__)  
  
<img src="https://i.imgur.com/8x7EjjI.png" alt="IP de exemplo" width="400" height="200">  
<img src="https://i.imgur.com/rfSOwIF.png" alt="Exemplo de Docker Desktop" width="1000" height="100">  
  
• Para terminar o seu uso, utilizar o comando:
`````docker
docker compose down
`````
  

## VCS e Histórico de Commits
O controlo de versões foi utilizado de forma frequente durante a realização do trabalho.  
Histórico:  
• configuração esqueleto de tabela de sensores  
• correção de erros para dashboard  
• mqtt backend  
• tentativa de leitura de sensores mqtt  
• fix docker routes and js paths  
• dashboard para sensores mqtt  

## Dificuldades
Tendo em conta o tópico de trabalho para esta fase, as maiores dificuldades encontradas no período de trabalho foram no acesso e leitura dos dados disponíveis pela série de sensores MQTT, principalmente em alturas onde estes não estavam ainda disponíveis, tendo que dificulta a verificação da funcionalidade do código que os lê.  


## Possíveis Melhorias
A leitura, de forma dinâmica, de uma série de tópicos MQTT, para gerar uma série de tabelas de dados em vez de uma única tabela, para o qual se verificaria todos os campos num formato semelhante ao que foi implementado nesta entrega.  
