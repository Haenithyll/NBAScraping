import csv
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('DataFrame.csv', sep=';')
currentSelection = []

array_Dataframe = genfromtxt('DataFrame.csv', delimiter=';', dtype=None, encoding='utf8')
sns.set_theme(style="ticks")


def XColumnDisplay(array, X):
    for i in range((len(array) // X)):
        output = []
        for j in range(X):
            if X * i + j < len(array):
                output.append(array[X * i + j])

        print(output)


def ListAllTeams():
    teamNames = []
    for row in array_Dataframe:
        isInList = False
        for name in teamNames:
            if row[3] == name:
                isInList = True
        if (not isInList) and len(row[3]) == 3:
            teamNames.append(row[3])
    teamNames
    return teamNames


def ListParameters():
    elements = []
    for element in array_Dataframe[0]:
        elements.append(element)
    return elements


def TeamSelector():
    teams = []
    print(
        "\n(press enter after each team name, \nand once more to finish selection)\nTeam names (3 letters) to add to Selection filter : ")
    inputTxt = input()

    while len(inputTxt) > 0:
        teams.append(inputTxt)
        inputTxt = input()

    return teams


def PlayerSelector():
    print("Please input two player's Last Names (beware of typos!) to compare their stats :")
    players = [input("Player 1 : "), input("Player 2 : ")]

    return players


def CustomPlotSelector():
    XColumnDisplay(ListParameters(), 5)
    print("Here are all the parameters, which two (beware of typos!) do you want to compare ? ")
    paramSelect = [(input("Parameter 1 : "))]
    print("vs")
    paramSelect.append((input("Parameter 2 : ")))
    return paramSelect


def InitialDecision():
    print("Welcome to the NBA Player-Stat viewer. \n\n")
    answer = ""
    while answer != "P" and answer != "p" and answer != "T" and answer != "t":
        answer = input("What do you want to view? \n - Two-(P)layer Comparison \n - (T)eam stats \n ")

    if answer == "P" or answer == "p":
        return True
    else:
        return False


if InitialDecision():
    selector = PlayerSelector()
    f, ax = plt.subplots(2, 1, sharey=True, figsize=(16, 6))
    sns.barplot(ax=ax[0], data=df[df['LastName'].isin([selector[0]])])
    ax[0].set_title(selector[0])
    sns.barplot(ax=ax[1], data=df[df['LastName'].isin([selector[1]])])
    ax[1].set_title(selector[1])
    plt.show()

else:
    answer = ""
    while answer != "A" and answer != "a" and answer != "S" and answer != "s":
        answer = input(
            "Do you want to view for (A)ll teams, or (S)elect the ones to view ?\n *warning! viewing with all teams migh be hard to read...\n")

    if answer == "A" or answer == "a":
        selector = ListAllTeams()
    else:
        print("\n Here are all the teams : ")
        XColumnDisplay(ListAllTeams(), 5)
        selector = TeamSelector()

    print("Close all plots to continue")
    f, ax = plt.subplots()
    sns.relplot(data=df[df['TEAM'].isin(selector)], x="PTS", y="MIN", hue="W")
    ax.set_title('Points Scored vs Average Time in Game')

    f, ax = plt.subplots(figsize=(10, 6))

    sns.regplot(x='Rank', y='PTS', data=df[df['TEAM'].isin(selector)], order=3)
    ax.set_title('Regression Plot of Rank vs Points Scored')

    f, ax = plt.subplots(figsize=(10, 6))

    sns.kdeplot(data=df[df['TEAM'].isin(selector)], x="OREB", y="FTM", hue="TEAM", thresh=.1)
    ax.set_title('Offensive Rebounds vs FreeThrow Made (successful attempts)')

    corr = df.corr()
    f, ax = plt.subplots(figsize=(8, 6))
    mask = np.triu(np.ones_like(corr[['Rank']].sort_values(by='Rank', ascending=False), dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr[['Rank']].sort_values(by='Rank', ascending=False), vmin=-1, vmax=1, annot=True,
                mask=mask, cmap=cmap)
    ax.set_title('Features Correlating with Rank', fontdict={'fontsize': 18}, pad=16)
    plt.show()

    answer = ""
    while answer != "Y" and answer != "y" and answer != "N" and answer != "n":
        answer = input("Do you want to make your own graph ? Y/N")

    if answer == "Y" or answer == "y":
        parameters = CustomPlotSelector()
        f, ax = plt.subplots()
        sns.relplot(x=parameters[0], y=parameters[1], data=df[df['TEAM'].isin(selector)], hue='TEAM')
        ax.set_title(parameters[0] + " vs " + parameters[1] + " by team")
        plt.show()
print("\nThank you for using our Viewer!")
