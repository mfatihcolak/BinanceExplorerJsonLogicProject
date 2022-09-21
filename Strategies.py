import json
import math
import pandas as pd
import pandas_ta as ta
import numpy as np
from pandas_ta import df
from json_logic import jsonLogic
from jsonschema import validate


def crossover(a : list, b : list):
    kisa = a[len(a) - 2]
    simdikiKisa = a[len(a) - 1]

    uzun = b[len(b) - 2]
    simdikiUzun = b[len(b) - 1]

    if kisa < uzun and simdikiKisa > simdikiUzun:
        return True
    else:
        return False


def volumeUpLogic(data):
    #rules = {"+": [{'var': ["data.-2.volume"]}, {'var': ["data.-3.volume"]}, {'var': ["data.-4.volume"]}]}
    #rules = {"/":[{"+":[{'var':["data.-2.volume"]}, {'var':["data.-3.volume"]}, {'var':["data.-4.volume"]}]},3]}
    rules = {">": [{'var': ["data.-1.volume"]}, {"/": [{"+": [{'var': ["data.-2.volume"]}, {'var': ["data.-3.volume"]}, {'var': ["data.-4.volume"]}]}, 3]}]}
    print("data1 :", data)
    ruledata1 = {'var':["data.-1.volume"]}
    ruledata2 = {'var': ["data.-2.volume"]}
    ruledata3 = {'var': ["data.-3.volume"]}
    ruledata4 = {'var': ["data.-4.volume"]}

    print("rules :",rules)
    #data={"schema":{"fields":[{"name":"index","type":"integer"},{"name":"open-time","type":"number"}]}}
    #print("data2 :" , data)
    print("data1 :", jsonLogic(ruledata1, data))
    print("data2 :", jsonLogic(ruledata2, data))
    print("data3 :", jsonLogic(ruledata3, data))
    print("data4 :", jsonLogic(ruledata4, data))
    print("result :",jsonLogic(rules, data))



def fisherTransformStrategy(high, low):
    length = 10
    fishLine = ta.fisher(high, low, length)["FISHERT_10_1"]
    signalLine = ta.fisher(high, low, length)["FISHERTs_10_1"]

    if crossover(fishLine, signalLine) is True:
        return True

def fisherTransformJson(high,low):
    length = 10
    fishLine = ta.fisher(high, low, length)["FISHERT_10_1"]
    fishDump = json.dumps(fishLine)
    signalLine = ta.fisher(high, low, length)["FISHERTs_10_1"]
    signalDump = json.dumps(signalLine)
    #if kisa < uzun and simdikiKisa > simdikiUzun:

    rules = {"and":[
        {"<":[
            {"var":"shortLine"},
            {"var":"longLine"}
        ]},
        {">":[
            {"var":"shortNow"},
            {"var":"longNow"}
        ]}
    ]}
    data = {
        {"var":fishDump},
        {"var":signalDump}
    }
    return fishLine

def waveTrend(high,low,close):
    n1 = 10
    n2 = 21
    obLevelone = 60
    obLeveltwo = 53
    osLevelone = -60
    osLeveltwo = -53

    ap = ta.hlc3(high=high, low=low, close=close)
    esa = ta.ema(ap, n1)
    d = ta.ema(abs(ap-esa), n1)
    ci = (ap-esa) / (0.015 * d)
    tci = ta.ema(ci, n2)

    wt1 = tci
    wt2 = ta.sma(ci, 4)

    if wt1[len(wt1)-1] < 0:
        return True
    elif wt1[len(wt1)-1] > 0:
        return False





