"""
Copyright © 2021 The Johns Hopkins University Applied Physics Laboratory LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import gym
import os
import numpy as np
import cv2
import json
import imageio


def make_gif(game_name):
    frame_buffer = []
    env = gym.make("AIArcade-v0", config=game_name)
    img = env.reset()
    done = False
    steps = 0

    while not done and steps < 200:
        a = env.action_space.sample()
        s, r, done, info = env.steps(a)
        s = cv2.resize(s, (150, 150))
        frame_buffer.append(s)
        steps += 1

    # make gif from buffer, down-select frames so gifts are not too large
    imageio.mimsave("./readme_content/"+game_name+".gif", frame_buffer[::4], duration=0.02)


# read in the intro
file1 = open('./readme_content/rmintro.md', 'r')
readme_lines = file1.readlines()

readme_lines.append("| Image | Name | Description | \n")
readme_lines.append("| :---: | :---: | :---: |\n")

# sort the game alphabetically
files = os.listdir("./ai_arcade/predefined_games/")
files.sort(files)


