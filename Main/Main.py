import logging

import requests
from bs4 import BeautifulSoup

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


# main menu
def start(bot, update):
    update.message.reply_text("Wait a second..",
                              reply_markup=main_menu_keyboard())


def user_input(bot, update):
    update.message.reply_text()


def main_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text='Choose the option:',
                          reply_markup=main_menu_keyboard())


def main_menu_keyboard():
    menu_main = [[InlineKeyboardButton('멜론', callback_data='m1')],
                 [InlineKeyboardButton('지니', callback_data='m2')],
                 [InlineKeyboardButton('벅스', callback_data='m3')],
                 [InlineKeyboardButton('종료', callback_data='exit')]]
    return InlineKeyboardMarkup(menu_main)


# It cannot print all data if this program crawls rank data
# from website over top 50.
# all other menus
def menu_actions(bot, update):
    query = update.callback_query
    result = []

    if query.data == 'exit':
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='종료하였습니다.')
        return

    elif query.data == 'm1':
        # first submenu
        menu_1 = [[InlineKeyboardButton('실시간 차트 검색', callback_data='m1_1')],
                  # [InlineKeyboardButton('가수 이름 또는 곡명 검색', callback_data='m1_2')],
                  # [InlineKeyboardButton('가수별 곡 차트 검색', callback_data='m1_3')],
                  [InlineKeyboardButton('홈으로 돌아가기', callback_data='main')]]
        reply_markup = InlineKeyboardMarkup(menu_1)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='멜론에 오신 것을 환영합니다. 원하시는 메뉴를 선택하세요 :',
                              reply_markup=reply_markup)
    elif query.data == 'm2':
        # second submenu
        # first submenu
        menu_2 = [[InlineKeyboardButton('실시간 차트 검색', callback_data='m2_1')],
                  # [InlineKeyboardButton('가수 이름 또는 곡명 검색', callback_data='m2_2')],
                  # [InlineKeyboardButton('가수별 곡 차트 검색', callback_data='m2_3')],
                  [InlineKeyboardButton('홈으로 돌아가기', callback_data='main')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='지니에 오신 것을 환영합니다. 원하시는 메뉴를 선택하세요 :',
                              reply_markup=reply_markup)

    elif query.data == 'm3':
        menu_3 = [[InlineKeyboardButton('실시간 차트 검색', callback_data='m3_1')],
                  # [InlineKeyboardButton('가수 이름 또는 곡명 검색', callback_data='m3_2')],
                  # [InlineKeyboardButton('가수별 곡 차트 검색', callback_data='m3_3')],
                  [InlineKeyboardButton('홈으로 돌아가기', callback_data='main')]]
        reply_markup = InlineKeyboardMarkup(menu_3)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='벅스에 오신 것을 환영합니다. 원하시는 메뉴를 선택하세요 :',
                              reply_markup=reply_markup)

    # Melon Menu
    elif query.data == 'm1_1':
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        get_File = requests.get("https://www.melon.com/chart/index.htm", headers=headers)

        html = get_File.text
        bsObj = BeautifulSoup(html, "html.parser")

        charts = bsObj.findAll("div", {"class": "ellipsis rank01"})
        artists = bsObj.findAll("span", {"class": "checkEllipsis"})

        for i in range(len(charts)):
            if i < 50:
                chart = charts[i].text.strip()
                artist = artists[i].text.strip()

                result += ["{0:3d}위 {1} - {2}".format(i + 1, chart, artist)]

        temp = ''
        if len(result) > 0:
            for r in result:
                temp += r + "\n"
            bot.send_message(message_id=query.message.message_id,
                             chat_id=query.message.chat_id,
                             text=temp)
        # Back to Main Menu
        menu_1_1 = [[InlineKeyboardButton('Back', callback_data='m1')]]
        reply_markup = InlineKeyboardMarkup(menu_1_1)
        bot.send_message(chat_id=query.message.chat_id,
                         message_id=query.message.message_id,
                         text="Back to the Melon Menu",
                         reply_markup=reply_markup)

    # elif query.data == 'm1_2':
    #     # dp = updater.dispatcher
    #     # dp.add_handler(MessageHandler(Filters.text, user_input))
    #     # bot.edit_message_text(chat_id=query.message.chat_id,
    #     #                       message_id=query.message.message_id,
    #     #                       text="원하는 가수 또는 곡의 제목을 입력하세요 : {}".format(user_input))
    #     #
    #     # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    #     # get_File = requests.get("https://www.melon.com/chart/index.htm", headers=headers)
    #     #
    #     # html = get_File.text
    #     # bsObj = BeautifulSoup(html, "html.parser")
    #     #
    #     # charts = bsObj.findAll("div", {"class": "ellipsis rank01"})
    #     # artists = bsObj.findAll("span", {"class": "checkEllipsis"})
    #     #
    #     # temp = ''
    #     # for i in range(len(charts)):
    #     #     chart = charts[i].text.strip()
    #     #     artist = artists[i].text.strip()
    #     #
    #     #     if user_input in chart or user_input in artist:
    #     #         result += ["{0:3d}위 {1} - {2}".format(i + 1, chart, artist)]
    #     #
    #     # if len(result) > 0:
    #     #     for r in result:
    #     #         temp += r + "\n"
    #     #     bot.send_message(message_id=query.message.message_id,
    #     #                      chat_id=query.message.chat_id,
    #     #                      text=temp)
    #
    #     menu_1_2 = [[InlineKeyboardButton('Back', callback_data='m1')]]
    #     reply_markup = InlineKeyboardMarkup(menu_1_2)
    #     bot.edit_message_text(chat_id=query.message.chat_id,
    #                           message_id=query.message.message_id,
    #                           text="Back to the Melon Menu",
    #                           reply_markup=reply_markup)
    #
    # elif query.data == 'm1_3':
    #     menu_1_3 = [[InlineKeyboardButton('Back', callback_data='m1')]]
    #     reply_markup = InlineKeyboardMarkup(menu_1_3)
    #     bot.edit_message_text(chat_id=query.message.chat_id,
    #                           message_id=query.message.message_id,
    #                           text="Back to the Melon Menu",
    #                           reply_markup=reply_markup)

    # Genie Menu
    elif query.data == 'm2_1':
        result = []
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        get_file_dir = "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20190719&hh=21&rtm=Y&pg="
        get_file_dir_2 = "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20190719&hh=21&rtm=Y&pg=2"

        genie_temp = ''
        # It should have to write 1 to 5, Rank 1 to Rank 200, but datas overflow message,
        # and it cannot crawl Rank 1 to Rank 200 or Rank 1 to Rank 100,
        # So I changed the code that crawl data just 1 Page, Rank 1 to Rank 50
        for i in range(1, 2):
            link = '{}{}'.format(get_file_dir, i)
            # link2 = '{}'.format(get_file_dir_2)
            genie_property = requests.get(link, headers=header)
            # genie_property_2 = requests.get(link2, headers=header)
            html = genie_property.text
            # html2 = genie_property_2.text
            bsObj = BeautifulSoup(html, "html.parser")
            title_list = bsObj.findAll("a", {"class": "title ellipsis"})
            artist_list = bsObj.findAll("a", {"class": "artist ellipsis"})

            for j in range(len(title_list)):
                artist = artist_list[j + 5].text.strip()
                song = title_list[j].text.strip()
                result += ["{0:3d}위 {1} - {2}".format((i - 1) * 50 + j + 1, artist, song)]
                # print("{0:3d}위 {1} - {2}".format((i - 1) * 50 + j + 1, artist, song))
            if len(result) > 0:
                for r in result:
                    genie_temp += r + "\n"
                    # print(r)
                bot.send_message(message_id=query.message.message_id,
                                 chat_id=query.message.chat_id,
                                 text=genie_temp)

        # if len(result) > 0:
        #     for r in result:
        #         genie_temp2 += r + "\n"
        #     bot.send_message(message_id=query.message.message_id,
        #                      chat_id=query.message.chat_id,
        #                      text=genie_temp2)

        menu_2_1 = [[InlineKeyboardButton('Back', callback_data='m2')]]
        reply_markup = InlineKeyboardMarkup(menu_2_1)
        bot.send_message(chat_id=query.message.chat_id,
                         message_id=query.message.message_id,
                         text="Back to the Genie Menu",
                         reply_markup=reply_markup)

    # elif query.data == 'm2_2':
    #     menu_2_2 = [[InlineKeyboardButton('Back', callback_data='m2')]]
    #     reply_markup = InlineKeyboardMarkup(menu_2_2)
    #     bot.edit_message_text(chat_id=query.message.chat_id,
    #                           message_id=query.message.message_id,
    #                           text="Back to the Genie Menu",
    #                           reply_markup=reply_markup)
    #
    # elif query.data == 'm2_3':
    #     menu_2_3 = [[InlineKeyboardButton('Back', callback_data='m2')]]
    #     reply_markup = InlineKeyboardMarkup(menu_2_3)
    #     bot.edit_message_text(chat_id=query.message.chat_id,
    #                           message_id=query.message.message_id,
    #                           text="Back to the Genie Menu",
    #                           reply_markup=reply_markup)

    # Bugs Menu
    elif query.data == 'm3_1':
        result = []
        request = requests.get("https://music.bugs.co.kr/chart")
        html = request.text

        bsObj = BeautifulSoup(html, "html.parser")
        chart_list = bsObj.findAll("p", {"class": "title"})
        artist_list = bsObj.findAll("p", {"class": "artist"})

        # if len(chart_list) or len(artist_list) > 50:
        for i in range(len(chart_list)):
            if i < 50:
                artist = artist_list[i].text.strip().split("\n")[0]
                title = chart_list[i].text.strip()

                result += ["{0:3d}위 {1} - {2}".format(i + 1, artist, title)]

        bugs_temp = ''
        if len(result) > 0:
            for r in result:
                bugs_temp += r + "\n"
            bot.send_message(message_id=query.message.message_id,
                             chat_id=query.message.chat_id,
                             text=bugs_temp)

        menu_3_1 = [[InlineKeyboardButton('Back', callback_data='m3')]]
        reply_markup = InlineKeyboardMarkup(menu_3_1)
        bot.send_message(chat_id=query.message.chat_id,
                         message_id=query.message.message_id,
                         text="Back to the Bugs Menu",
                         reply_markup=reply_markup)

    # elif query.data == 'm3_2':
    #     menu_3_2 = [[InlineKeyboardButton('Back', callback_data='m3')]]
    #     reply_markup = InlineKeyboardMarkup(menu_3_2)
    #     bot.edit_message_text(chat_id=query.message.chat_id,
    #                           message_id=query.message.message_id,
    #                           text="Back to the Bugs Menu",
    #                           reply_markup=reply_markup)
    #
    # elif query.data == 'm3_3':
    #     menu_3_3 = [[InlineKeyboardButton('Back', callback_data='m3')]]
    #     reply_markup = InlineKeyboardMarkup(menu_3_3)
    #     bot.edit_message_text(chat_id=query.message.chat_id,
    #                           message_id=query.message.message_id,
    #                           text="Back to the Bugs Menu",
    #                           reply_markup=reply_markup)

    # and so on for every callback_data option


# handlers

updater = Updater("913334663:AAHZQR4hDRl43nqfuJW2vg7B8qCkwtQ9WnU")
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(menu_actions))
updater.start_polling()
