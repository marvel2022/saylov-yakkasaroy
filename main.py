"""
Created on Tue July 31 2021

bot link: http://t.me/yakkasaroy_saylov_bot 

@author: jamshid
"""
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup,  Location, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          ConversationHandler,  MessageHandler, Filters)

from const import TOKEN, DB_NAME, VOTERS_DB_NAME
from db_helper import StationsDBHelper, VotersDBHelper
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATE_LANGUAGE = 1
STATE_MENU = 2
STATE_LIST_STATIONS = 3
STATE_STATION = 4
STATE_PASPORT_DATA=5


# ADDRESS BOT
BOT_ADDRESS = '@yakkasaroy_saylov_bot'
WEBSITE_ADDRESS = 'yakkasaroysaylov.uz'

# Languages
UZ = 'uz'
RU = 'ru'

# Callback datas
SHTAB = 'shtab'
STATION = 'station'
PASPORT = 'pasport'
CHANGE_LANGUAGE = 'language'
BACK = 'back'
GO_HOME = 'go_home'


TEXT_BTN_SHTAB = {
    UZ: '🏢Saylov shtabi',
    RU: '🏢Избирательный штаб'
}
TEXT_BTN_STATIONS = {
    UZ: '🏫Saylov uchastkalari',
    RU: '🏫Избирательные участки'
}
TEXT_BTN_CHECK_STATION = {
    UZ: '❓Saylov uchastkasini aniqlash',
    RU: '❓Определение избирательного участка'
}
TEXT_BTN_CHANGE_LANGUAGE = {
    UZ: '🌐Tilni o\'zgartirish',
    RU: '🌐Изменить язык'
}
TEXT_BTN_BACK = {
    UZ: '⬅️Orqaga',
    RU: '⬅️Назад'
}
TEXT_BTN_GO_TO_HOME = {
    UZ: '🏛Bosh sahifa',
    RU: '🏛Главная страница'
}
TEXT_TITLE_ELECTION_NAME = {
    UZ: "<b>O'zbekiston Respublikasi Prezidenti Saylovi - 2021</b>",
    RU: "<b>Выборы Президента Республики Узбекистан - 2021</b>"
}
TEXT_TITLE_CHOOSE_LANGUAGE = 'Iltimos, tilni tanlang / Пожалуйста, выберите язык ⬇️'
TEXT_TITLE_MENU = {
    UZ: "<b>\"Yakkasaroy Saylov\"</b> rasmiy botiga xush kelibsiz!\n\n" + TEXT_TITLE_ELECTION_NAME[UZ],
    RU: "Добро пожаловать в официальный бот <b>\"Yakkasaroy Saylov\"</b>\n\n" +
        TEXT_TITLE_ELECTION_NAME[RU]
}
TEXT_TITLE_CHOOSE_STATION = {
    UZ: 'Saylov uchastkasini tanlang: ⬇️',
    RU: 'Выберите избирательный участок: ⬇️'
}
TEXT_TITLE_STATION_NUMBER = {
    UZ: '<b>{} - SAYLOV UCHASTKASI</b>',
    RU: '<b>ИЗБИРАТЕЛЬНЫЙ УЧАСТОК №{}</b>'
}
TEXT_LOCATION_CAPTION = {
    UZ: '📍Saylov uchastkasi joylashuvi',
    RU: '📍Расположение избирательного участка'
}
TEXT_STATION_NUMBER = {
    UZ: '<b>Saylov uchastkasi raqami:</b>',
    RU: '<b>Номер избирательного участка:</b>'
}
TEXT_STATION_SECTOR = {
    UZ: '<b>Sektor:</b>',
    RU: '<b>Сектор:</b>'
}
TEXT_STATION_VOTERS = {
    UZ: '<b>Saylovchilar soni:</b>',
    RU: '<b>Количество проголосовавших:</b>'
}
TEXT_STATION_WEB = {
    UZ: '<b>Veb sayt:</b>',
    RU: '<b>Веб-сайт</b>'
}
TEXT_STATION_MFY = {
    UZ: '<b>Saylov uchastkasi hududidagi MFY:</b>',
    RU: '<b>СГМ на территории избирательного участка:</b>'
}
TEXT_STATION_BUILDING = {
    UZ: '<b>Saylov uchastkasi joylashgan bino:</b>',
    RU: '<b>Здание, в котором находится избирательный участок:</b>'
}
TEXT_STATION_BUILDING_ADDRESS = {
    UZ: '<b>Binoning yuridik manzili:</b>',
    RU: '<b>Юридический адрес здания:</b>'
}
TEXT_STATION_CADASTRE = {
    UZ: '<b>Binoning kadastr raqami:</b>',
    RU: '<b>Кадастровый номер здания:</b>'
}
TEXT_STATION_HEAD = {
    UZ: '<b>Saylov uchastkasi raisi:</b>',
    RU: '<b>Председатель избирательного участка:</b>'
}
TEXT_STATION_ASSISTANT = {
    UZ: "<b>Saylov uchastkasi rais o'rinbosari:</b>",
    RU: '<b></b>'
}
TEXT_STATION_SECRETARY = {
    UZ: "<b>Saylov uchastkasi rais kotibi:</b>",
    RU: '<b></b>'
}
TEXT_STATION_HEAD = {
    UZ: '<b>Saylov uchastkasi raisi:</b>',
    RU: '<b>Председатель избирательного участка:</b>'
}
TEXT_STATION_HEAD_PHONE = {
    UZ: '<b>Telefon raqami:</b>',
    RU: '<b>Номер телефона:</b>'
}
TEXT_POSITION={
    UZ: "<b>Lavozimi</b>",
    RU: "<b>Позиция</b>"
}
TEXT_PASPORT_DATA={
    UZ:"<b>Pasportingizni seriyasi va raqamini yuboring (AA0000000)</b>",
    RU:"<b>Отправьте серию и номер паспорта (AA0000000)</b>",
}
NOT_FOUND={
    UZ:"Topilmadi 😕 (404)",
    RU:"Не найден 😕 (404)",
}

user_language = dict()
db=StationsDBHelper(DB_NAME)
db_voter=VotersDBHelper(VOTERS_DB_NAME)


# return menu button for  selecet section 
# (statons list, search for station, change language)
def get_menu_buttons(lang):
    menu_buttons = [
        [
            InlineKeyboardButton(
                TEXT_BTN_STATIONS[lang], callback_data=STATION)
        ],
        [
            InlineKeyboardButton(
                TEXT_BTN_CHECK_STATION[lang], callback_data=PASPORT)
        ],
        [
            InlineKeyboardButton(
                TEXT_BTN_CHANGE_LANGUAGE[lang], callback_data=CHANGE_LANGUAGE)
        ]
    ]
    return menu_buttons


# return stations' id numbers as inline button
def stations_button_list():
    stations = db.get_stations()
    buttons = []
    line = []

    for station in stations:
        line.append(InlineKeyboardButton(str(station['number']), callback_data=station['id']))
        if len(line) == 3:
            buttons.append(line)
            line = []
    if len(line)>0:
        buttons.append(line)

    return buttons


# return station that queried by id
def get_station_by_id(id):
    station = db.get_station_by_id(id)
    return station

# return voter from db by pasport
def check_voter_by_pasport(pasport_data):
    return db_voter.get_voter_by_pasport(pasport_data)
    
# entry point function
def start(update, context):
    user = update.message.from_user
    user_language[user.id] = UZ
    languageButtons = [
        [
            InlineKeyboardButton("🇺🇿O'zbek", callback_data=UZ),
            InlineKeyboardButton("🇷🇺Русский", callback_data=RU)
        ]
    ]
    update.message.reply_text(
        TEXT_TITLE_CHOOSE_LANGUAGE,
        reply_markup=InlineKeyboardMarkup(languageButtons)
    )

    return STATE_LANGUAGE

# STATE_LANGUAGE callback function
def language_callback(update, context):
    query = update.callback_query

    user_language[query.from_user.id] = query.data

    query.edit_message_text(
        text=TEXT_TITLE_MENU[query.data],
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(get_menu_buttons(query.data))
    )

    return STATE_MENU


# STATE_MENU callback function
def menu_callback(update, context):
    query = update.callback_query

    if query.data == STATION:
        return station_list(update, context)
    elif query.data == PASPORT:
        return pasport_data(update, context)
    elif query.data == CHANGE_LANGUAGE:
        return change_language(query)


# displaies a list of avoilabe stations
def station_list(update, context):
    query = update.callback_query

    lang = user_language[query.from_user.id]

    buttons = stations_button_list()
    buttons.append([InlineKeyboardButton(TEXT_BTN_BACK[lang], callback_data=BACK)])

    query.edit_message_text(
        text=TEXT_TITLE_CHOOSE_STATION[lang],
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons))
    return STATE_LIST_STATIONS


def pasport_data(update, context):
    query=update.callback_query
    lang=user_language[query.from_user.id]

    query.edit_message_text(
        text=TEXT_PASPORT_DATA[lang],
        parse_mode='HTML',
    )
    example_photo_path = f"images/ex_pasport-{lang}.jpg"
    example_photo = open(example_photo_path, 'rb')
    query.message.reply_photo(
        photo=example_photo,
        caption="Namuna / пример",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(
            [
                [
                    # TEXT_BTN_BACK[lang], 
                    TEXT_BTN_GO_TO_HOME[lang]
                ]
            ], 
            resize_keyboard=True
        )
    )
    # return check_voter_pasword(update, context)
    return STATE_STATION


def full_name(voter):
    fish=''
    f_name=None
    s_name=None
    th_name=None
    try:
        f_name=voter['f_name']
    except:
        pass
    try:
        s_name=voter['s_name']
    except:
        pass
    try:
        th_name=voter['th_name']
    except:
        pass
    if f_name:
        fish+=f_name
    if s_name:
        fish=fish+" "+s_name
    if th_name:
        fish=fish+" "+th_name
    return fish


# STATE_PASPORT_DATA callback function
def check_voter_pasword(update, context):
    # query=update.callback_query
    lang = user_language[update.message.from_user.id]
    # lang=UZ

    voter=check_voter_by_pasport(update.message.text)
    print(voter)
    if voter:
        url_website = str(voter['station'])+'.'+WEBSITE_ADDRESS

        station_message = "<b>FISH</b>: {} \n\n<b>Do'imiy yashash manzili:</b> {} \n\n<b>Saylov uchastkasi:</b> {} \n\n<b>Web sayt:</b> {}".format(
            full_name(voter), voter['address'], voter['station'], url_website
        )
        # update.message.reply_html()
    else:
        station_message=NOT_FOUND[lang]
    update.message.reply_text(
        text=station_message,
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(
            [
                [
                    # TEXT_BTN_BACK[lang], 
                    TEXT_BTN_GO_TO_HOME[lang]
                ]
            ], 
            resize_keyboard=True
        )
    )
    
    return STATE_STATION



def change_language(query):
    languageButtons = [
        [
            InlineKeyboardButton("🇺🇿O'zbek", callback_data=UZ),
            InlineKeyboardButton("🇷🇺Русский", callback_data=RU)
        ]
    ]
    query.edit_message_text(
        text=TEXT_TITLE_CHOOSE_LANGUAGE,
        reply_markup=InlineKeyboardMarkup(languageButtons)
    )

    return STATE_LANGUAGE


# STATE_LIST_STATIONS callback function
def station_list_callback(update, context):
    query = update.callback_query

    lang = user_language[query.from_user.id]

    if query.data == BACK:
        query.edit_message_text(
            text=TEXT_TITLE_MENU[lang],
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(get_menu_buttons(lang))
        )
        return STATE_MENU
    else:
        station = get_station_by_id(int(query.data))
        query.message.delete()

        if lang == UZ:
            name_mfy='name_mfy'
            building='building'
            building_address='building_address'
            
            chairman='chairman'
            position_ch='position_ch'

            assistant='assistant'
            position_a='position_a'

            secretary='secretary'
            position_s='position_s'
        else:
            name_mfy = 'name_mfy_ru'
            building = 'building_ru'
            building_address = 'building_address_ru'
            chairman = 'chairman'


        # STATION NUMBER
        message = TEXT_TITLE_STATION_NUMBER[lang].format(station['number'])
        query.message.reply_html(message)

        # STATION_MESSAGE
        url_website = str(station['number'])+'.'+WEBSITE_ADDRESS

        station_message = "{} {} \n\n{} {} \n\n{} {} \n\n{} {} \n\n{} {} \n\n{} {} \n\n{} {} \n\n{} {} \n\n{}".format(
            TEXT_STATION_NUMBER[lang], station['number'],
            TEXT_STATION_SECTOR[lang], station['sector'],
            TEXT_STATION_VOTERS[lang], station['number_voters'],
            TEXT_STATION_WEB[lang],    url_website,
            TEXT_STATION_MFY[lang],    station[name_mfy],
            TEXT_STATION_BUILDING[lang], station[building],
            TEXT_STATION_BUILDING_ADDRESS[lang], station[building_address],
            TEXT_STATION_CADASTRE[lang], station['cadastre'],
            BOT_ADDRESS
        )
        x=[]
        try:
            station_photo_path=f"images/stations/{station['number']}/G1.jpg"
            station_photo=open(station_photo_path, 'rb')
        except:
            station_photo=open('images/stations/station.jpg', 'rb')
        query.message.reply_photo(
            photo=station_photo,
            caption=station_message,
            parse_mode="HTML"
        )

        # CHAIRMAN MESSAGE
        # phone = re.sub("[^+0-9]", "", station['phone_ch'])
        chairman_message = "{}\n{} \n\n{}\n{} \n\n{}\n{} \n\n{}".format(
            TEXT_STATION_HEAD[lang], station[chairman],
            TEXT_POSITION[lang], station[position_ch],
            TEXT_STATION_HEAD_PHONE[lang], station['phone_ch'],
            BOT_ADDRESS
        )

        try:
            chairman_photo_path = 'images/chairmen/{}/{}a.jpg'.format(str(station['number']), station['number'])
            print(chairman_photo_path)
            chairman_photo = open(chairman_photo_path, 'rb')
        except:
            chairman_photo = open('images/chairmen/chairman.jpg', 'rb')

        query.message.reply_photo(
            photo=chairman_photo,
            caption=chairman_message,
            parse_mode="HTML",
        )

        # ASSISTANT MESSAGE
        # phone = re.sub("[^+0-9]", "", station['phone_ch'])
        assistant_message = "{}\n{} \n\n{}\n{} \n\n{}\n{} \n\n{}".format(
            TEXT_STATION_ASSISTANT[lang], station[assistant],
            TEXT_POSITION[lang], station[position_a],
            TEXT_STATION_HEAD_PHONE[lang], station['phone_a'],
            BOT_ADDRESS
        )

        try:
            assistant_photo_path = 'images/chairmen/{}/{}b.jpg'.format(str(station['number']), station['number'])
            print(assistant_photo_path)
            assistant_photo = open(assistant_photo_path, 'rb')
        except:
            assistant_photo = open('images/chairmen/chairman.jpg', 'rb')

        query.message.reply_photo(
            photo=assistant_photo,
            caption=assistant_message,
            parse_mode="HTML",
        )

        # SECRETARY MESSAGE
        # phone = re.sub("[^+0-9]", "", station['phone_ch'])
        secretary_message = "{}\n{} \n\n{}\n{} \n\n{}\n{} \n\n{}".format(
            TEXT_STATION_SECRETARY[lang], station[secretary],
            TEXT_POSITION[lang], station[position_s],
            TEXT_STATION_HEAD_PHONE[lang], station['phone_s'],
            BOT_ADDRESS
        )

        try:
            secretary_photo_path = 'images/chairmen/{}/{}c.jpg'.format(str(station['number']), station['number'])
            print(secretary_photo_path)
            secretary_photo = open(secretary_photo_path, 'rb')
        except:
            secretary_photo = open('images/chairmen/chairman.jpg', 'rb')

        query.message.reply_photo(
            photo=secretary_photo,
            caption=secretary_message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup(
                    [[TEXT_BTN_BACK[lang], TEXT_BTN_GO_TO_HOME[lang]]], 
                    resize_keyboard=True
                )
        )

        # LOCATION
        try:
            title_location = query.message.reply_html(
                TEXT_LOCATION_CAPTION[lang]
            )
            query.message.reply_location(
                latitude=station['latitude'],
                longitude=station['longitude']
            )
        except:
            title_location.delete()
        
        return STATE_STATION


def go_back_station_list(update, context):
    user_id = update.message.from_user.id
    lang = user_language[user_id]

    buttons = stations_button_list()
    buttons.append([InlineKeyboardButton(
        TEXT_BTN_BACK[lang], callback_data=BACK)])

    mes = update.message.reply_text(
        'Foydalanishda davom eting',
        reply_markup=ReplyKeyboardRemove(),

    )
    mes.delete()
    update.message.reply_html(
        TEXT_TITLE_CHOOSE_STATION[lang],
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return STATE_LIST_STATIONS


def go_back_menu(update, context):
    user_id = update.message.from_user.id
    lang = user_language[user_id]

    mes = update.message.reply_text(
        'Foydalanishda davom eting',
        reply_markup=ReplyKeyboardRemove()
    )
    mes.delete()

    update.message.reply_html(
        TEXT_TITLE_MENU[lang],
        reply_markup=InlineKeyboardMarkup(get_menu_buttons(lang))
    )

    return STATE_MENU

def main():
    # Updater
    updater = Updater(TOKEN, use_context=True)

    # Dispatcher
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE_LANGUAGE: [
                CallbackQueryHandler(language_callback)
            ],
            STATE_MENU: [
                CallbackQueryHandler(menu_callback)
            ],
            STATE_LIST_STATIONS: [
                CallbackQueryHandler(station_list_callback)
            ],
            STATE_STATION: [
                MessageHandler(Filters.regex(
                    '^(' + TEXT_BTN_BACK[UZ] + '|' + TEXT_BTN_BACK[RU] + ')$'), go_back_station_list),
                MessageHandler(Filters.regex(
                    '^(' + TEXT_BTN_GO_TO_HOME[UZ] + '|' + TEXT_BTN_GO_TO_HOME[RU] + ')$'), go_back_menu),
                MessageHandler(Filters.text & ~Filters.command & ~Filters.video & ~Filters.photo, check_voter_pasword)
            ],
            STATE_PASPORT_DATA: [
                CallbackQueryHandler(check_voter_pasword)
            ],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()


main()

#              MessageHandler(Filters.regex(
#                 '^(' + TEXT_BTN_GO_TO_HOME[UZ] + '|' + TEXT_BTN_GO_TO_HOME[RU] + ')$'), go_back_menu)


"""
number
sector
number_voters
name_mfy
building
building_address
cadastre
chairman
phone_ch
position_ch
assistant
phone_a
position_a
secretary
phone_s
position_s
latitude
longitude

"""