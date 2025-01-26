<div style="margin: 0; padding: 0; text-align: center; border: none;">
<a href="https://quantlet.com" target="_blank" style="text-decoration: none; border: none;">
<img src="https://github.com/StefanGam/test-repo/blob/main/quantlet_design.png?raw=true" alt="Header Image" width="100%" style="margin: 0; padding: 0; display: block; border: none;" />
</a>
</div>

```
Name of Quantlet: SC_over_time

Published in: Understanding Smart Contracts: Hype or Hope?

Description: This Quantlet is dedicated to visualization of time-series of the amount of Smart contracts created since the invention of Ethereum

Quantlet Scripts Description: 
- SC_over_time.ipynb visualizing the time-series

Keywords: Kaggle, BigQuery, visualization, time-series, source code, Solidity, smart contracts

Author: Elizaveta Zinovyeva, Raphael Constantin Georg Reule

Submitted: Jan 20 2021 by Elizaveta Zinovyeva

Datafile: 
- contracts_over_time_2020-12-09.csv the file created using BigQuery on Kaggle https://www.kaggle.com/bigquery/ethereum-blockchain https://www.kaggle.com/lizzzi1/contracts-over-time (the notebooks can also be found here, but the application requires the Ethereum BigQuery dataset on Kaggle)
- transactions_over_time_2020-12-09.csv the file created using BigQuery on Kaggle https://www.kaggle.com/lizzzi1/transactions-over-time
- source_codes_from_dapps.csv the file created within SC_Dapp_scraping quanlet

Additional Notes: 
- you will need to create the additional data folder and store the first two datafiles there
- be aware of the redundancies in the code. The code presented here is not made for production (neither it is optimized for production). It's purpose is solely to see and to be able to compare all the numbers presented in the paper

```
<div align="center">
<img src="https://raw.githubusercontent.com/QuantLet/USC/master/SC-over-time/contracts_over_time.png" alt="Image" />
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/QuantLet/USC/master/SC-over-time/contracts_over_time_with_dapps.png" alt="Image" />
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/QuantLet/USC/master/SC-over-time/contracts_over_time_with_t.png" alt="Image" />
</div>

