import matplotlib.pyplot as plt
from selenium import webdriver
import csv
import pandas as pd
import time
from selenium.common import exceptions
import numpy as np
import seaborn as sns

driver = webdriver.Chrome()


def InitializeDataFrame():
    Initialize()
    PlayerInfoList = GetPlayersInfo()
    ColumnNames = GetColumnNames()
    df = pd.DataFrame(PlayerInfoList, columns=ColumnNames)
    df.to_csv('DataFrame.csv', index=False, sep=';')


def Initialize():
    driver.get("https://www.nba.com/stats/players/traditional/?sort=PTS&dir=-1%22")

    time.sleep(3)
    accept = driver.find_element_by_css_selector("#onetrust-accept-btn-handler")
    accept.click()


def GetPlayersInfo():
    time.sleep(5)
    PlayerList = []
    selector = f"body > main > div > div > div.row > div > div > nba-stat-table > div:nth-child(1) > div > div"
    code = driver.find_element_by_css_selector(selector)
    info = code.text
    player_amount = info[0] + info[1] + info[2]
    remainder = int(player_amount) // 50
    player_amount_last_page = int(player_amount) % 50
    page_amount = (remainder + 1, remainder)[player_amount_last_page == 0]

    for pageIndex in range(page_amount):
        RowsAmount = (50, player_amount_last_page)[pageIndex == page_amount - 1]
        for playerIndex in range(RowsAmount):
            PlayerInfo = GetSinglePlayer(playerIndex)
            if len(PlayerInfo) != 30:
                PlayerInfo[1] += " " + PlayerInfo[3]
                PlayerInfo.pop(3)
            PlayerList.append(PlayerInfo)
        if pageIndex != page_amount - 1:
            selector = "body > main > div > div > div.row > div > div > nba-stat-table > div:nth-child(1) > div > div > a.stats-table-pagination__next"
            NextPageButton = driver.find_element_by_css_selector(selector)
            NextPageButton.click()
            time.sleep(2)
    return PlayerList


def GetSinglePlayer(index):
    selector = f"body > main > div > div > div.row > div > div > nba-stat-table > div.nba-stat-table > div.nba-stat-table__overflow > table > tbody > tr:nth-child({index + 1})"
    CurrentPlayer = driver.find_element_by_css_selector(selector)
    CurrentPlayerInfo = CurrentPlayer.text
    ArraySize = len(CurrentPlayerInfo)
    PlayerInfo = []
    CurrentElement = ""
    for i in range(ArraySize):
        if CurrentPlayerInfo[i] != " " and CurrentPlayerInfo[i] != "\n":
            CurrentElement += CurrentPlayerInfo[i]
        else:
            if len(CurrentElement) > 0:
                PlayerInfo.append(CurrentElement)
            CurrentElement = ""
    return PlayerInfo


def GetColumnNames():
    ColumnNames = ['Rank', 'FirstName', 'LastName']
    for i in range(2, 29):
        selector = f"body > main > div > div > div.row > div > div > nba-stat-table > div.nba-stat-table > div.nba-stat-table__overflow > table > thead > tr > th:nth-child({i + 1})"
        columnnames = driver.find_element_by_css_selector(selector)
        ColumnNames.append(columnnames.text)
    return ColumnNames


InitializeDataFrame()
