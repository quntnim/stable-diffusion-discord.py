<div align="center">
    <h1> | stable-diffusion-discord.py | </h1>
    <p><a href="https://github.com/quntnim/stable-diffusion-discord.py/blob/main/README.md">한국어</a> / ENG</p>
</div>

A project to make Stable Diffusion into a Discord bot using Stable Diffusion Web UI API
## Features


| Features | Progress |
| --- | --- |
| txt2img | 60% |
| img2img | todo |
| extras | todo |
| png info | todo |
| options | 40% |
| controlnet | todo |

## Commands

### /register

- Register your information in Discord Bot.

### /profile {user}

- Shows a user's profile.
- user (discord.user.User) : The user whose profile you want to check. Default - None

### /ranking

- Shows a server user rankings.

### /set-model {query}

- Change the currently set model.
- query (str) : Keyword of the model to be searched. Default - None

### /lora {query}

- Search for LoRAs on the server. (beta)
- query (str) : Keyword of the LoRA to be searched. Default - None

### /memory

- Shows the current RAM and VRAM usage of the server computer.

### /txt2img {prompt} {negative_prompt} {width} {height} {steps} {seed} {hires_toggle}

- Turns text into a picture.
- prompt (str) : A string that tells the AI what to draw.
- negative_prompt (str) : A string that tells the AI what not to do. Default - (low quality, worst quality:1.4), easynegative ,badhandv4, badv3, nsfw
- width (int)  : The width of the image. (width must be an integer between 64 and 1024.) Default - 384
- height (int) : The height of the image. (height must be an integer between 64 and 1024.) Default - 512
- steps (int) : The number of times the AI will draw repeatedly. (steps must be an integer between 1 and 50.) Default - 28
- seed (bool) : Sets the seed value for image generation. Default value - -1
- hires_toggle (bool) : Enables or disables hires_fix. Default - True