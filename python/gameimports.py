import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import sys
import json
from skeleton import *
from data import *
from delay import *
from game import *
from pvegame import *
import requests
import threading
import json
import time
from flask_socketio import SocketIO, emit
from socketio import Client