# AIPhotoFrame
[![last-commit](https://img.shields.io/github/last-commit/alexander-veselov/AIPhotoFrame)](https://github.com/alexander-veselov/AIPhotoFrame/commits/main/)

Display AI generated images in photo frame.

<img width="49%" src="https://github.com/user-attachments/assets/d1741d2f-e302-4ad7-934c-58aa75d427b1"/>

# Install
```bash
# Clone a repository
git clone https://github.com/alexander-veselov/AIPhotoFrame.git

# Create Python virtual environment
python3 -m venv venv

# Activate Python virtual environment
source ./venv/bin/activate
```

There are two display alternatives: pygame window or ILI9486 display

```
# pygame
pip3 install -r requirements.txt
```

```
# ILI9486
pip3 install -r requirements_ili9486.txt
```
In case if you are using ILI9486 and Raspberry Pi everything should work out of the box, but make sure that [SPI is enabled](https://github.com/alexander-veselov/ILI9486?tab=readme-ov-file#install).

# Stable Diffusion (AUTOMATIC1111) setup
Since Raspberry Pi is not capable enough for generating AI images using large generative models, a separate server is required.
[AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) can be used for such purposes.
Follow [Installation and Running](https://github.com/AUTOMATIC1111/stable-diffusion-webui?tab=readme-ov-file#installation-and-running) instructions.

To run AUTOMATIC1111 as a server that can be accessed using Raspberry Pi you need to run the ```webui-user.sh/bat``` with following parameters: ```--nowebui --api```. Windows example:
```batch
@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--nowebui --api

call webui.bat
```

After running server you will see server IP and port. E.g ```http://0.0.0.0:7861```.
To get public IP you can run ```ipconfig``` (on Windows) or ```ifconfig``` (on Linux).

#### Windows Firewall

Server still can be inaccessible from Raspberry Pi. If your server is running on Windows, check Windows Firewall settings.

As first step you can disable Firewall at all and check if it helps. If it helps and you still want to have Firewall enabled, you need to make a special rule for the port that server is using. Also double-check that there are no conflicting rules that are restricting connection. There may be a situation that Python has a rule to restrict all incoming connections. In such a case you need to disable or modify this rule.

# Usage
```bash
# Make sure venv is activated
python3 src/main.py --ip 192.168.0.1 --port 7861 --display pygame --prompt landscape
```

If you want to easily run an application remotely from machine that is currently running server, you can use following script (Windows): 
```batch
@echo off
setlocal

set /p prompt=Prompt: 

rem Remote machine IP
set REMOTE_IP=192.168.0.2

rem Server IP and port 
set SERVER_IP=192.168.0.1
set SERVER_PORT=7861

rem Project path at remote machine
set PROJECT_PATH=Projects/AIPhotoFrame

rem May be necessary if pygame is selected instead of ili9486
set DISPLAY=:0

ssh -t pi@%REMOTE_IP% "export DISPLAY=%DISPLAY% && cd %PROJECT_PATH% && source ./venv/bin/activate && python3 src/main.py --ip %SERVER_IP% --port %SERVER_PORT% --display ili9486 --prompt \"%prompt%\""

endlocal
```

# Hardware
- Tested on Raspberry Pi 5 only
- Display: 3.5 inch RPi LCD Display

# Photos
Note: In real life, the display has nice, rich colors without any artifacts. Artifacts present in photographs are camera distortions.

<p align="center">
    <img width="49%" src="https://github.com/user-attachments/assets/1b668564-db97-49ea-bce1-857dd7d07d60"/>
&nbsp;
    <img width="49%" src="https://github.com/user-attachments/assets/136eb35a-bfaf-41a0-8862-b7a0bfa74b49"/>
</p>

<p align="center">
    <img width="49%" src="https://github.com/user-attachments/assets/4ae8bff5-11cf-41fe-9e69-8f16b0a283ca"/>
&nbsp;
    <img width="49%" src="https://github.com/user-attachments/assets/fbd3e379-6b68-474c-be10-a19f05d94e9a"/>
</p>

<p align="center">
    <img width="49%" src="https://github.com/user-attachments/assets/6ac2162a-0fc4-42d0-b136-469e82aae32e"/>
&nbsp;
    <img width="49%" src="https://github.com/user-attachments/assets/5d03eb77-1889-4fa1-b94a-791016fcf514"/>
</p>
