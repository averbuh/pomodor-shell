from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from pygame import mixer


audio_link='/home/alex/database/scripts/python/tomato_app/flute.wav'


def soundplay():
    mixer.init()
#   mixer.music.load("tomato_app/mixkit-woosh-wind-1168.wav")
    mixer.music.load(audio_link)
    mixer.music.play()
