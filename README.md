This repository contains the code developed over the third semester of the MSc in Business Analytics of AUEB for the Machine Learning and Content Analytics course.

For our project, we decided to create a Real Estate Ad Quality Assistant. The implementation focuses on two key aspects of a real estate listing: the description and the images.

In order to create our training dataset we implemented a web scrapper and collected the necessary data from a real estate aggregator, spitogatos.gr.

For data privacy reasons, the dataset is not included in this repository.

Our Data Collection folder contains the scrapper script we implemented.

The Data Processing folder contains the code for all the data exploratory analysis, the data transformations and augmentations which led to the final training dataset.

The LLM folder contains the implementation of our model fine-tuning which handles tasks such as feature extraction from the listings descriptions and description enhancement based on information gathered from the uploaded images.
The model weights have been uploaded to huggingface on the following [link](https://huggingface.co/jtsoug/llama3.1_8b_real_estate_feature_ft)

The Price Prediction folder contains the model weights, tokenizer, as well as the code implemented for the development of a multimodal price classification nn.
