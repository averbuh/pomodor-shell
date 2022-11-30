from os import environ
from pygame import mixer
from settings import AUDIO
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'







def soundplay():
    mixer.init()
    mixer.music.load(AUDIO)
    mixer.music.play()
