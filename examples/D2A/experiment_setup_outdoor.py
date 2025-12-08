import sentence_transformers
import sys
from concordia.language_model import utils
import json
import os
import time
import requests
from concordia.language_model import utils
import openai

# the root path of the project, this is used to import the D2A module
ROOT = r""

# how many episodes in each simulation, each episode is 20 minutes
episode_length = 6

# whether to use the language model, if set to True, No language model will be used
# use for debugging
disable_language_model = False

# the sentence transformer model used to encode the text
st_model = sentence_transformers.SentenceTransformer(
    'sentence-transformers/all-mpnet-base-v2')
embedder = lambda x: st_model.encode(x, show_progress_bar=False)

# the agents that will be tested, there are four agents: ['ReAct', 'BabyAGI', 'LLMob', 'D2A']
tested_agents = ['D2A']

# whether to use the previous profile, if set to True, the previous profile will be used
# used to run with the same profile as the previous run
Use_Previous_profile = False
previous_profile_file = None
previous_profile = None

# if Use_Previous_profile is True, the previous profile file should be provided
if Use_Previous_profile:
  previous_profile_file = os.path.join(r'examples\D2A\result_folder\outdoor_result\Your folder name', 'Your previous profile name.json')
  try:
    with open(previous_profile_file, 'r') as f:
      previous_profile = json.load(f)
  except:
    raise ValueError('The previous profile file is not found.')
else:
  previous_profile = None


# 设定最大重试次数和重试间隔
MAX_RETRIES = 8
RETRY_DELAY = 5  # 每次重试的延迟时间（秒）

# 定义一个新的函数来处理带重试机制的API请求
def get_language_model_with_retry(api_type, model_name, api_key, disable_language_model, retries=MAX_RETRIES):
    attempt = 0
    while attempt < retries:
        try:
            # 调用原有的函数获取语言模型
            model = utils.language_model_setup(
                api_type=api_type,
                model_name=model_name,
                api_key=api_key,
                disable_language_model=disable_language_model,
            )
            return model
        except requests.exceptions.RequestException as e:
            # 如果遇到请求错误（连接问题等），则打印错误并重试
            print(f"Request failed on attempt {attempt + 1}/{retries}. Error: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Could not connect to the API.")
                raise  # 如果达到最大重试次数，则抛出异常

# the language model used to generate the text
# you can also use other models, detailed see the definition of language_model_setup
api_type = 'openai'
model_name = 'deepseek-v3'
api_key=''
openai.log = 'debug'
device = 'cpu'
model = utils.language_model_setup(
    api_type=api_type,
    model_name=model_name,
    api_key=api_key,
    disable_language_model=disable_language_model,
)

# the desires that will be used in the simulation
###
wanted_desires = [

  ]
###
# the hidden desires that will be used in the simulation
hidden_desires = []
###

# the path to store the result
current_file_path = os.path.dirname(os.path.abspath(__file__))
result_folder_name = 'result_folder'
current_folder_path = os.path.join(current_file_path, result_folder_name)
if not os.path.exists(current_folder_path):
  os.makedirs(current_folder_path)

# the result will be store in the subsub_folder
subsub_folder = os.path.join(current_folder_path, 'outdoor_result')
if not os.path.exists(subsub_folder):
  os.makedirs(subsub_folder)
