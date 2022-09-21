import json
import time
from binance.spot import Spot as Client
import Keys
from Strategies import *
from Keys import *
from Telegram import telegramBotSendText as telebot
from json_logic import jsonLogic

spotClient = Client(apiKey, secretKey)

# borsa verileri
def exchangeInfo(coinName: str = None):
    exchange = spotClient.exchange_info(symbol=str(coinName))
    return exchange


# mum verileri
def klineData(coinName: str, period: str, limit: int = None):
    mum = spotClient.klines(symbol=str(coinName), interval=str(period), limit=limit)
    return mum


# 24 saatlik değişimin verisi
def ticker24h(coinName: str):
    ticker = spotClient.ticker_24hr(symbol=str(coinName))
    return ticker


# coin fiyatını getirir
def price(coinName: str):
    return spotClient.ticker_price(symbol=str(coinName))["price"]

# timestamp
def serverTime():
    return spotClient.time()["serverTime"]


# emir defteri
def book(coinName: str, limit: int):
    return spotClient.depth(symbol=str(coinName), limit=limit)


def getAllSymbols():
    response = spotClient.exchange_info()
    return list(map(lambda symbol: symbol["symbol"], response["symbols"]))

#coinde virgülden sonra kaç basamak var gösterir
def lotSize(coinName: str):
    return exchangeInfo(coinName)["symbols"][0]["filters"][2]["minQty"]


def base(coinName: str):
    return exchangeInfo(coinName)["symbols"][0]["baseAsset"]

#virgülden sonra kaç basamak olduğunu hesaplar
def step(coinName: str):
    basamak = 0
    for i in lotSize(coinName):
        if i == str(0):
            basamak +=1
        elif i == str(1):
            break
    return basamak

usdtList = []
btcList = []
ethList = []
for coin in getAllSymbols():
    if "USDT" in coin and "UP" not in coin and "DOWN" not in coin and "ERDUSDT" not in coin and "BCCUSDT" not in coin: #and coin.startswith("USDT", 0,2) is True not in coin:
        usdtList.append(coin)
        for coin in usdtList:
            result = coin.startswith("USDT") or coin.startswith("BUSD") or coin.startswith("EUR") or coin.startswith("TUSD")
            if result is True:
                usdtList.remove(coin)
    elif "BTC" in coin:
        btcList.append(coin)
    elif "ETH" in coin:
        ethList.append(coin)

def symbolsData(coinName: str, period: str, limit: int):
    kline = klineData(coinName, period, limit)
    converted = pd.DataFrame(kline,
                             columns=["open-time", "open", "high", "low", "close", "volume", "close-time", "qav", "not",
                                      "tbbav", "tbqav", "ignore"], dtype=float)
    return converted


def dailyVolumeJson(coinName: str):
    volumeDaily = float(ticker24h(coinName)["quoteVolume"])
    j = json.dumps(volumeDaily)
    rules = {">": [
        {"var": "volumeDaily"},
        2000000
    ]}
    data = {"var": j}
    return jsonLogic(rules, data)

def scanner(coinList):
    result = []
    while True:
        try:
            for coin in coinList:
                data = symbolsData(coin, "4h", 500)
                close = data["close"]
                low = data["low"]
                high = data["high"]
                volume = data["volume"]
                js = data.to_json(orient='table')
                if volumeUpLogic(js) is True:
                    result.append(coin)
                    anlikFiyat = close[len(close) - 1]
                    telebot(f"🚀 {coin} paritesinde yükseliş dalgası tespiti!!\n₿ Anlık Fiyat = {anlikFiyat}\n"
                            , Keys.telegramGroupId)
                    result.clear()
                    break
        except:
            pass
        print("HEPSİ TARANDI ŞİMDİ BAŞTAN TARAYACAK")
        #telebot("---- Hepsi Tarandı ----", Keys.telegramGroupId)
        time.sleep(300)
#scanner(usdtList)



data = symbolsData("RLCUSDT", "4h", 5)
vol = data["volume"]
high = data["high"]
low = data["low"]
js = data.to_json(orient='table')
jsEnd = json.loads(js)

volumeUpLogic(jsEnd)





