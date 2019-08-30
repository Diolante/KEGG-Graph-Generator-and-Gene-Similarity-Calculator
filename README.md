# KEGG-Graph-Generator-and-Gene-Similarity-Calculator

Este programa faz parte do trabalho desenvolvido para iniciação cientifica (PIBIC) de 2018-2019, apoiado pelo CNPq.

## Bibliotecas e Softwares Utilizados

- [IGraph for Python](https://igraph.org/python/), Biblioteca para geração de grafos.
- [RE](https://docs.python.org/3/library/re.html), Biblioteca para uso de expressões regulares.
- [Cytoscape](https://cytoscape.org/), Software para vizualização de grafos.


## Sobre

Este programa pode ser dividido em duas partes:

- Geração do Grafo Aciclico Direcionado do Organismo.
- Cálculo de Similaridade Semântica entre dois Genes.

Além de armazenar os termos KO associados a cada gene (se houver), entranto ainda não são levados em conta no cálculo da similaridade semântica. 

## Organismos

No desenvolvimento fora considerados quatro organismos modelos:

- *Escherichia Coli*, Bactéria
- *Arabdopsis Thaliana*, Planta
- *Saccharomyces Cerevisiae*, Fungi
- *Drosophila Melanogaster*, Inseto

 Gerando-se assim quatro scripts, praticamente iguais mudando apenas a expressão regular associada a captura dos genes, ou seja, uma mudança de paramêtro apenas.

## Base de Dados

Foi obtida da [KEGG: Kyoto Encyclopedia of Genes and Genomes](https://www.genome.jp/kegg/), quatro arquivos para cada um dos organismos.

- eco00001.keg
- ath00001.keg
- sce00001.keg
- dme00001.keg

Onde os dados do organismo estão descritos hierarquicamente em nívels 'A', 'B', 'C' e 'D' sendo o mais especifico e contendo o gene e os possíveis termos KO associados.

## Resultados e Saídas

Na atual forma, este programa retorna um degrade de valores de similaridade (0, 0.25, 0.50, 0.75 e 1.00), onde estão relacionados diretamente com a topologia do grafo percorrido. sendo 1.00 totalmente similar.

Uma saída de grafo pode ser gerada, retornando um arquivo [**Nome-Organismo**].graphml, que pode ser utilizado no Cytoscape para visualização, conforme um pequeno exemplo abaixo.

![Trecho do Grafo da Escherichia Coli gerado](https://i.ibb.co/zSXCW0z/l0-IsbRQ.png)



