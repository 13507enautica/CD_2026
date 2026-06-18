# CD_2026
Escola Superior Náutica Infante D. Henrique  
Relatório de Trabalho Prático para a Unidade Curricular de Computação Distríbuida, Ano Letivo 2025/2026  
  
<ins>__Grupo__</ins>: Nº9  
  
<ins>__Estudantes Autores__</ins>:
- Duarte Vale Nº13507  
- Guilherme Bento Nº13744
  
<ins>__Professor Orientador__</ins>:  
- Prof. Carlos Gonçalves  
## Índice de Trabalhos:  
1) [Trabalho 1](https://github.com/13507enautica/CD_2026/tree/main/TrabalhoPratico1)  
2) [Trabalho 2](https://github.com/13507enautica/CD_2026/tree/main/TrabalhoPratico2)  
3) [Trabalho 3](https://github.com/13507enautica/CD_2026/tree/main/TrabalhoPratico3)  
  
## Introdução
texto introdutório  
  
## Estrutura de Ficheiros
- Pasta "Aulas1e2"
- Pasta "TrabalhoPratico1"  
- Pasta "TrabalhoPratico2"  
- Pasta "TrabalhoPratico3"  
  
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
  
## Clarificação de Uso de Inteligência Artificial
Numa tentativa de manter a lógica do trabalho fiel à criada por nós o uso de inteligência artificial no trabalho foi limitado apenas aos propósitos de debug e resumo de documentação para algumas bibliotecas.  
  
## Resultados (Projeto Final)
por fazer  
  
## Conclusões
conclusões do trabalho  