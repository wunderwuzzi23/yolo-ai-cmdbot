# Install (Linux instructions)

```
pip install -r requirements.txt
chmod +x yolo.py
alias yolo=$(pwd)/yolo.py
```

# Use 

Here are a couple of examples. By default the command that comes back from GPT-3 will be immediatly executed (yolo!). If you want to inspect the command before running add the `-a` argument, e.g `yolo -a delete the file test.txt`.

More examples:

```
yolo whats the time?
yolo whats the time in UTC?
yolo is there a ssh-agent process running
yolo create a file named test.txt and write my user name into it
yolo print the contents of the test.txt file
yolo -a delete the test.txt file
```

# License

MIT. No Liability. No Warranty. But lot's of fun.