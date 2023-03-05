# Install (Linux instructions)

```
git clone https://github.com/wunderwuzzi23/yolo-ai-cmdbot
cd yolo-ai-cmdbot
pip install -r requirements.txt
chmod +x yolo.py
alias yolo=$(pwd)/yolo.py
alias computer=$(pwd)/yolo.py #optional
```

Another option is to run `source install.sh` after cloning the repo. That does the following:
1. Copies the necessary files to `~/yolo-ai-cmdbot/`
2. Creates two aliases `yolo` and `computer` pointint to `~/yolo-ai-cmdbot/yolo.py`


# macOS 

I haven't tested it yet, but it should just work :)

# Windows

Windows is less tested, it does work though and will use PowerShell.

`python.exe yolo.py what is my username`

Have fun.

# OpenAI API Key configuration

There are two ways to configure the key:
- You can either `export OPENAI_API_KEY=<yourkey>`
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
