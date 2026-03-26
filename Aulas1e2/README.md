# Aulas Práticas 1 e 2 - Sockets

Curso : Computação Distribuída
Estudantes Autores : Duarte Vale Nº13507, Guilherme Bento Nº13744
Date : 26/03/2026
Repository URL : Link(https://github.com/13507enautica/CD_2026)
---

## Introdução
Este relatório descreve as duas primeiras aulas práticas da unidade Curricular de Computação Distribuída, para as quais se pretende implementar um sistema de comunicação distribuída utilizando Sockets sob uma arquitetura de Cliente/Servidor, onde o servidor espera para ser contactado pelos processos clientes e tem como objetivo responder aos pedidos efetuados pelos mesmos. Os 'Sockets' detalhados no enunciado podem ser descritos como um mecanismo de comunicação bidirecional que permite a comunicação entre processos.

## Metodologia
Aula Prática 1 - Além de estudar os exemplos fornecidos, é indicado para:
1. Modificar o exemplo de Python de modo a que este funcione através de um servidor concorrente;
2. Executar os exemplos de modo que o cliente e o servidor sejam implementados em diferentes linguagens (ex.: Python/Java, Java/Python)

Aula Prática 2 - Além de estudar os exemplos fornecidos, é indicado para:
1. Propor uma versão para o programa da calculadora (Servidor e Cliente) de modo que:
a) Os dois programas comunicam utilizando mensagens JSON
b) Adicione as seguintes operações com números complexos:
  • Soma
  • Subtração
  • Multiplicação 

## Estrutura de Ficheiros
CD_Java    -> Implementação da 2ª aula prática
CD_Python  -> Implementação da 1ª aula prática

## Instruções
• A pasta CD_Java/Java está configurada no IDE de IntelliJ IDEA e entre dois ficheiros .bat dedicados às pastas de Cliente (go-Java/Python) /Servidor (go)
• A pasta CD_Python/Python está configurada entre dois ficheiros .bat dedicados às pastas de Cliente (go-Java/Python) /Servidor (go)

## VCS e Histórico de Commits
O VCS (Version Control System) do projeto foi configurado no final do seu desenvolvimento, o que se reflete na pouca quantidade de commits.
# Histórico:
• Initial commit
• Configuração de ficheiros existentes no repositório git
• readme para relatório 1
•

## Dificuldades
A implementação de heterogeneidade entre servidores/clientes nas linguagens de Python/Java apresentou um grande nível de dificuldades, bem como a escrita/leitura de várias operações num único cliente.

## Possíveis Melhorias
Melhoria de heterogeneidade entre modelos de arquitetura cliente/servidor, otimização da leitura de dados para requerer a criação de menos variáveis e instâncias de código, integração de várias operações por cada cliente.

