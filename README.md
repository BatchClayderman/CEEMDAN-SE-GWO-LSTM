# CEEMDAN-SE-GWO-LSTM

This is a repo for implementing CEEMDAN-SE-GWO-LSTM. CEEMDAN-SE and GWO-LSTM are combined manually in this experiment. 

- CEEMDAN: Divide the waves into several sine or cosine waves. 
- SE: Select the waves that contain the top-$k$ highest information amount to combine to form new waves with less noise.
- GWO: Lead the LSTM as the optimizer.
- LSTM: The core training part. 

This repo will no longer be under maintenance. Continuing usage may lead to potential errors and exceptions. 

To train the related time-series models (with a GUI), please refer to [https://github.com/BatchClayderman/ForestAdvisor](https://github.com/BatchClayderman/ForestAdvisor). 
