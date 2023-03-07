# Install (Linux instructions)

```
git clone https://github.com/wunderwuzzi23/yolo-ai-cmdbot
cd yolo-ai-cmdbot
pip3 install -r requirements.txt
chmod +x yolo.py
alias yolo=$(pwd)/yolo.py
alias computer=$(pwd)/yolo.py #optional
```

## Aliases

To set the alias on each login, add them to your .bashrc or .bash_aliases file.

```
echo "alias yolo=$TARGET_FULLPATH"     >> ~/.bash_aliases
echo "alias computer=$TARGET_FULLPATH" >> ~/.bash_aliases
```

## Yolo in Action

![Animated GIF](https://github.com/wunderwuzzi23/blog/raw/master/static/images/2023/yolo-shell-anim-gif.gif)

## Installation script

Another option is to run `source install.sh` after cloning the repo. That does the following:
1. Copies the necessary files to `~/yolo-ai-cmdbot/`
2. Creates two aliases `yolo` and `computer` pointint to `~/yolo-ai-cmdbot/yolo.py`
3. Adds the aliases to the `~/bash_aliases` file (only tested on Ubuntu)

That's it. Now make sure you have an OpenAI API key set.

## Installation script (Windows)

For windows you can run `.\install.bat` (or double-click) after cloning the repo. It will do the following:
1. Copies the necessary files to `~/yolo-ai-cmdbot/`
2. Creates a `yolo.bat` file in `~` that lets you run equivalent to `python.exe ~\yolo-ai-cmdbot\yolo.py`
3. Creates a `.env` file in `~/yolo-ai-cmdbot/`

You may also edit `install.bat`:
- Changing `set INSTALL_DIR=%HOME%` to `set INSTALL_DIR={Enter directory path}` will change where the `\yolo-ai-cmdbot` folder will be made
- Similarly, changing `set SCRIPT_DIR=%HOME%` to `set SCRIPT_DIR={Enter directory path}` will change where `yolo.bat` script will be made.
- Uncommenting `::call :install_yolo_repository` and commenting `call :install_yolo_directory` will let you use the repository `yolo.py` instead of a seperate directory (And won't make the extra directory)
- Uncommenting `::call :create_openai_apikey` will create a `.openai.apikey` file at the `~` directory
- Uncommenting `::call :create_safety_off` will create a `.yolo-safety-off` file at the `~` directory

That's it. Now make sure you have an OpenAI API key set.

# macOS 

On make OS (when using `zsh`) you can't end your instructions with a question mark (unless you put the question/instructions into a string 'whats the time?'). Hoever, yolo adds a question mark regardless if there is no . or ? at the end.

# Windows

Windows is less tested, it does work though and will use PowerShell.

`python.exe yolo.py what is my username`

If you use `install.bat` you should have a `yolo.bat` file in your `~` directory that lets you run the command like so:

`.\yolo.bat what is my username`

you can put the `yolo.bat` file into a $PATH directory (like `C:\Windows\System32`) to use in any directory

Have fun.

# OpenAI API Key configuration

There are two ways to configure the key:
- You can either `export OPENAI_API_KEY=<yourkey>`, or have a `.env` file in the same directory as `yolo.py` with `OPENAI_API_KEY="<yourkey>"` as a line
- Create a file at `~/.openai.apikey` with the key in it

# Using yolo

By default `yolo` will prompt the user before executing commands.

## Disabling the safety switch!

To disable the default behavior and have yolo run commands right away when they come back from ChatGPT create a file named `~/.yolo-safety-off`

A simple command to do that on Linux would be:

```
touch ~/.yolo-safety-off
```

If you still want to inspect the command that is executed when safety is off, add the `-a` argument, e.g `yolo -a delete the file test.txt`.

Let's go!

# Demo Video on YouTube

https://www.youtube.com/watch?v=g6rvHWpx_Go

[![Watch the video](https://embracethered.com/blog/images/2023/yolo-thumbnail-small.png)](https://www.youtube.com/watch?v=g6rvHWpx_Go)


## Examples

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
