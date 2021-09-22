# LEAD CHAT

Este é um repositório criado para estudo da construção de um chatbot. O projeto tem como objetivo **filtrar** a captação de leads de um negócio de design.

## COMO EXECUTAR O PROJETO

1. tenha instalado na máquina o **python**, **pip** e o **virtualenv**
2. execute `virtualenv venv` para inicial um ambiente virtual python
3. execute `source venv/bin/activate` para ativar o ambiente  
4. execute `venv/bin/pip3 install -r requirements.txt` para atualizar as dependências
5. configure o .env de acordo
6. execute `flask run` para iniciar o servidor na porta default 5000, se ela estiver sendo usada por um processo importante você pode executar `flask run -p :port` para especificar a porta

(OCASIONAL) execute `venv/bin/pip3 freeze > requirements.txt` se adicionar uma nova dependência ao projeto