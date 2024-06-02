# Yolo Demo

![Animated GIF](https://github.com/wunderwuzzi23/blog/raw/master/static/images/2023/yolo-shell-anim-gif.gif)

# Update Yolo v0.4 - Support for Groq

* Added groq support. You can get an API key at `https://console.groq.com` and set mode to for instance `llama3-8b-8192`. groq is lightning fast. 
* Simplified and improved default `prompt.txt`, 
* Note: Testing shows that model `gpt-4o` gives the best results.


# Update Yolo v0.3 - Support for Azure OpenAI

* Key changes are upgrades to the latest OpenAI libraries and support for Azure OpenAI. There is an `api` key in the `yolo.yaml` that can be set to `azure_openai` and then you can provide all the parameters accordingly in the yaml file as well (`api-version`, your `azure-endpoint`,...). The api key for azure is called `AZURE_OPENAI_API_KEY` by the way. It can be set via environment variable and config file.
* It's now possible to change the color of the suggested command via config file
* The "modify prompt" feature is now optional and can be toggled via config file.
* Minor bug fixes (like copy to clipboard should work on macOS)

Tested on macOS and Linux. Windows hopefully still works also.

# Update Yolo v0.2 - Support for GPT-4 API

This update introduces the `yolo.yaml` configuration file. In this file you can specify which OpenAI model you want to query, and other settings. The safety switch also moved into this configuration file.

For now the default model is still `gpt-3.5-turbo`, but you can update to `gpt-4` if you have gotten access already!

```
Yolo v0.3 - by @wunderwuzzi23

Usage: yolo [-a] list the current directory information
Argument: -a: Prompt the user before running the command (only useful when safety is off)

Current configuration per yolo.yaml:
* API          : openai
* Model        : gpt-4-turbo-preview
* Temperature  : 0
* Max. Tokens  : 500
* Safety       : True
* Command Color: blue
```

Happy Hacking!

# Installation on Linux and macOS

```
git clone https://github.com/wunderwuzzi23/yolo-ai-cmdbot
cd yolo-ai-cmdbot
pip3 install -r requirements.txt
chmod +x yolo.py
alias yolo=$(pwd)/yolo.py
alias computer=$(pwd)/yolo.py #optional

yolo show me some funny unicode characters
```

## OpenAI API Key configuration

There are three ways to configure the key on Linux and macOS:
- You can either `export OPENAI_API_KEY=<yourkey>`, or have a `.env` file in the same directory as `yolo.py` with `OPENAI_API_KEY="<yourkey>"` as a line
- Create a file at `~/.openai.apikey` with the key in it
- Set the key in the `yolo.yaml` configuration file

### Azure OpenAI Key configuration
There are three ways to configure the key on Linux and macOS:
- You can either `export AZURE_OPENAI_API_KEY=<yourkey>`, or have a `.env` file in the same directory as `yolo.py` with `AZURE_OPENAI_API_KEY="<yourkey>"` as a line
- Create a file at `~/.azureopenai.apikey` with the key in it
- Set the key in the `yolo.yaml` configuration file

### Groq Configuration
- Grab an API key from `console.groq.com` 
- You can either `export GROQ_API_KEY=<yourkey>`, or have a `.env` file in the same directory as `yolo.py` with `GROQ_API_KEY="<yourkey>"` as a line
- Set `api` and `model` (e.g llama3-8b-8192) in `yolo.yaml` configuration file

## Aliases

To set the alias, like `yolo` or `computer` on each login, add them to .bash_aliases (or .zshrc on macOS) file. Make sure the path is the one you want to use.

```
echo "alias yolo=$(pwd)/yolo.py"     >> ~/.bash_aliases
echo "alias computer=$(pwd)/yolo.py" >> ~/.bash_aliases
```

## Installation script

Another option is to run `source install.sh` after cloning the repo. That does the following:
1. Copies the necessary files to `~/yolo-ai-cmdbot/`
2. Creates two aliases `yolo` and `computer` pointint to `~/yolo-ai-cmdbot/yolo.py`
3. Adds the aliases to the `~/.bash_aliases` or `~/.zshrc` file

That's it for Linux and macOS. Now make sure you have an OpenAI API key set.

# Windows Installation

On Windows you can run `.\install.bat` (or double-click) after cloning the repo. By default it does the following:
1. Copies the necessary files to `~\yolo-ai-cmdbot\`
2. Creates a `yolo.bat` file in `~` that lets you run equivalent to `python.exe ~\yolo-ai-cmdbot\yolo.py`

You also have the option to:
1. Change the location where `yolo-ai-cmdbot\` and `yolo.bat` will be created
2. Skip creating `yolo-ai-cmdbot\` and use the folder of the cloned repository instead.
3. Create a `.openai.apikey` file in your `~` directory

That's it basically.

## OpenAI API Key Configuration on Windows

On Windows `export OPENAI_API_KEY=<yourkey>` will not work instead:
- Run `$env:OPENAI_API_KEY="<yourkey>"` to set key for that terminal
- Or, Run PowerShell as administrator and run `setx OPENAI_API_KEY "<yourkey>"`
- Or, Go to `Start` and search `edit environment variables for your account` and manually create the variable with name `OPENAI_API_KEY` and value `<yourkey>`

Optionally (since v.0.2), the key can also be stored in `yolo.yaml`.

If you want to use Azure, the the key is called `AZURE_OPENAI_API_KEY`.

## Running yolo on Windows 

Windows is less tested, it does work though and will use PowerShell.

```
python.exe yolo.py what is my username
```

That's it.

## yolo.bat

If you use `install.bat` you should have a `yolo.bat` file in your `~` directory that lets you run the command like so:

```
.\yolo.bat what is my username
```

You can put the `yolo.bat` file into a $PATH directory (like `C:\Windows\System32`) to use in any directory like so:

```
yolo what is my username
```

Have fun.

# Disabling the safety switch! **Caution!**

By default `yolo` will prompt the user before executing commands. 

Since v.0.2 the safety switch setting moved to `yolo.yaml`, the old `~/.yolo-safety-off` is not used anymore. 

To have yolo run commands right away when they come back from ChatGPT change the `safety` in the `yolo.yaml` to `False`.

If you still want to inspect the command that is executed when safety is off, add the `-a` argument, e.g `yolo -a delete the file test.txt`.

Let's go!

# Demo Video on YouTube

https://www.youtube.com/watch?v=g6rvHWpx_Go

[![Watch the video](https://embracethered.com/blog/images/2023/yolo-thumbnail-small.png)](https://www.youtube.com/watch?v=g6rvHWpx_Go)


# Examples

Here are a couple of examples on how this utility can be used.

```
yolo whats the time?
yolo whats the time in UTC
yolo whats the date and time in Vienna Austria
yolo show me some unicode characters
yolo what is my user name and whats my machine name?
yolo is there a nano process running
yolo download the homepage of ycombinator.com and store it in index.html
yolo find all unique urls in index.html
yolo create a file named test.txt and write my user name into it
yolo print the contents of the test.txt file
yolo -a delete the test.txt file
yolo whats the current price of Bitcoin in USD
yolo whats the current price of Bitcoin in USD. Ext the price only
yolo look at the ssh logs to see if any suspicious logons accured
yolo look at the ssh logs and show me all recent logins
yolo is the user hacker logged on right now?
yolo do i have a firewall running?
yolo create a hostnames.txt file and add 10 typical hostnames based on planet names to it, line by line, then show me the contents
yolo find any file with the name yolo.py. do not show permission denied errors
yolo write a new bash script file called scan.sh, with the contents to iterate over hostnames.txt and invokes a default nmap scan on each host. then show me the file. 
yolo write a new bash script file called scan.sh, with the contents to iterate over hostnames.txt and invokes a default nmap scan on each host. then show me the file. Make it over multiple lines with comments and annotiations.
```

# Thanks!

# License

MIT. No Liability. No Warranty. But lot's of fun.
