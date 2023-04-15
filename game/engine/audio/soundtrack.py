from enum import Enum
from os import listdir, path
from engine.events import MUSIC_TRACK_END, LEVEL_LOADED, PUZZLE_LOADED
from pygame import mixer
import pygame

dir_path = path.dirname(path.realpath(__file__))
mixer.init()


class SoundtrackSong(Enum):
  water = "water"


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

  def handle_event(self, event: pygame.event.Event, world_time: int):
    if event.type == MUSIC_TRACK_END:
      mixer.music.queue(self.tracks[self.track_num])
    elif event.type == LEVEL_LOADED:
      mixer.music.fadeout(100)
      self.set_song(event.__dict__['song'])
    elif event.type == PUZZLE_LOADED:
      if mixer.music.get_busy():
        self.advance()
      else:
        self.play()

  def set_song(self, song_name: SoundtrackSong):
    self.track_num = 0
    self.tracks = TRACK_ATLAS[song_name]
    mixer.music.load(self.tracks[self.track_num])

  def set_volume(self, vol: float):
    mixer.music.set_volume(vol)

  def play(self):
    mixer.music.play()
    mixer.music.queue(self.tracks[self.track_num])

  def advance(self):
    if self.track_num >= len(self.tracks) - 1:
      return
    self.track_num += 1
    mixer.music.queue(self.tracks[self.track_num])
    if self.track_num >= len(self.tracks) - 1:
      mixer.music.set_endevent() # stops event firing