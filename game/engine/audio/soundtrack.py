from enum import Enum
from os import listdir, path
from engine.events import MUSIC_TRACK_END
from pygame import mixer
import pygame

dir_path = path.dirname(path.realpath(__file__))
mixer.init()


class SoundtrackSong(Enum):
  water = "water"


FADE_OUT_TIME = 1000


MUSIC_DIRECTORY = path.join(dir_path, '..', '..', 'assets', 'music')
TRACK_ATLAS = dict()
for song_name in SoundtrackSong:
  song_directory = path.join(MUSIC_DIRECTORY, song_name.value)
  song_files = [path.join(song_directory, f) for f in listdir(song_directory) if path.isfile(path.join(song_directory, f))]
  TRACK_ATLAS[song_name] = sorted(song_files)


class Soundtrack:

  def __init__(self):
    self.tracks = None
    self.track_num = 0
    mixer.music.set_endevent(MUSIC_TRACK_END)
    print("init new soundtrack")

  def handle_event(self, event: pygame.event.Event, world_time: int):
    if event.type == MUSIC_TRACK_END:
      print("Music Track End", self.track_num)
      mixer.music.queue(self.tracks[self.track_num])

  def set_song(self, song_name: SoundtrackSong):
    self.tracks = TRACK_ATLAS[song_name]
    print("set song", self.tracks)
    mixer.music.load(self.tracks[self.track_num])

  def set_volume(self, vol: float):
    mixer.music.set_volume(vol)

  def play(self):
    mixer.music.play()
    mixer.music.queue(self.tracks[self.track_num])

  def advance(self):
    print("advancing")
    self.track_num += 1
    print(self.tracks[self.track_num])
    mixer.music.queue(self.tracks[self.track_num])
    if self.track_num >= len(self.tracks) - 1:
      mixer.music.set_endevent() # stops event firing