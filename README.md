<div align="center">
    <h1> | stable-diffusion-discord.py | </h1>
    <p>한국어 / <a href="https://github.com/quntnim/stable-diffusion-discord.py/blob/main/README-eng.md">ENG</a></p>
</div>

Stable Diffusion Web UI API를 이용하여 Stable Diffusion을 디스코드 봇으로 만들어 보는 프로젝트
## 기능 구현


| 기능 | 진행도 |
| --- | --- |
| txt2img | 60% |
| img2img | todo |
| extras | todo |
| png info | todo |
| options | 40% |
| controlnet | todo |

## 구현된 명령어

### /register

- 디스코드 봇에 내 정보를 등록합니다.

### /profile {user}

- 유저의 프로필을 보여 줍니다.
- user (discord.user.User) : 프로필을 확인할 유저입니다. 기본값 - None

### /set-model {query}

- 현재 설정되있는 모델을 바꿉니다.
- query (str) : 검색할 모델의 키워드 입니다. 기본값 - None

### /lora {query}

- 서버에 있는 로라를 검색합니다. (beta)
- query (str) : 검색할 로라의 키워드 입니다.

### /memory

- 현재 서버 컴퓨터의 RAM과 VRAM 사용량을 알려 줍니다.

### /txt2img {prompt} {negative_prompt} {width} {height} {steps} {seed} {hires_toggle}

- 텍스트를 그림으로 만들어 줍니다.
- prompt (str) : AI에게 그려야 할 것을 알려주는 문자열 입니다.
- negative_prompt (str) : AI에게 하지 말아야 할 것을 알려주는 문자열 입니다. 기본값 - (low quality, worst quality:1.4), easynegative ,badhandv4, badv3, nsfw
- width (int)  : 이미지의 너비 입니다. (width는 64에서 1024 사이의 정수여야 합니다.) 기본값 - 384
- height (int) : 이미지의 높이 입니다. (height는 64에서 1024 사이의 정수여야 합니다.) 기본값 - 512
- steps (int) : AI가 반복해서 그림을 그릴 횟수입니다. (steps는 1에서 50 사이의 정수여야 합니다.) 기본값 - 28
- seed (bool) : 이미지 생성의 시드값을 정합니다. 기본값 - -1
- hires_toggle (bool) : hires_fix의 여부를 정합니다. 기본값 - True