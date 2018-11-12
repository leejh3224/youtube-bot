from Bot import Bot

# your location to chromedriver executable
bot = Bot('/Users/**/Downloads/chromedriver')

bot.goto_youtube() \
    .login(email='your@email', password='password') \
    .subscribe(channelId='uisdg22g') \
    .end()