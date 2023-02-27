# Install (Linux instructions)

```
git clone https://github.com/wunderwuzzi23/yolo-ai-cmdbot
cd yolo-ai-cmdbot
pip install -r requirements.txt
chmod +x yolo.py
alias yolo=$(pwd)/yolo.py
```

## OpenAI API Key configuration

There are two ways to configure the key:
- You can either `export OPENAI_API_KEY=<yourkey>`
- Create a file at `~/.openai.apikey` with the key in it

# Using yolo

Here are a couple of examples. By default the command that comes back from GPT-3 will be immediatly executed (yolo!). 

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
```

# License

MIT. No Liability. No Warranty. But lot's of fun.
