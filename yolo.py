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

from termcolor import colored
from colorama import init

# Check if the user globally disabled the safety switch
def get_yolo_safety_switch_config():
  
  home_path = os.path.expanduser("~")
  yolo_safety_off_path = os.path.join(home_path,".yolo-safety-off")
  
  if os.path.exists(yolo_safety_off_path):
    return False
  else:
    return True

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
  print("Yolo 0.1 - by @wunderwuzzi23")
  print()
  print("Usage: yolo [-a] list the current directory information")
  print("Argument: -a: Prompt the user before running the command")
  print()
  print("Current safety switch setting (~/.yolo-safety-off) is " + str(yolo_safety_switch))

def get_os_friendly_name():
  
  # Get OS Name
  os_name = platform.system()
  
  if os_name == "Linux":
      return "Linux/"+distro.name(pretty=True)
  elif os_name == "Windows":
      return os_name
  elif os_name == "Darwin":
     return "Darwin/macOS"


if __name__ == "__main__":

  # Get the global safety switch setting (default is True/on) 
  yolo_safety_switch = get_yolo_safety_switch_config()

  # Unix based SHELL (/bin/bash, /bin/zsh), otherwise assuming it's Windows
  shell = os.environ.get("SHELL", "powershell.exe") 

  command_start_idx  = 1      # Question starts at which argv index?
  ask_flag = False           # safety switch -a command line argument
  yolo = ""                  # user's answer to safety switch (-a) question y/n


  # Two options for the user to specify they openai api key.
  #1. Place a ".env" file in same directory as this with the line:
  #   OPENAI_API_KEY="<yourkey>"
  #   or do `export OPENAI_API_KEY=<yourkey>` before use
  dotenv.load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")
  #2. Place a ".openai.apikey" in the home directory that holds the line:
  #   <yourkey>
  if not openai.api_key:  #If statement to avoid "invalid filepath" error
    home_path = os.path.expanduser("~")    
    openai.api_key_path = os.path.join(home_path,".openai.apikey")

  # Parse arguments and make sure we have at least a single word
  if len(sys.argv) < 2:
    print_usage()
    sys.exit(-1)

  # safety switch via argument -a (local override of global setting)
  # Force Y/n questions before running the command
  if sys.argv[1] == "-a":
    ask_flag = True
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
 
  
  # Load the correct prompt based on Shell and OS and append the user's prompt
  prompt = get_full_prompt(user_prompt, shell)

  # Make the first line also the system prompt
  system_prompt = prompt[1]
  #print(prompt)

  # Call the ChatGPT API
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    temperature=0,
    max_tokens=500,
  )

#print (response)

res_command = response.choices[0].message.content.strip()

#Enable color output on Windows using colorama
init() 

if res_command.startswith("Sorry, try again") or res_command.startswith("I'm sorry"):
  print(colored("There was an issue: "+res_command, 'red'))
  sys.exit(-1)

# odd corner case, sometimes ChatCompletion returns markdown
if res_command.count("```",2):
  print(colored("The proposed command contains markdown, so I did not execute the response directly: \n", 'red')+res_command)
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