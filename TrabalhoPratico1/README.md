# Trabalho Prático Fase 1 (Grupo )

Curso : Computação Distribuída
Grupo: 
Estudantes Autores : Duarte Vale Nº13507, Guilherme Bento Nº13744
Date : 23/04/2026
Repository URL : Link(https://github.com/13507enautica/CD_2026)
---


## Introdução
Este relatório descreve a primeira fase do projeto final da unidade curricular de Computação Distribuída, para o qual se pretende reimplementar uma nova adaptação do projeto de Programação Web de modo a que este funcione dentro de um ambiente de contentores. 


## Metodologia
O trabalho original para a unidade curricular de Programação Web (2024/2025) há sido realizado pelo Grupo 12 do suposto ano letivo (João Pires, Duarte Vale, Francisca Ricardo, Pedro Vingadas) com o propósito de gestão de uma rede de embarcações e estadías náuticas num porto escolar fictício.  
  
A questão inicial do trabalho de Computação Distríbuida visa o ambito de obter e alterar o trabalho prático do semestre passado (ano passado neste caso) de modo a separar a funcionalidade original do servidor Python entre os seus components de gestão de dados e serviços de backend.  
Estes dois servidores comunicam entre sí, exclusivamente por modo de mensagens no formato JSON, para que a informação da base de dados necessária para a devida página não seja acedida diretamente por um único servidor.  
Por fim, há o requesito da implementação de um dockerfile com uma solução 'compose' de modo a que os servidores desenvolvidos possam ser instanciados em contentores pela aplicação, onde apenas o contentor web consegue ser acedido pelo dado host.


## Estrutura de Ficheiros
• Ficheiro README.md (Relatório de trabalho)
• 

## Instruções
O projeto implica não só o uso básico do código desenvolvido, mas o mesmo também deverá ser utilizado dentro de um ambiente de contentores (Docker ou Podman) para o qual existe a presença do ficheiro 'compose'.  
  
• Descarregar o código de projeto presente no repositório  
• Descarregar a aplicação [Docker Desktop](https://www.docker.com/products/docker-desktop/)  
![Página de download para a aplicação Docker Desktop](https://i.imgur.com/LNmSqrW.png)  
• Iniciar a aplicação Docker Desktop  
• Configurar os contentores  
•   

## VCS e Histórico de Commits
O VCS (Version Control System) do projeto foi configurado no final do seu desenvolvimento, tendo em conta a realização de trabalho for a do contexto de git.  
  
Histórico:  
• Commit inicial de criação do ficheiro README.md  
• Transferência de todos os ficheiros do propósito prático (Trabalho proposto)  
• Finalização do ficheiro README.md de relatório  

## Dificuldades
As principais dificuldades sentidas durante o período de trabalho tiveram origem em testar o trabalho por meio do ambiente de contentores da Docker Desktop, visto que este terá sido o principal componente de trabalho introduzido à lógica existente.  
Mesmo assim, também houve um nível de dificuldade baseado na quantidade de tempo entre a criação inicial do trabalho de Programação Web e o trabalho atual de Computação Distríbuida.  


## Possíveis Melhorias
Ainda existem diversos problemas em relação à leitura de informação por parte da página web, tendo em conta os components de comunicação entre os dois servidores.
