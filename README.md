# Smart Seat GUI
Require: python 3.8

## Installation
Create an venv environment is recommended.  

0. Install venv (skip if you already installed venv)
    - `python -m pip install venv`
1. clone this repository
    - `git clone https://github.com/aclich/smart-seat-GUI.git`  
and change the directory
    - `cd smart-seat-GUI`

2. Create new venv environemnt
    - `python -m venv venv`
3. Activate the venv environment
    - Windows 
      - `.\venv\Scripts\activate`
    - Linux
      - `./venv/bin/activate`
4. Install the requirements
    - `python -m pip install -r requirements.txt`
5. Run the application
    - `python main.py`

### Backend setup
- https://github.com/aclich/smart-seat-api
- TODO
### Arduino setup
- TODO

## TODO  
- REDME
- Web connection
  - http connector ✅
  - login ✅
  - upload data 
  - connection try exception
- Sit pose detection
  - data collector ✅
  - models 
    - RF ✅
    - ANN
  - real-time predict
- GUI
  - Login fail
  - Input Data check
  - Page swithch(data collect & user mode)
  - code rearrange
