# AIPhotoFrame
[![last-commit](https://img.shields.io/github/last-commit/alexander-veselov/AIPhotoFrame)](https://github.com/alexander-veselov/AIPhotoFrame/commits/main/)

Display AI generated images in photo frame. 

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
- TBD

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

(More images TBD)
<p align="center">
    <img width="49%" src="https://github.com/user-attachments/assets/acfdada0-0c4c-4822-b97e-689a1e80440c"/>
</p>
