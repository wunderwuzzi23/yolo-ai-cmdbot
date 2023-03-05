# Installs yolo in the user's home directory

TARGET_DIR=~/yolo-ai-cmdbot
TARGET_FULLPATH=$TARGET_DIR/yolo.py

mkdir -p $TARGET_DIR
cp yolo.py prompt.txt $TARGET_DIR
chmod +x $TARGET_FULLPATH

# Creates two aliases for use
alias yolo=$TARGET_FULLPATH
alias computer=$TARGET_FULLPATH

# Add the aliases to the logon scripts
echo "alias yolo=$TARGET_FULLPATH"     >> ~/.bash_aliases
echo "alias computer=$TARGET_FULLPATH" >> ~/.bash_aliases
