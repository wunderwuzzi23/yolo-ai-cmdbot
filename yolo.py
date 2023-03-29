#!/usr/bin/env python3

# MIT License
# Copyright (c) 2023 wunderwuzzi23
# Greetings from Seattle! 

import os, platform, openai, sys, subprocess, distro, pyperclip, termcolor, colorama

colorama.init()
os_name = platform.system()
if os_name == "Linux": os_name += distro.name(pretty=True)
if os_name == "Darwin": os_name += "/macOS"
shell = os.environ.get("SHELL", "powershell.exe")
messages = [{"role": "system", "content": f"Translate to one line of input for the shell {shell} on {os_name}."}]
try:
  model = "gpt-4" if any(engine.id == 'gpt-4' for engine in openai.Engine.list().data) else "gpt-3.5-turbo"
except openai.error.AuthenticationError:
  print("Set the environment variable OPENAI_API_KEY=<API-KEY>. Don't know how to do that? I'll tell you... given an API key.", file=sys.stderr)
  sys.exit(1)
blather = print if len(sys.argv) == 1 else lambda *args, **kwargs: print(*args[1:], **kwargs)
try:
  blather("Describe a shell command, or Ctrl-C to exit. ==> ", end = '')
  query = input() if len(sys.argv) == 1 else " ".join(sys.argv[1:])
  while True:
    messages.append({"role": "user", "content": query})
    command = openai.ChatCompletion.create(messages=messages, model=model, temperature=0, max_tokens=500).choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": command})
    blather("Command: ", termcolor.colored(command, 'blue'))
    try:
      pyperclip.copy(command)
      blather("Copied command to clipboard.\n", end='')
    except:
      pass
    blather(f"Enter to execute, or continue conversing. ", "==> ", end = '')
    query = input()
    if not query:
      # Unix: /bin/bash /bin/zsh: uses -c both Ubuntu and macOS should work, others might not
      subprocess.run([shell, "/c" if shell == "powershell.exe" else "-c", command], shell=False)
      print("==> ", end = '')
      query = input()
except KeyboardInterrupt:
  sys.exit(0)