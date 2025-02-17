<div style="margin: 0; padding: 0; text-align: center; border: none;">
<a href="https://quantlet.com" target="_blank" style="text-decoration: none; border: none;">
<img src="https://github.com/StefanGam/test-repo/blob/main/quantlet_design.png?raw=true" alt="Header Image" width="100%" style="margin: 0; padding: 0; display: block; border: none;" />
</a>
</div>

```
Name of Quantlet: SC_open_source_scraping

Published in: Understanding Smart Contracts: Hype or Hope?

Description: This Quantlet is dedicated to gathering data on the open source source codes of Solidity Smart Contracts using the API of https://etherscan.io/.

Quantlet Scripts Description: 
- SC_open_source_scraping.ipynb the code to obtain the source codes of open source verified Solidity Smart Contracts using API of Etherscan
- SC_open_source_codes_parsing.ipynb parsing the open source source codes using regex

Keywords: API, parsing, scraping, regex, Ethereum, Solidity, smart contracts, Etherscan

Author: Elizaveta Zinovyeva, Raphael Constantin Georg Reule

Submitted: Jan 09 2021 by Elizaveta Zinovyeva

Datafile: 
- token.txt the file containing the API token of Etherscan
- current export-verified-contractaddress-opensource-license* csv file, you can obtain the last 10.000 verified open source smart contracts as csv on Etherscan https://etherscan.io/contractsVerified?filter=opensourcelicense
- other datasets are created within this Quantlet, so please just use the codes in the order listed in Quantlet Scripts Description

Additional Notes: 
- you would need to create additional folders data, data/sol_source_open_source and data/sol_source_not_verified_open_source
- be aware of the redundancies in the code. The code presented here is not made for production (neither it is optimized for production). It's purpose is solely to see and to be able to compare all the numbers presented in the paper

```
