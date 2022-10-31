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
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import json
import gym
import cv2
import imageio


def make_gif(game_name):
    """
    Making a gif
    """
    frame_buffer = []
    env = gym.make("AIArcade-v0", config=game_name)
    img = env.reset()
    done = False
    steps = 0

    while not done and steps < 200:
        sample = env.action_space.sample()
        s, r, done_local = env.steps(sample)
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

# create an image for each game
for file in files:
    if file.endswith(".json"):
        with open("./ai_arcade/predefined_games/"+files) as f:
            config = json.load(f)

        if "meta" in config:
            desc = config['meta']['description']
        else:
            desc = "Not Available"

        game_name = file.split(".")[0]

        # get the words in the name and capitalize
        game_name.replace("_", " ")
        game_name.replace("-", " ")
        game_name_title = game_name.title()

        # make gif game_name
        env = gym.make("AIArcade-v0", config=game_name)
        img = env.reset()

        # play a few steps to get game started
        for i in range(80):
            a = env.action_space.sample()
            img, _, done, _ = env.step(a)
            if done:
                img = env.reset()

            img = cv2.resize(img, (150, 150))
            img = img[:, :, ::-1]
            cv2.imwrite("./readme_content/"+game_name+".png", img)

            readme_lines.append("| ![](./readme_content/"+game_name+".gif) | "+game_name_title+" | "+desc+" |\n")

# write
out_file = open("README.md", "w")
for line in readme_lines:
    out_file.write(line)
out_file.close()




