[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **SC_topics_unlabelled** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Name of Quantlet: 'SC_topics_unlabelled'

Published in: 'Hype or Hope? Understanding Smart Contracts.'

Description: 'This Quantlet is dedicated to clustering of the unlabelled open source Ethereum Smart Contracts.
First, we encode our abstracts with Distilbert embeddings and using UMAP we reduce dimensionality reduction to perform K-Means, finally again using UMAP
reduce dimensionality to 2, to be able to plot it.'

Quantlet Scripts Description:
- SC_topics_unlabelled.ipynb clustering of the unlabelled open source Smart Contracts, using Distilbert embeddings, UMAP dimensionality reduction and K-Means clustering


Keywords: 'DistilBERT, topic modelling, clustering, UMAP, K-Means, comments, source code, Solidity'

Author: 'Elizaveta Zinovyeva, Raphael Constantin Georg Reule'

Submitted:  'Jan 20 2021 by Elizaveta Zinovyeva'

Datafile:
- open_source_parsed_16thousand.csv the file created in the Quantlet SC_open_source_scraping


Additional Notes:
- you would need to create additional folder images
- be aware of the redundancies in the code. The code presented here is not made for production (neither it is optimized for production). It's purpose is solely to see and to be able to compare all the numbers presented in the paper

```

![Picture1](davies_unlabelled_t.png)

![Picture2](scatter_research_t.png)

![Picture3](scatter_unlabelled_t.png)

![Picture4](silhouette_unlabelled_t.png)