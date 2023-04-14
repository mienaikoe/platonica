from os import listdir, path
import random
from pygame import mixer

dir_path = path.dirname(path.realpath(__file__))
mixer.init()

SOUNDS_DIRECTORY = path.join(dir_path, '..', '..', 'assets', 'sounds')

class SoundEffect:
  def __init__(self, sound_name: str, volume=1.0):
    sound_directory = path.join(SOUNDS_DIRECTORY, sound_name)
    sound_files = [path.join(sound_directory, f) for f in listdir(sound_directory) if path.isfile(path.join(sound_directory, f))]
    self.sounds = [mixer.Sound(filename) for filename in sound_files]
    for sound in self.sounds:
      sound.set_volume(volume)

  def play(self):
    random.choice(self.sounds).play()