[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **SC_Dapp_scraping** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Name of Quantlet: 'SC_Dapp_scraping'

Published in: 'Hype or Hope? Understanding Smart Contracts.'

Description: 'This Quantlet is dedicated to gathering data on the open source source codes of Solidity Smart Contracts.
First, the Ethereum Dapps names are obtained using the API https://www.stateofthedapps.com/. For each DApp the list of smart contract hashes were obtained if available (Also through the API of state of the Dapps).
And followingly using the API of https://etherscan.io/, the source codes (if verified) are obtained for the open source Dapps.
Finally, the codes are parsed and preprocessed to extract comments and merged with the category from the State of the Dapps and stored as a csv file.'

Quantlet Scripts Description:
- SC_Dapp_scraping.ipynb the code for obtaining the list of Ethereum DApps and hashes for each DApp
- SC_Dapp_source_codes_scraping.ipynb the code to obtain the source codes of open source verified Solidity Smart Contracts using API of Etherscan
- SC_Dapp_source_codes_parsing.ipynb parsing the open source source codes using regex
- SC_Dapp_contracts_per_Dapp.ipynb just additional code to check how many source codes have different DApps

Keywords: 'API, parsing, scraping, regex, Ethereum, Solidity, Etherscan, smart contracts, stateofthedapps'

Author: 'Elizaveta Zinovyeva, Raphael Constantin Georg Reule'

Submitted:  'Jan 08 2021 by Elizaveta Zinovyeva'

Datafile:
- address.txt the file containing the URL address of the stateofthedapps API, you can contact the website's team for the address
- token.txt the file containing the API token of Etherscan
- other datasets are created within this Quantlet, so please just use the codes in the order listed in Quantlet Scripts Description

Additional Notes:
- you would need to create additional folders data, data/sol_source_open_source and data/sol_source_not_verified_open_source
- be aware of the redundancies in the code. The code presented here is not made for production (neither it is optimized for production). It's purpose is solely to see and to be able to compare all the numbers presented in the paper

```

### [IPYNB Code: SC_Dapp_scraping.ipynb](SC_Dapp_scraping.ipynb)


automatically created on 2021-01-21