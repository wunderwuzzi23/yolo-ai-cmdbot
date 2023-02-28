# Install (Linux instructions)

```
git clone https://github.com/wunderwuzzi23/yolo-ai-cmdbot
cd yolo-ai-cmdbot
pip install -r requirements.txt
chmod +x yolo.py
alias yolo=$(pwd)/yolo.py
```

# Windows

You can use: `pyinstaller yolo.py --onefile` to get a single `yolo.exe` to run.
Windows is less tested, but it does work.

# OpenAI API Key configuration

There are two ways to configure the key:
- You can either `export OPENAI_API_KEY=<yourkey>`
- Create a file at `~/.openai.apikey` with the key in it

# Using yolo

Here are a couple of examples on how this utility can be used.

**WARNING**: By default the command that comes back from GPT-3 will be immediatly executed (yolo!). 

If you want to inspect the command that is executed, add the `-a` argument, e.g `yolo -a delete the file test.txt`.

More examples:

```
yolo whats the time?
yolo whats the time in UTC
yolo is there an ssh-agent process running
yolo create a file named test.txt and write my user name into it
yolo print the contents of the test.txt file
yolo -a delete the test.txt file
yolo whats the current price of Bitcoin in USD
yolo whats the current price of Bitcoin in USD. Extract the price only
yolo look at the ssh logs to see if any suspicious logons accured
yolo is the user hacker logged in right now?
yolo do i have a firewall running?
yolo create a hostnames.txt file and add 10 typical hostnames based on planet names to it
yolo write a new bash script file called scan.sh, with the contents to  iterate over hostnames.txt and invokes a default nmap scan on each host. Make it over multiple lines with comments and annotiations.
```

# License

MIT. No Liability. No Warranty. But lot's of fun.
