# Trabalho Prático Fase 2 (Grupo 9)  
  
Curso : Computação Distribuída  
Grupo: 9  
Estudantes Autores : Duarte Vale Nº13507, Guilherme Bento Nº13744  
Date : 23/04/2026  
Repository URL : Link(https://github.com/13507enautica/CD_2026)  
---


## Introdução
Este relatório descreve a segunda fase do projeto final da unidade curricular de Computação Distribuída, para o qual se pretende continuar a adaptação do projeto final de Programação Web para este mesmo funcionar através de um ambiente de contentores. Distinguido da abordagem da primeira fase, a comunicação entre servidores não é realizada por sockets, mas sim por uma API REST.  


## Metodologia
O trabalho original para a unidade curricular de Programação Web (2024/2025) há sido realizado pelo Grupo 12 do suposto ano letivo (João Pires, Duarte Vale, Francisca Ricardo, Pedro Vingadas) com o propósito de gestão de uma rede de embarcações e estadías náuticas num porto escolar fictício.  
  
Esta fase do trabalho visa ainda o ambito de alterar o trabalho prático do semestre passado (ano passado neste caso) de modo a separar a funcionalidade original do servidor Python entre os seus components de gestão de dados e serviços de backend.  
Estes dois servidores comunicam entre sí, exclusivamente por modo de mensagens no formato JSON, para que a informação da base de dados necessária para a devida página não seja acedida diretamente por um único servidor.  
Por fim, há o requesito da implementação de um dockerfile com uma solução 'compose' de modo a que os servidores desenvolvidos possam ser instanciados em contentores pela aplicação, onde apenas o contentor web consegue ser acedido pelo dado host.  


## Estrutura de Ficheiros
• Ficheiro README.md (Relatório de trabalho)  
• Pasta "docker_rotas"  
- | Pasta "servidor_docker_backend" (Ficheiros de backend do servidor, destinados para o seu próprio contentor)  
- | Pasta "servidor_docker_db" (Ficheiros da base de dados do servidor, destinados para o seu próprio contentor)  
- | Ficheiro "docker-compose.yaml" (Configurações de contentores por modo de um ficheiro docker-compose)  

## Instruções
O projeto implica não só o uso básico do código desenvolvido, mas o mesmo também deverá ser utilizado dentro de um ambiente de contentores (Docker ou Podman) para o qual existe a presença do ficheiro 'compose'.  
  
• Descarregar o código de projeto presente no repositório  
• Descarregar a aplicação [Docker Desktop](https://www.docker.com/products/docker-desktop/)  
![Página de download para a aplicação Docker Desktop](https://i.imgur.com/LNmSqrW.png)  
• Iniciar a aplicação Docker Desktop  
• Iniciar um terminal (PowerShell) na pasta onde o ficheiro docker-compose.yaml estiver presente (neste caso, docker_sockets)  
• Neste terminal, correr o comando "docker compose up --build" (usos futuros do comando não necessitaram do parametro "--build")  
• Aceder à página pelo IP fornecido no terminal  

## VCS e Histórico de Commits
O VCS (Version Control System) do projeto foi configurado no final do seu desenvolvimento, tendo em conta a realização de trabalho for a do contexto de git.  
  
Histórico:  
• Commit inicial  
• rotas e sockets  
• fix ports  
• Reconfiguração da estrutura de ficheiros para dividir fases  
• Configuração do ficheiro README.md de relatório  

## Dificuldades
O principal desafio para a conclusão desta fase teve origem no desenvolvimento da página de marcação de estadias para embarcações, que apresentou várias dificuldades em encontrar os componentes necessários para carregar a página em si.  


## Possíveis Melhorias
A implementação de testes para componentes individuais de modo a conseguir identificar e/ou justificar erros por parte das páginas que demonstram/obtêm informação por meio da base de dados.  
