### Informações ###
* Projeto foi criando unsando python 3.6

### Executando aplicação ###
* Para executar a aplicação: `python processar.py`
* Finalmente execute o `python manage.py runserver`

### Rodando os testes ###
* Para executar os testes ` python -m unittest tests.py`

### Obs ###
* O metodo `prepara_resultado()` possui um parâmetro `completo` que o default está como `False`.
Esse parâmetro existe para fazer a análise de todo o log da corrida, não só até a definição do primeiro colocado.
Querendo analisar todo o log, só mudar esse parâmetro para `completo=True`
* O metodo `calcula_melhor_volta()` possui um parâmetro `corrida` que o default está como `False`.
Esse parâmetro existe para ver a melhor volta por piloto ou da corrida inteira.
Querendo ver a melhor volta da corrida inteira, só mudar o parâmetro para `corrida=True`