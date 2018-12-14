# Youtube bot

## Getting Started

1. This program uses `chromedriver`. So you must install it via [link](https://sites.google.com/a/chromium.org/chromedriver/downloads).
2. Clone the repository.

```bash
git clone https://github.com/leejh3224/youtube-bot.git && cd youtube-bot
```

3. Create `main.py` inside root directory.
   (You can copy `example-subscribe.py`)

```bash
touch main.py or
cp example-subscribe.py main.py
```

4. If you want to use `like` method, you should change the logic inside.
   If statement is based on comparing text label to identify whether the button is `like` button or not.
   So feel free to change '좋아함' into your local langauge.

```python
if label and ('좋아함' in label) and not liked:
    button.click()
    break
```

5. execute `main.py`.

```python
python3 main.py
```

## features:

-   login to google (implemented)
-   subscribe a channel (implemented)
-   like a video (implemented)

> If you have any issue or code suggestion, please make an issue or pull request.
