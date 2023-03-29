#!/usr/bin/env python3

# MIT License
# Copyright (c) 2023 wunderwuzzi23
# Greetings from Seattle! 

import os, platform, openai, sys, subprocess, dotenv, distro, yaml, pyperclip, termcolor, colorama

prompt_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(prompt_path, "yolo.yaml"), 'r') as file:
  config = yaml.safe_load(file)

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:  #If statement to avoid "invalid filepath" error
  openai.api_key_path = os.path.join(os.path.expanduser("~"),".openai.apikey")
if not openai.api_key:  
  openai.api_key = config["openai_api_key"]

shell = os.environ.get("SHELL", "powershell.exe")
usage = f"""Yolo v0.2 - by @wunderwuzzi23

Usage: yolo [-a] list the current directory information
Argument: -a: turn safety on

Current configuration per yolo.yaml:
* Model        : {config["model"]}
* Temperature  : {config["temperature"]}
* Max. Tokens  : {config["max_tokens"]}
"""
if len(sys.argv) < 2:
  print(usage)
  sys.exit(-1)
user_prompt = " ".join(sys.argv[1:])
colorama.init()

while True:
  if user_prompt == "":
      print ("No user prompt specified.")
      sys.exit(-1)
  
  os_name = platform.system()
  if os_name == "Linux":
    os_name += distro.name(pretty=True)
  elif os_name == "Darwin":
    os_name += "/macOS"
  
  with open(os.path.join(prompt_path, "prompt.txt"), 'r') as file:
    system_prompt = file.read().replace("{shell}", shell).replace("{os}", os_name)
  
  if user_prompt[-1:] != "?" and user_prompt[-1:] != ".":
    user_prompt+="?"

  command = openai.ChatCompletion.create(
    model=config["model"],
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=config["temperature"],
    max_tokens=config["max_tokens"],
  ).choices[0].message.content.strip()

  if command.lower().startswith(("sorry", "i'm sorry", "the question is not clear", "i'm", "i am")):
    print("There was an issue: "+command, file=sys.stderr)
    sys.exit(-1)
  
  if command.count("```",2):
    print("The proposed command contains markdown, so I did not execute the response directly: \n"+command, file=sys.stderr)
    sys.exit(-1)
  
  print("Command: " + termcolor.colored(command, 'blue'))
  try:
    pyperclip.copy(command)
    print("Copied command to clipboard.")
  except:
    pass
  print(f"Execute command? [Y]es [n]o [m]odify ==> ", end = '')
  user_input = input()
  print()
  if user_input.upper() == "Y" or user_input == "":
    # Unix: /bin/bash /bin/zsh: uses -c both Ubuntu and macOS should work, others might not
    subprocess.run([shell, "/c" if shell == "powershell.exe" else "-c", command], shell=False)
  
  if user_input.upper() == "M":
    print("Modify prompt: ", end = '')
    user_query = input()
    continue
  break
