# KEGG-Graph-Generator-and-Gene-Similarity-Calculator

Este programa faz parte do trabalho desenvolvido para iniciação cientifica (PIBIC) de 2018-2019, apoiado pelo CNPq.

## Bibliotecas Utilizadas

- [IGraph for Python](https://igraph.org/python/), Ferramenta para geração de grafos.
- [RE](https://docs.python.org/3/library/re.html), Ferramenta para uso de expressões regulares.

## Sobre

Este programa pode ser dividido em duas partes:

- Geração do Grafo Aciclico Direcionado do Organismo.
- Cálculo de Similaridade Semântica entre dois Genes.

Além de armazenar os termos KO associados a cada gene (se houver), entranto ainda não são levados em conta no cálculo da similaridade semântica. 

## Organismos

No desenvolvimento fora considerados quatro organismo modelos:

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

