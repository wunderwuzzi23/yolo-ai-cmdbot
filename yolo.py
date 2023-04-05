#!/usr/bin/env python3

# MIT License
# Copyright (c) 2023 wunderwuzzi23
# Greetings from Seattle! 

import os
import platform
import openai
import sys
import subprocess
import dotenv 
import distro
import yaml
import pyperclip

from termcolor import colored
from colorama import init

def read_config() -> any:

  ## Find the executing directory (e.g. in case an alias is set)
  ## So we can find the config file
  yolo_path = os.path.abspath(__file__)
  prompt_path = os.path.dirname(yolo_path)

  config_file = os.path.join(prompt_path, "yolo.yaml")
  with open(config_file, 'r') as file:
    return yaml.safe_load(file)

# Construct the prompt
def get_full_prompt(user_prompt, shell):

  ## Find the executing directory (e.g. in case an alias is set)
  ## So we can find the prompt.txt file
  yolo_path = os.path.abspath(__file__)
  prompt_path = os.path.dirname(yolo_path)

  ## Load the prompt and prep it
  prompt_file = os.path.join(prompt_path, "prompt.txt")
  pre_prompt = open(prompt_file,"r").read()
  pre_prompt = pre_prompt.replace("{shell}", shell)
  pre_prompt = pre_prompt.replace("{os}", get_os_friendly_name())
  prompt = pre_prompt + user_prompt
  
  # be nice and make it a question
  if prompt[-1:] != "?" and prompt[-1:] != ".":
    prompt+="?"

  return prompt

def print_usage():
  print("Yolo v0.2.1 - by @wunderwuzzi23")
  print()
  print("Usage: yolo [-a] list the current directory information")
  print("Argument: -a: Prompt the user before running the command (only useful when safety is off)")
  print()

  print("Current configuration per yolo.yaml:")
  print("* Model        : " + str(config["model"]))
  print("* Temperature  : " + str(config["temperature"]))
  print("* Max. Tokens  : " + str(config["max_tokens"]))
  print("* Safety       : " + str(bool(config["safety"])))


def get_os_friendly_name():
  
  # Get OS Name
  os_name = platform.system()
  
  if os_name == "Linux":
    return "Linux/"+distro.name(pretty=True)
  elif os_name == "Windows":
    return os_name
  elif os_name == "Darwin":
    return "Darwin/macOS"
  else:
    return os_name


def set_api_key():
  # Two options for the user to specify they openai api key.
  #1. Place a ".env" file in same directory as this with the line:
  #   OPENAI_API_KEY="<yourkey>"
  #   or do `export OPENAI_API_KEY=<yourkey>` before use
  dotenv.load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")
  
  #2. Place a ".openai.apikey" in the home directory that holds the line:
  #   <yourkey>
  #   Note: This options will likely be removed in the future
  if not openai.api_key:  #If statement to avoid "invalid filepath" error
    home_path = os.path.expanduser("~")    
    openai.api_key_path = os.path.join(home_path,".openai.apikey")

  #3. Final option is the key might be in the yolo.yaml config file
  #   openai_apikey: <yourkey>
  if not openai.api_key:  
    openai.api_key = config["openai_api_key"]

if __name__ == "__main__":

  config = read_config()
  set_api_key()

  # Unix based SHELL (/bin/bash, /bin/zsh), otherwise assuming it's Windows
  shell = os.environ.get("SHELL", "powershell.exe") 

  command_start_idx  = 1     # Question starts at which argv index?
  ask_flag = False           # safety switch -a command line argument
  yolo = ""                  # user's answer to safety switch (-a) question y/n

  # Parse arguments and make sure we have at least a single word
  if len(sys.argv) < 2:
    print_usage()
    sys.exit(-1)

  # Safety switch via argument -a (local override of global setting)
  # Force Y/n questions before running the command
  if sys.argv[1] == "-a":
    ask_flag = True
    command_start_idx = 2

  # To allow easy/natural use we don't require the input to be a 
  # single string. So, the user can just type yolo what is my name?
  # without having to put the question between ''
  arguments = sys.argv[command_start_idx:]
  user_prompt = " ".join(arguments)

def call_open_ai(query):
  # do we have a prompt from the user?
  if query == "":
      print ("No user prompt specified.")
      sys.exit(-1)
 
  # Load the correct prompt based on Shell and OS and append the user's prompt
  prompt = get_full_prompt(query, shell)

  # Make the first line also the system prompt
  system_prompt = prompt[1]
  #print(prompt)

  # Call the ChatGPT API
  response = openai.ChatCompletion.create(
    model=config["model"],
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    temperature=config["temperature"],
    max_tokens=config["max_tokens"],
  )
 
  return response.choices[0].message.content.strip()


#Enable color output on Windows using colorama
init() 

def check_for_issue(response):
  prefixes = ("sorry", "i'm sorry", "the question is not clear", "i'm", "i am")
  if response.lower().startswith(prefixes):
    print(colored("There was an issue: "+response, 'red'))
    sys.exit(-1)

def check_for_markdown(response):
  # odd corner case, sometimes ChatCompletion returns markdown
  if response.count("```",2):
    print(colored("The proposed command contains markdown, so I did not execute the response directly: \n", 'red')+response)
    sys.exit(-1)

def missing_posix_display():
  display = subprocess.check_output("echo $DISPLAY", shell=True)
  return display == b'\n'

def prompt_user_input(response):
  print("Command: " + colored(response, 'blue'))
  #print(config["safety"])

  if bool(config["safety"]) == True or ask_flag == True:
    prompt_text = "Execute command? [Y]es [n]o [m]odify [c]opy to clipboard ==> "
    if os.name == "posix" and missing_posix_display():
        prompt_text =  "Execute command? [Y]es [n]o [m]odify ==> "
    print(prompt_text, end = '')
    user_input = input()
    return user_input 
  
  if config["safety"] == False:
     return "Y"

def evaluate_input(user_input, command):
  if user_input.upper() == "Y" or user_input == "":
    if shell == "powershell.exe":
      subprocess.run([shell, "/c", command], shell=False)  
    else: 
      # Unix: /bin/bash /bin/zsh: uses -c both Ubuntu and macOS should work, others might not
      subprocess.run([shell, "-c", command], shell=False)
  
  if user_input.upper() == "M":
    print("Modify prompt: ", end = '')
    modded_query = input()
    modded_response = call_open_ai(modded_query)
    check_for_issue(modded_response)
    check_for_markdown(modded_response)
    modded_user_input = prompt_user_input(modded_response)
    print()
    evaluate_input(modded_user_input, modded_response)
  
  if user_input.upper() == "C":
      if os.name == "posix" and missing_posix_display():
        return
      pyperclip.copy(command) 
      print("Copied command to clipboard.")

res_command = call_open_ai(user_prompt) 
check_for_issue(res_command)
check_for_markdown(res_command)
user_input = prompt_user_input(res_command)
print()
evaluate_input(user_input, res_command)
