# stable-diffusion-discord.py
KOR / ENG(soon)

Stable Diffusion Web UI API를 이용하여 Stable Diffusion을 디스코드 봇으로 만들어 보는 프로젝트
## 기능 구현


| 기능 | 진행도 |
| --- | --- |
| txt2img | 40% |
| img2img | todo |
| extras | todo |
| png info | todo |
| options | 30% |
| controlnet | todo |

## 구현된 명령어

### /get-options

- 현재 설정되있는 모델과 vae를 알려 줍니다.

### /set-model

- 현재 설정되있는 모델을 바꿉니다.

### /txt2img {prompt} {negative_prompt} {width} {height} {steps} {hires_toggle}

- 텍스트를 그림으로 만들어 줍니다.
- prompt (str) : AI에게 그려야 할 것을 알려주는 문자열 입니다.
- negative_prompt (str) : AI에게 하지 말아야 할 것을 알려주는 문자열 입니다. 기본값 - (low quality, worst quality:1.4), easynegative ,badhandv4, badv3, nsfw
- width (int)  : 이미지의 너비 입니다. (width는 64에서 1024 사이의 정수여야 합니다.) 기본값 - 384
- height (int) : 이미지의 높이 입니다. (height는 64에서 1024 사이의 정수여야 합니다.) 기본값 - 512
- steps (int) : AI가 반복해서 그림을 그릴 횟수입니다 (steps는 1에서 50 사이의 정수여야 합니다.) 기본값 - 28
- hires_toggle (bool) : hires_fix의 여부를 정합니다. 기본값 - True
