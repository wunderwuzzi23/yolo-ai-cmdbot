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

yolo_path = os.path.abspath(__file__)
prompt_path = os.path.dirname(yolo_path)

config_file = os.path.join(prompt_path, "yolo.yaml")
with open(config_file, 'r') as file:
  config = yaml.safe_load(file)

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:  #If statement to avoid "invalid filepath" error
  home_path = os.path.expanduser("~")    
  openai.api_key_path = os.path.join(home_path,".openai.apikey")

if not openai.api_key:  
  openai.api_key = config["openai_api_key"]

shell = os.environ.get("SHELL", "powershell.exe") 

command_start_idx  = 1     # Question starts at which argv index?
ask_flag = False           # safety switch -a command line argument
yolo = ""                  # user's answer to safety switch (-a) question y/n

usage = f"""Yolo v0.2 - by @wunderwuzzi23

Usage: yolo [-a] list the current directory information
Argument: -a: Prompt the user before running the command (only useful when safety is off)

Current configuration per yolo.yaml:
* Model        : {config["model"]}
* Temperature  : {config["temperature"]}
* Max. Tokens  : {config["max_tokens"]}
* Safety       : {"on" if config["safety"] else "off"}
"""

if len(sys.argv) < 2:
  print(usage)
  sys.exit(-1)

if sys.argv[1] == "-a":
  ask_flag = True
  command_start_idx = 2

arguments = sys.argv[command_start_idx:]
user_prompt = " ".join(arguments)

init()

def can_copy():
  return not os.name == "posix" or not subprocess.check_output("echo $DISPLAY", shell=True) == b'\n'

while True:
  if user_prompt == "":
      print ("No user prompt specified.")
      sys.exit(-1)
  
  os_name = platform.system()
  if os_name == "Linux":
    os_name += distro.name(pretty=True)
  elif os_name == "Darwin":
    os_name += "/macOS"
  
  yolo_path = os.path.abspath(__file__)
  prompt_path = os.path.dirname(yolo_path)
  prompt_file = os.path.join(prompt_path, "prompt.txt")
  system_prompt = open(prompt_file,"r").read().replace("{shell}", shell).replace("{os}", os_name)
  
  if user_prompt[-1:] != "?" and user_prompt[-1:] != ".":
    user_prompt+="?"

  response = openai.ChatCompletion.create(
    model=config["model"],
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=config["temperature"],
    max_tokens=config["max_tokens"],
  )
  command = response.choices[0].message.content.strip()

  prefixes = ("sorry", "i'm sorry", "the question is not clear", "i'm", "i am")
  if command.lower().startswith(prefixes):
    print(colored("There was an issue: "+command, 'red'))
    sys.exit(-1)
  
  if command.count("```",2):
    print(colored("The proposed command contains markdown, so I did not execute the response directly: \n", 'red')+command)
    sys.exit(-1)
  
  print("Command: " + colored(command, 'blue'))
  if config["safety"] != "off" or ask_flag == True:
    print(f"Execute command? [Y]es [n]o [m]odify{' [c]opy to clipboard' if can_copy() else ''} ==> ", end = '')
    user_input = input()
  print()
  if user_input.upper() == "Y" or user_input == "":
    # Unix: /bin/bash /bin/zsh: uses -c both Ubuntu and macOS should work, others might not
    subprocess.run([shell, "/c" if shell == "powershell.exe" else "-c", command], shell=False)
  
  if user_input.upper() == "M":
    print("Modify prompt: ", end = '')
    user_query = input()
    continue
  
  if user_input.upper() == "C" and can_copy():
    pyperclip.copy(command)
    print("Copied command to clipboard.")
  break
