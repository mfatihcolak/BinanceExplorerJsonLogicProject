import requests
import Keys


def telegramBotSendText(botMessage,id):
    botToken = Keys.telegramToken
    botChatId = id
    sendText = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + botChatId + "&parse_mode" \
                                                                                                 "=Markdown&text=" \
                                                                                              + botMessage
    response = requests.get(sendText)
    return response.json()

