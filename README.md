# teabot
A slack bot who also likes (ordering) boba tea just like you!

![teabot_preview](https://user-images.githubusercontent.com/17972401/62922089-6a089180-bd5f-11e9-9afe-8bff7420687b.png)

Icon used in the preview above is made by [Freepik](https://www.flaticon.com/authors/freepik) from www.flaticon.com under [Flaticon Basic License](https://file000.flaticon.com/downloads/license/license.pdf).

## Installation
```bash
mkvirtualenv oit --python=python3.7 # if virtual environment has not been created
workon oit --python=python3.7 # if virtual environment has created
pip install -r requirements.txt
```

In order to use this bot (in your workspace for development purpose), please follow the steps [here](https://github.com/slackapi/pycon/blob/master/README.rst) in order to set up the Slack app.

## Development Guidance

For local testing: 

1. Set up __ngrok__ for local testing following installation guidance [here](https://ngrok.com/) and run `ngrok http 3000`. 

2. Have the app running with `python app.py`.
