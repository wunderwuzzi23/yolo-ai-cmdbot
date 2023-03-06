# Installs yolo in the user's CMD directory ( change $CMD to desired file path )

TARGET_DIR=$CMD
TARGET_FULLPATH=$TARGET_DIR/yolo.py

mkdir -p $TARGET_DIR
cp yolo.py $TARGET_DIR
cp prompt.txt $TARGET_DIR/yolo_prompt.txt #changed this so it doesnt conflict with possible future prompts
chmod +x $TARGET_FULLPATH

# Adds batch file to System32 so you can call it in powershell
cp yolo.bat C:/Windows/System32