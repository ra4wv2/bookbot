# - *- coding: utf-8 - *-

from typing import Any
import telebot
import requests
import re
import os
import socket
import socks
import string
from telebot import types
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

#socks.set_default_proxy(socks.SOCKS5, "3.132.226.33")
#socket.socket = socks.socksocket

token = '1013007216:AAHS3qMb-o41MuMzv0Z8TzCJrIMef6mDtwU'

bot = telebot.TeleBot(token)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global book
    message = call.message
    if call.data == "hello":
        msg = bot.send_message(call.message.chat.id, 'Hi! I am a book bot that helps you find books to buy! Ok?')
        bot.register_next_step_handler(msg, which_website)
    if call.data == "help":
        msg = 'If you want to know more about me, press /help, and if you do not know what you want to read, check out recommendations, if you want to restart me, write /start. To start say hi!'
        bot.send_message(call.message.chat.id, msg)
    if call.data == "yes_o":
        msg = bot.send_message(call.message.chat.id, 'Please tell me the minimal and maximal price of your book (eg.: 300 500)')
        bot.register_next_step_handler(msg, price_range_ozon)
    if call.data == "yes_l":
        msg = bot.send_message(call.message.chat.id, 'Please tell me the minimal and maximal price of your book (eg.: 300 500)')
        bot.register_next_step_handler(msg, price_range_labirint)
    if call.data == "yes_b":
        msg = bot.send_message(call.message.chat.id, 'Please tell me the minimal and maximal price of your book (eg.: 300 500)')
        bot.register_next_step_handler(msg, price_range_bukvoed)
    if call.data == 'ozon':
        msg = bot.send_message(call.message.chat.id, 'Please write the name of the book and the author')
        bot.register_next_step_handler(msg, which_book_ozon)
    elif call.data == 'labirint':
        msg = bot.send_message(call.message.chat.id, 'Please write the name of the book and the author')
        bot.register_next_step_handler(msg, which_book_labirint)
    elif call.data == 'bukvoed':
        msg = bot.send_message(call.message.chat.id, 'Please write the name of the book and the author')
        bot.register_next_step_handler(msg, which_book_bukvoed)
    if call.data == "no_b":
        url = 'https://www.bookvoed.ru/books?q=' + book
        bot.send_message(call.message.chat.id, 'Here are all the books I have found for you: ' + url)
    if call.data == "no_l":
        url = 'https://www.labirint.ru/search/' + book + '/?stype=0'
        bot.send_message(call.message.chat.id, 'Here are all the books I have found for you: ' + url)
    if call.data == "no_o":
        url = 'https://www.ozon.ru/category/knigi-16500/?text=' + book
        url1 = 'https://www.ozon.ru/category/knigi-16500/?text=' + book + '&from_global=true'
        bot.send_message(call.message.chat.id, 'Here are all the books I have found for you: ' + url)
        bot.send_message(call.message.chat.id, 'Mobile version: ' + url1)
        
    if call.data == "horror":
        msg = "Here are some horror books you might enjoy:\n\n1.The Shining by Stephen King\n2.Dracula by Bram Stoker\n3.The Haunting of Hill House by Shirley Jackson\n4.Rosemary’s Baby by Ira Levin\n5.The Amityville Horror by Jay Anson"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "thriller":
        msg = "Here are some thrillers you might enjoy:\n\n 1.The Silence of the Lambs by Thomas Harris \n2.The Girl with the Dragon Tattoo by Stieg Larsson \n3.The Da Vinci Code by Dan Brown \n4. Kiss the Girls by James Patterson \n5.Gone Girl by Gillian Flynn"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "romance":
        msg = "Here are some romance books you might enjoy:\n\n 1.Pride and Prejudice by Jane Austen \n2.Outlander by Diana Gabaldon \n3.Jane Eyre by Charlotte Brontë \n4.Gone with the Wind by Margaret Mitchell \n5.A Knight in Shining Armor by Jude Deveraux"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "mystery":
        msg = "Here are some mystery books you might enjoy:\n\n 1.The Maltese Falcon, Dashiell Hammett \n2.And Then There Were None, Agatha Christie \n3.The Curious Incident of the Dog in the Night-Time, Mark Haddon \n4.Rebecca, Daphne du Maurier \n5.The Spy Who Came in From the Cold, John Le Carré"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "sci-fi":
        msg = "Here are some science fiction books you might enjoy:\n\n 1.The Hitchhiker’s Guide to the Galaxy, Douglas Adams \n2.Ender’s Game, Orson Scott Card \n3.Dune, Frank Herbert \n4.A Song of Ice and Fire, George R.R. Martin \n5.The Foundation Trilogy, Isaac Asimov"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "crime":
        msg = "Here are some crime books you might enjoy:\n\n 1.The Hound of the Baskervilles by Arthur Conan Doyle \n2.The Murder of Roger Ackroyd by Agatha Christie \n3.The Godfather by Mario Puzo \n4.The Lovely Bones By Alice Sebold \n5.The Big Sleep by Raymond Chandler"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "historical":
        msg = "Here are some historical dramas you might enjoy:\n\n 1.All the Light We Cannot See, Anthony Doerr \n2.The Color Purple, Alice Walker \n3.Shōgun, James Clavell \n4.War and Peace, Leo Tolstoy \n5.Sarah’s Key, Tatiana de Rosnay"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "fantasy":
        msg = "Here are some fantasy books you might enjoy:\n\n 1.The Lord of the Rings, J.R.R. Tolkien \n2.The Lion, the Witch and the Wardrobe by C. S. Lewis \n3.The Colour of Magic by Terry Pratchett \n4.Assassin’s Apprentice by Robin Hobb \n5.The Lies of Locke Lamora by Scott Lynch"
        bot.send_message(call.message.chat.id, msg)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('/help', 'recommendations')
    bot.send_message(message.chat.id,
                     '...',
                     reply_markup=keyboard1)
    keyboard = types.InlineKeyboardMarkup()
    if message.text == '/start':
        msg = bot.send_message(message.from_user.id, 'Hi! I am a book bot that helps you find books to buy! Ok?')
        bot.register_next_step_handler(msg, which_website)
    elif message.text.lower() == 'hi':
        keyboard = types.InlineKeyboardMarkup()
        key_hello = types.InlineKeyboardButton(text='start', callback_data='hello')
        keyboard.add(key_hello)
        key_help = types.InlineKeyboardButton(text='help', callback_data='help')
        keyboard.add(key_help)
        bot.send_message(message.from_user.id, text='Choose a button', reply_markup=keyboard)
        msg = bot.send_message(message.from_user.id, '🐶')
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'If you want to know more about me, press /help, and if you do not know what you want to read, check out recommendations, if you want to restart me, write /start. To start say hi!')
    elif message.text == 'recommendations':
        msg = bot.send_message(message.from_user.id, 'Please enjoy some of our book suggestions by genre! Send any message to continue')
        bot.register_next_step_handler(msg, recommendations)
    else:
        bot.send_message(message.from_user.id, 'I do not understand:( please try /help.')


global book

def recommendations(message):
    keyboard = types.InlineKeyboardMarkup()
    key_horror = types.InlineKeyboardButton(text='horror', callback_data='horror')
    keyboard.add(key_horror)
    key_thriller = types.InlineKeyboardButton(text='thriller', callback_data='thriller')
    keyboard.add(key_thriller)
    key_romance = types.InlineKeyboardButton(text='romance', callback_data='romance')
    keyboard.add(key_romance)
    key_crime = types.InlineKeyboardButton(text='crime', callback_data='crime')
    keyboard.add(key_crime)
    key_fantasy = types.InlineKeyboardButton(text='fantasy', callback_data='fantasy')
    keyboard.add(key_fantasy)
    key_science_fiction = types.InlineKeyboardButton(text='sci-fi', callback_data='sci-fi')
    keyboard.add(key_science_fiction)
    key_historical = types.InlineKeyboardButton(text='historical', callback_data='historical')
    keyboard.add(key_historical)
    key_mystery = types.InlineKeyboardButton(text='mystery', callback_data='mystery')
    keyboard.add(key_mystery)
    bot.send_message(message.from_user.id, text='Please choose a genre', reply_markup=keyboard)

def which_website(message):
    keyboard = types.InlineKeyboardMarkup()
    key_ozon = types.InlineKeyboardButton(text='Ozon', callback_data='ozon')
    keyboard.add(key_ozon)
    key_labirint = types.InlineKeyboardButton(text='Labirint', callback_data='labirint')
    keyboard.add(key_labirint)
    key_bukvoed = types.InlineKeyboardButton(text='Bukvoed', callback_data='bukvoed')
    keyboard.add(key_bukvoed)
    bot.send_message(message.from_user.id, text='Please choose the store where you want to shop', reply_markup=keyboard)



def which_book_ozon(message):
    global book
    book = message.text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    book = '+'.join(book)
    keyboard = types.InlineKeyboardMarkup()
    key_yes_o = types.InlineKeyboardButton(text='yes', callback_data='yes_o')
    keyboard.add(key_yes_o)
    key_no_o = types.InlineKeyboardButton(text='no', callback_data='no_o')
    keyboard.add(key_no_o)
    bot.send_message(message.from_user.id, text='Do you want to sort the books by price', reply_markup=keyboard)
    bot.send_message(message.from_user.id, '🐰')

def which_book_bukvoed(message):
    global book
    book = message.text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    book = '+'.join(book)
    keyboard = types.InlineKeyboardMarkup()
    key_yes_b = types.InlineKeyboardButton(text='yes', callback_data='yes_b')
    keyboard.add(key_yes_b)
    key_no_b = types.InlineKeyboardButton(text='no', callback_data='no_b')
    keyboard.add(key_no_b)
    bot.send_message(message.from_user.id, text='Do you want to sort the books by price', reply_markup=keyboard)
    bot.send_message(message.from_user.id, '🐰')


def which_book_labirint(message):
    global book
    book = message.text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    book = '%20'.join(book)
    keyboard = types.InlineKeyboardMarkup()
    key_yes_l = types.InlineKeyboardButton(text='yes', callback_data='yes_l')
    keyboard.add(key_yes_l)
    key_no_l = types.InlineKeyboardButton(text='no', callback_data='no_l')
    keyboard.add(key_no_l)
    bot.send_message(message.from_user.id, text='Do you want to sort the books by price', reply_markup=keyboard)
    bot.send_message(message.from_user.id, '🐰')


def price_range_labirint(message):
    price = message.text.translate(str.maketrans('', '', string.punctuation)).split()
    if price[0] < price[1]:
        url = 'https://www.labirint.ru/search/' + book + '/?order=relevance&way=back&stype=0&paperbooks=1&ebooks=1' \
                                                         '&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=' + \
              price[0] + '&price_max=' + price[1]
    else:
        url = 'https://www.labirint.ru/search/' + book + '/?order=relevance&way=back&stype=0&paperbooks=1&ebooks=1' \
                                                         '&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=' + \
              price[1] + '&price_max=' + price[0]
    bot.send_message(message.from_user.id, 'Here are the books I have picked for you (for mobiles: copy and paste it in your browser): ' + url)
    bot.send_message(message.from_user.id, 'If the results of your search do not include books that are available, '
                                           'try to make the maximal price higher')

def price_range_bukvoed(message):
    price = message.text.translate(str.maketrans('', '', string.punctuation)).split()
    if price[0] < price[1]:
        url = 'https://www.bookvoed.ru/books?q=' + book + '&ishop=true&pod=true&priceMin=' + price[0] + '&priceMax=' + \
              price[1]
    else:
        url = 'https://www.bookvoed.ru/books?q=' + book + '&ishop=true&pod=true&priceMin=' + price[1] + '&priceMax=' + \
              price[0]
    bot.send_message(message.from_user.id, 'Here are the books I have picked for you: ' + url)
    bot.send_message(message.from_user.id, 'If your search results are empty, it is possible that you have made a mistake in the name of the book or the price range you chose was too small. Please try to make the maximal price higher')


def price_range_ozon(message):
    price = message.text.translate(str.maketrans('', '', string.punctuation)).split()
    if price[0] < price[1]:
        url = 'https://www.ozon.ru/category/knigi-16500/' + '?price=' + price[0] + '.000%3B' + price[
            1] + '.000&' + 'text=' + book
    else:
        url = 'https://www.ozon.ru/category/knigi-16500/' + '?price=' + price[1] + '.000%3B' + price[
            0] + '.000&' + 'text=' + book
    bot.send_message(message.from_user.id, 'Here are the books I have picked for you(for mobiles: copy and paste it in your browser): ' + url)
    bot.send_message(message.from_user.id, 'If it seems like the results are not what you were looking for, yet they have a word in common with your search, try to make the price range bigger by making the maximal price higher')


def main():
    new_offset = 0
    print('launching...')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    
    bot.polling(none_stop=True, interval=0)