# A bot that can subscribe subreddits and post them to a channel

## Quick start

Clone this repository:

```bash
git clone https://github.com/iamnmt/reddit-discord-bot.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Setup environment variables in `.env` file:

```bash
DISCORD_TOKEN="<YOUR_DISCORD_TOKEN>"
REDDIT_CLIENT_ID="<YOUR_REDDIT_CLIENT_ID>"
REDDIT_PRIVATE_KEY="<YOUR_REDDIT_PRIVATE_KEY>"
```

Invite the bot to your server.

Run the bot:

```bash
python bot.py
```

## Deployment

There is a `Procfile` included for deploying to Heroku. 

## Development
### Auto restart on save

By using `nodemon` and `pipenv` you can restart your bot when there are changes:

```bash
nodemon --exec pipenv run python bot.py
```

### Testing

Write commands you want to run to `.txt` file in `/test` folder. For example, in `test_help.txt`:

```
help
help sub
...
```

Run a testing script for the bot:

```
python test.py
```

In the Discord channel, enter the message:

```
!test
```

for testing commands in all `.txt` files. Or:

```
!test test_help test_sub ...
```

for specific files (`.txt` extention is excluded).

## To-do List

- [ ] Include upvotes and downvotes of a post.
- [ ] Fetch video and text post.
- [ ] Watch comments from a post.
- [ ] Follow a redditor
- [ ] More options for scheduling command.
