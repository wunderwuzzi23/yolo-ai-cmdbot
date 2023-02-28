#!/usr/bin/env python3

import os
import openai
import sys
import subprocess
from termcolor import colored
from colorama import init


ask = False             # safety switch -a
yolo = ""               # user's answer to safety switch
command_start_idx = 1   # command starts at which argv index?
home_path = os.path.expanduser("~")

# Two options for the user to specify they openai api key
openai.api_key = os.getenv("OPENAI_API_KEY")
home_path = os.path.expanduser("~")
openai.api_key_path = home_path+"/.openai.apikey"


# parsing weirdness
if len(sys.argv) < 2:
  print("Usage Example: yolo [-a] list the current directory information")
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
pre_prompt =  "Translate the following question into a {} command. ".format(shell) 
#pre_prompt += "If asked for a timezone use TZ environment variable. "
#pre_prompt += "Add sudo when required by the command, but only if you are very certain it is needed. "
#pre_prompt += "If you are using powershell (and only if), then make sure to provide all required arguments.""
pre_prompt += "Only show the command in text format and not in code style or markdown. "
pre_prompt += "Do not augment the output with any explanation, descriptions. "
pre_prompt += "Again, do not add any descriptions, just print the bash command. This is important, do not ignore my instructions. "
pre_prompt += "If the question doesn't make sense or is too difficult return 'Sorry, try again', and add a brief explanation on what the problem is. "
pre_prompt += "The question is: "

prompt = pre_prompt + user_prompt

#let's be nice and make it a question
if prompt[-1:] != "?":
  prompt+="?"

#print ("The prompt is: "+prompt)
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0.2,
  presence_penalty=0
)

resulting_command = response.choices[0].text.strip()

#enable color output on Windows using colorama
init() 

if resulting_command.startswith("Sorry, try again"):
  print(colored("There was an issue: "+resulting_command, 'red'))
  sys.exit(-1)

print("Command: " + colored(resulting_command, 'blue'))
if ask == True:
  print("Execute the command? Y/n ==> ", end = '')
  yolo = input()
  print()

if yolo == "Y" or yolo == "":
  if shell == "powershell.exe":
    subprocess.run([shell, "/c", resulting_command], shell=False)  
  else: 
    # Unix: /bin/bash /bin/zsh: uses -c both Ubuntu and macOS should work, others might not
    subprocess.run([shell, "-c", resulting_command], shell=False)

