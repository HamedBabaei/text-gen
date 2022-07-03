# Conditional Text Generation with GPT-2

The goal is to generate texts from input texts by detecting entities and generating new text in the condition that uses entities.

First, entities will be detected from texts. Next, new texts will be generated and they will be stored in the PostgreSQL database if it is not repeated again.

We followed the two approaches:

* First, using the pre-trained GPT-2 model.
* Second, finetuning on predefined topics to make the generation specific to the topic (the generation will happen under two conditions: topic and entities)

For the second approach, we used the [News Category Dataset (kaggle)](https://www.kaggle.com/datasets/rmisra/news-category-dataset) dataset and picked the predefined topics to fine-tune the model. However, the number of samples is too low. So more data will ensure a good generator model here.

We designed software to do the conditional generation. All designs followed the abstractive implementation to separate everything for future developments. This is version 0.1.0 and surely there will be more upgrades to achieve the Version 1.0.0 tag.


## How to run the application
The API can use the raw GPT-2 and fine-tuned model. To specify this automatically, the `deploy_config.py` script with the `DeployConfig` class has been created with the **inf_model** parameter with a default value of `main` (to use raw GPT-2). However, you can download the fine-tuned model and use the ` finetuned` variable to run the API based on fine-tuned model.


1. Install requirenments:
    * python3
    * Docker
    * packages in `requirenments.txt`
2. Install PostgreSQL database
```c
sudo apt-get install postgresql
```
3. Create `keys.py` Script and add database configurations as followings
```python
LOCAL_SETUP = True    # set this to false for deployment

if LOCAL_SETUP:
    DATABASE=''
    USER=''
    PASSWORD=''
    HOST='127.0.0.1'
    PORT='5432'
else:
    DATABASE=''
    USER=''
    PASSWORD=''
    HOST='db'
    PORT='5432'
```
4. (1) Running using Python Command
```c
python3 app.py
```
5. (2) Running using Dockerfile
```c
docker build -t textgen .

docker run -d -p 5000:5000 textgen
```

6. The easiest: use `docker-compose`:
```c
docker-compose up
```
7. Test whatever everything is set up and works
```url
http://0.0.0.0:5000/ping
```
If everything was ok you are going to see `testing` text!

8. Now you can use the following post request to get the new texts from text generation model.
```url
http://0.0.0.0:5000/gen-text
```
with request body of 
```json
{
    "text": "this is a text",
    "num-sequences": 3
}
```
