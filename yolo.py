#!/usr/bin/env python3

# MIT License
# Copyright (c) 2023-2024 wunderwuzzi23
# Greetings from Seattle! 

import os
import platform
from openai import OpenAI
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

def print_usage(config):
  print("Yolo v0.3 - by @wunderwuzzi23")
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


def create_client(config):
  
  # Three options for the user to specify they openai api key.
  #1. Place a ".env" file in same directory as this with the line:
  #   OPENAI_API_KEY="<yourkey>"
  #   or do `export OPENAI_API_KEY=<yourkey>` before use
  dotenv.load_dotenv()
  api_key = os.getenv("OPENAI_API_KEY")
  

  #2. Place a ".openai.apikey" in the home directory that holds the line:
  #   <yourkey>
  #   Note: This options will likely be removed in the future
  if not api_key:  #If statement to avoid "invalid filepath" error
    home_path = os.path.expanduser("~")   
    api_key=open(os.path.join(home_path,".openai.apikey"), "r").readline().strip()
   
  #3. Final option is the key might be in the yolo.yaml config file
  #   openai_apikey: <yourkey>
  if not api_key:  
    api_key=config["openai_api_key"]

  return OpenAI(api_key=api_key)

def call_open_ai(client, query, config, shell):
  # do we have a prompt from the user?
  if query == "":
      print ("No user prompt specified.")
      sys.exit(-1)
 
  # Load the correct prompt based on Shell and OS and append the user's prompt
  prompt = get_full_prompt(query, shell)

  # Make the first line also the system prompt
  system_prompt = prompt.split('\n')[0]
  #print(prompt)

  # Call the ChatGPT API
  response = client.chat.completions.create(model=config["model"],
  messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": prompt}
  ],
  temperature=config["temperature"],
  max_tokens=config["max_tokens"])
 
  return response.choices[0].message.content.strip()

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
  return 'DISPLAY' not in os.environ or not os.environ['DISPLAY']

def prompt_user_for_action(config, ask_flag, response):
  print("Command: " + colored(response, 'blue'))
  #print(config["safety"])

  modify_snippet = ""
  if bool(config["modify"]) == True:
    modify_snippet = " [m]odify"
    
  copy_to_clipboard_snippet = " [c]opy to clipboard"
  if os.name == "posix" and missing_posix_display():
    if get_os_friendly_name() != "Darwin/macOS":
      copy_to_clipboard_snippet = ""

  if bool(config["safety"]) == True or ask_flag == True:
    prompt_text = f"Execute command? [Y]es [n]o{modify_snippet}{copy_to_clipboard_snippet} ==> "
    print(prompt_text, end = '')
    user_input = input()
    return user_input 
  
  if bool(config["safety"]) == False:
     return "Y"

def eval_user_intent_and_execute(client, config, user_input, command, shell, ask_flag):
  if user_input.upper() not in ["", "Y", "C", "M"]:
    print("No action taken.")
    return
  
  if user_input.upper() == "Y" or user_input == "":
    if shell == "powershell.exe":
      subprocess.run([shell, "/c", command], shell=False)  
    else: 
      # Unix: /bin/bash /bin/zsh: uses -c both Ubuntu and macOS should work, others might not
      subprocess.run([shell, "-c", command], shell=False)
  
  if bool(config["modify"]) and user_input.upper() == "M":
    print("Modify prompt: ", end = '')
    modded_query = input()
    modded_response = call_open_ai(client, modded_query, config, shell)
    check_for_issue(modded_response)
    check_for_markdown(modded_response)
    user_intent = prompt_user_for_action(config, ask_flag, modded_response)
    print()
    eval_user_intent_and_execute(client, config, user_intent, modded_response, shell, ask_flag)
  
  if user_input.upper() == "C":
      if os.name == "posix" and missing_posix_display():
        if get_os_friendly_name() != "Darwin/macOS":
          return
      pyperclip.copy(command) 
      print("Copied command to clipboard.")

  

def main():
  #Enable color output on Windows using colorama
  init() 
  
  config = read_config()
  client = create_client(config)

  # Unix based SHELL (/bin/bash, /bin/zsh), otherwise assuming it's Windows
  shell = os.environ.get("SHELL", "powershell.exe") 

  command_start_idx  = 1     # Question starts at which argv index?
  ask_flag = False           # safety switch -a command line argument
  yolo = ""                  # user's answer to safety switch (-a) question y/n

  # Parse arguments and make sure we have at least a single word
  if len(sys.argv) < 2:
    print_usage(config)
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

  ## core prompting loop logic
  result = call_open_ai(client, user_prompt, config, shell) 
  check_for_issue(result)
  check_for_markdown(result)

  users_intent = prompt_user_for_action(config, ask_flag, result)
  print()
  eval_user_intent_and_execute(client, config, users_intent, result, shell, ask_flag)


if __name__ == "__main__":
  main()
