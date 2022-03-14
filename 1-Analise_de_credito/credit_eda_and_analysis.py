# -*- coding: utf-8 -*-
"""credit-eda-and-analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G0004G44nM5e97nvSQz0JjXJwJHRSalx
"""

import os

username = 'julio-cesar'
os.environ["GITHUB_USER"] = username

!git config --global user.name "${GITHUB_USER}"

import os
from getpass import getpass

usermail = getpass()
os.environ["GITHUB_MAIL"] = usermail

!git config --global user.email "${GITHUB_MAIL}"

import os
from getpass import getpass

usertoken = getpass()
os.environ["GITHUB_TOKEN"] = usertoken

!git clone https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/juliopk543/AWS_Cloud_Analysis.git

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/AWS_Cloud_Analysis

!git status

"""# **Exploração e análise de dados de crédito com SQL**

## Os dados: 

Os dados representam informações de clientes de um banco e contam com as seguintes colunas: 

* idade = idade do cliente
* sexo = sexo do cliente (F ou M)
* dependentes = número de dependentes do cliente
* escolaridade = nível de escolaridade do clientes
* salario_anual = faixa salarial do cliente
* tipo_cartao = tipo de cartao do cliente
* qtd_produtos = quantidade de produtos comprados nos últimos 12 meses
* iteracoes_12m = quantidade de iterações/transacoes nos ultimos 12 meses
* meses_inativo_12m = quantidade de meses que o cliente ficou inativo
* limite_credito = limite de credito do cliente
* valor_transacoes_12m = valor das transações dos ultimos 12 meses
* qtd_transacoes_12m  = quantidade de transacoes dos ultimos 12 meses

A tabela foi criada no **AWS Athena** junto com o **S3 Bucket** com uma versão dos dados disponibilizados em: https://github.com/andre-marcos-perez/ebac-course-utils/tree/main/dataset Professor do Curso **Profissão DataAnalyst ebac**


## **Exploração de dados:**

A primeira fase da análise é entender o que tem na nossa matéria prima. Vamos a exploração de dados:

**Qual a quantidade de informações temos na nossa base de dados?**

Query: SELECT count(*) FROM credito
> Reposta: 2564 linhas

**ps.:** A base de dados do link acima contém mais linhas do que a seleção utilizada. Você pode utilizar todas as linhas ou considerar apenas uma fração dos dados. Na prática, quanto maior a quantidade de dados utilizada, mais confiável a análise! Mas existem limites computacionais e financeiros na qual a redução de dados para análise para fins de estudo se torna interessante. 

**Como são os dados** 

Query: SELECT * FROM credito LIMIT 10;
![Dez primeiras linhas do dataset](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/credito_limit_10.png?raw=true)

> É possível reparar que existem algumas informações nulas na tabela (valor na), vamos olhar mais de perto para os valores de cada coluna! 

**Quais os tipos de cada dado**

**Query:** DESCRIBE credito

![Descrição dos tipos de dados](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/describe_credito.png?raw=true)


Agora que ja entendemos quais são os tipos de dados, vamos olhar mais atentamente para as varíaveis que não são numéricas.

**Quais são os tipos de escolaridade disponíveis no dataset?**

**Query:** SELECT DISTINCT escolaridade FROM credito

![Tipos de escolaridade](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_escolaridade.png?raw=true)

> Os dados contam com vários níveis de escolaridade e é possível perceber que temos valores nulos (na) no dataset, trataremos isso mais tarde!

Será que temos mais valores nulos?

**Quais são os tipos de estado_civil disponíveis no dataset?**

**Query:** SELECT DISTINCT estado_civil  FROM credito

![Tipos de estado civil](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_estado_civil.png?raw=true)

> Novamente encontramos valores nulos nos dados de estado civil!

**Quais são os tipos de salario_anual disponíveis no dataset?**

**Query:** SELECT DISTINCT salario_anual  FROM credito

![Tipos de salario anual](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_salario_anual.png?raw=true)

> Os salários nesse dataset não estão expostas com o valor exato que o cliente ganha. O que está informado é a faixa salarial de cada um. Também contem dados nulos. 


**Quais são os tipos de cartão disponíveis no dataset?**

**Query:** SELECT DISTINCT tipo_cartao  FROM credito

![Tipos de cartão](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_tipos_de_cartao.png?raw=true)

> Aqui vemos que não há necessidade de tratar valores nulos.

## **Análise de dados**

Uma vez que exploramos o dados e buscamos entender quais são as informações que temos no nosso banco de dados, podemos analisar as informações para buscar entender o que está acontecendo no banco de dados. Vamos fazer perguntas:
/
**Nesse banco de dados, quantos clientes temos de cada faixa salarial?**

**Query:** select count(*), salario_anual from credito group by salario_anual

![Quantidade para cada faixa salarial](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_faixa_salarial.png?raw=true)

> a maioria dos clientes dessa base de dados possui um renda menor que 40K e existem 235 clientes que não informaram ou não consta a faixa salarial. 
> De certa forma, pode ser interessante para a empresa focar nesse público de mais baixa renda. 

**Nesse banco de dados, quantos clientes são homens e quantos são mulheres?**

**Query:** select count(*), sexo from credito group by sexo


![Quantidade para cada sexo](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_faixa_sexo.png?raw=true)

![Quantidade para cada sexo - gráfico](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/grafico_faixa_sexo.png?raw=true)

> A maioria dos clientes desse banco é homem! Do csv extraído dos dados é possível gerar o gráfico em pizza com para melhor a proporção de masculino/feminino

**Queremos focar o nosso marketing de maneira adequada para nossos clientes, qual será a idade deles?**

**Query:** select avg(idade) as media_idade, min(idade) as min_idade, max(idade) as max_idade, sexo from credito group by sexo
![Média de idades por sexo](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_idade_sexo.png?raw=true)

> Por meio dessa análise não foi possível extrair nenhuma informação relevante.  A menor idade dos dois sexos é a mesma e a média é muito similar. A unica  diferença é a idade máxima mas fato quase irrelevante por a diferença não é tão gritante.


**Qual a maior e menor transação dos clientes?**

**Query:** select min(valor_transacoes_12m) as transacao_minima, max(valor_transacoes_12m) as transacao_maxima from credito
![Valor transacoes](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_transacoes.png?raw=true)

> Nesse banco de dados temos soma de transações em 12 meses variam de 510.16 a 4776.58

**Quais as características dos clientes que possuem os maiores creditos?**

**Query:** 
select max(limite_credito) as limite_credito, escolaridade, tipo_cartao, sexo 
from credito
where escolaridade != 'na' and tipo_cartao != 'na' 
group by  escolaridade, tipo_cartao, sexo 
order by limite_credito desc
limit 10

![Valor limite](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_limite_desc.png?raw=true)

> Não parece haver um impacto da escolaridade no limite. O limite mais alto é oferecido para um homem sem educação formal. O cartão também parece não estar relacionado com a escolaridade nem com o limite. Dentre os maiores limites, encontramos clientes com cartão: gold, silver, platinum e blue

**Quais as características dos clientes que possuem os menores creditos?**

**Query:** 
select min(limite_credito) as limite_credito, escolaridade, tipo_cartao, sexo 
from credito
where escolaridade != 'na' and tipo_cartao != 'na' 
group by  escolaridade, tipo_cartao, sexo 
order by limite_credito asc
limit 10


![Valor limite](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_limit_asc.png?raw=true)

> Dessa vez conseguimos perceber não há clientes com cartão platinum apenas blue dentre os 10 menores limites. Também foi possível perceber uma igualdade de 5 Homens x 5 Mulheres dentre os menores limites. 

**Será que as mulheres gastam mais?**

**Query:** 
select max(valor_transacoes_12m) as maior_valor_gasto, avg(valor_transacoes_12m) as  media_valor_gasto, min(valor_transacoes_12m) as min_valor_gasto, sexo 
from credito
group by sexo 


![Valor transacoes/sexo](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_gasto_por_sexo.png?raw=true)

> Os gastos de homens e mulheres são similares.

Por fim, 


**O salário impacta no limite?**

**Query:** select avg(qtd_produtos) as qts_produtos, avg(valor_transacoes_12m) as media_valor_transacoes, avg(limite_credito) as media_limite,  sexo,   salario_anual from credito 
where salario_anual != 'na'
group by sexo, salario_anual
order by avg(valor_transacoes_12m) desc

![Valor salario_anualLimite](https://github.com/juliopk543/AWS_Cloud_Analysis/blob/main/1-Analise_de_credito/query_results_imgs/query_salarioAnualMediaLimite.png?raw=true)

>SIM! As pessoas que tem menor faixa salarial também apresentam menor limite de credito!

# Conclusão

Essas foram **algumas** análises extraídas do dataset de crédito.  

Alguns insights interessantes:

- a maior parte dos clientes possui renda até 40K 
- a maior parte dos clientes é masculino!
- a escolaridade não parece influenciar no limite nem no tipo do cartão
- os clientes com maiores limites são em sua maioria homens 
- os clientes com menores limites esta dividido entre Homens e Mulheres
- dentre os primeiros, menores limites não há presença de cartão platinum apenas blue
- a faixa salarial impacta diretamente no limite de crédito
- nao existem clientes com salário anual acima de 60K do sexo feminino

**Uma exploração maior dos dados pode explicar porque as mulheres tem menor crédito. Isso também pode ser um problema cultural que pode ser repensado!**
"""