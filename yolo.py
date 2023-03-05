#!/usr/bin/env python3

# MIT License
# Copyright (c) 2023 wunderwuzzi23
# Greetings from Seattle! 

import os
import openai
import sys
import subprocess
from termcolor import colored
from colorama import init

yolo_safety_switch = True  # by default, user is prompted to run each command
ask_flag = False           # safety switch -a command line argument
yolo = ""                  # user's answer to safety switch (-a) question y/n
command_start_idx = 1      # command starts at which argv index?
home_path = os.path.expanduser("~")

# Two options for the user to specify they openai api key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path = os.path.join(home_path,".openai.apikey")

# Check if the user globally disabled the safety switch
yolo_safety_off_path = os.path.join(home_path,".yolo-safety-off")
if os.path.exists(yolo_safety_off_path):
  yolo_safety_switch = False
else:
  yolo_safety_switch = True

# Parsing weirdness
if len(sys.argv) < 2:
  print("Yolo 0.1 - by @wunderwuzzi23")
  print()
  print("Usage: yolo [-a] list the current directory information")
  print("Argument: -a: Prompt the user before running the command")
  print()
  print("Current safety switch setting (~/.yolo-safety-off) is " + str(yolo_safety_switch))
  sys.exit(-1)

# safety switch (no yolo mode)
if sys.argv[1] == "-a":
  ask = True
  command_start_idx = 2

# to allow easy/natural use we don't require the input to be a 
# single string. So, the user can just type yolo what is my name?
# without having to put the question between ''
arguments = sys.argv[command_start_idx:]
user_prompt = " ".join(arguments)

# do we have a prompt from the user?
if user_prompt == "":
    print ("No user prompt specified.")
    sys.exit(-1)

# Get shell info for a better prompt
# Unix based SHELL (/bin/bash, /bin/zsh), otherwise assuming it's Windows
shell = os.environ.get("SHELL", "powershell.exe")    

# Construct the prompt

## Find the executing directory (e.g. in case an alias is set)
## So we can find the prompt.txt file
yolo_path = os.path.abspath(__file__)
prompt_path = os.path.dirname(yolo_path)

## Load the prompt and prep it
prompt_file = os.path.join(prompt_path, "prompt.txt")
pre_prompt = open(prompt_file,"r").read()
pre_prompt = pre_prompt.replace("{}", shell)
prompt = pre_prompt + user_prompt

## make the first line also the system prompt
system_prompt = pre_prompt[1]

# be nice and make it a question
if prompt[-1:] != "?":
  prompt+="?"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": prompt}
  ],
  temperature=0,
  max_tokens=100,
  # top_p=1,
  # frequency_penalty=0.2,
  # presence_penalty=0
)

#print (response)

res_command = response.choices[0].message.content.strip()

#enable color output on Windows using colorama
init() 

if res_command.startswith("Sorry, try again") or res_command.startswith("I'm sorry"):
  print(colored("There was an issue: "+res_command, 'red'))
  sys.exit(-1)

# odd corner case, sometimes ChatCompletion returns markdown
if res_command.count("```",2):
  print(colored("The proposed command contains markdown, so I thought to not execute the response directly: \n", 'red')+res_command)
  sys.exit(-1)

print("Command: " + colored(res_command, 'blue'))
if yolo_safety_switch == True or ask_flag == True:
  print("Execute the command? Y/n ==> ", end = '')
  yolo = input()
  print()

if yolo == "Y" or yolo == "":
  if shell == "powershell.exe":
    subprocess.run([shell, "/c", res_command], shell=False)  
  else: 
    # Unix: /bin/bash /bin/zsh: uses -c both Ubuntu and macOS should work, others might not
    subprocess.run([shell, "-c", res_command], shell=False)

