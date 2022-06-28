import telebot
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

token = "put Telegram bot token here."

quotes = []

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'https://parade.com/968666/parade/chuck-norris-jokes/'
        yield scrapy.Request(url=url, callback=self.handle_page, meta={'COOKIES_ENABLED': False})

    def handle_page(self, response):
        lines = response.xpath('//ol/li')
        for line in lines:
            line_text = line.get()
            soup = BeautifulSoup(line_text, 'html.parser')
            quotes.append(soup.text)
        raise scrapy.exceptions.CloseSpider('bandwidth_exceeded')


def get_qoutes():
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()


def run_bot():
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Welcome to chuck norris bot!\n Enter a number from 1 to 101.")
        print("started!")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.reply_to(message, " Very easy: enter a number from 1 to 101.")


    @bot.message_handler(func=lambda m: True)
    def return_qoute(message):
        try:
            index = int(message.text) - 1
            if index < 0 or index > 100:
                bot.reply_to(message, "Invalid input! Enter a number from 1 to 101.")
            else:
                bot.reply_to(message, quotes[index])
        except:
            bot.reply_to(message, "Invalid input! Enter a number from 1 to 101.")

    bot.infinity_polling()



if __name__ == '__main__':
    get_qoutes()
    assert(len(quotes) == 101)
    run_bot()

