import requests, json, math

# Steam interfaces: ISteamUser ISteamUserStats IPlayerService
apiRoot='http://api.steampowered.com/'
apiKey='2685F2D1D5793A0FFA5CC01EEAD62653'
steamId='76561198072055054'

def callSteamWebAPIMethod(interfaceName, methodName, version, params=''):
    url=apiRoot+interfaceName+'/'+methodName+'/v'+version+'/?key='+apiKey+params
    # print('Requesting '+ url)
    response = requests.get(url)
    return json.loads(response.text)

def getOwnedGameCount():
    ownedGameResponse = callSteamWebAPIMethod('IPlayerService', 'GetOwnedGames', '0001', '&include_appinfo=true&steamId='+steamId)
    return ownedGameResponse['response']['game_count']
    
def getOwnedGameIds():
    ownedGameResponse = callSteamWebAPIMethod('IPlayerService', 'GetOwnedGames', '0001', '&include_appinfo=true&include_played_free_games=1&steamId='+steamId)
    gameIds = []
    for game in ownedGameResponse['response']['games']:
        gameIds.append({'appid':game['appid'], 'name':game['name']})
    return gameIds

def getNumberOfAchievementsForGame(appId):
    totalAchievements = 0
    gameStats = callSteamWebAPIMethod('ISteamUserStats', 'GetGlobalAchievementPercentagesForApp', '0002', '&gameid='+str(appId))
    if 'achievementpercentages' in gameStats:
        for achievement in gameStats['achievementpercentages']['achievements']:
            totalAchievements += 1
    return totalAchievements

def getCompletionRateForGame(appId, totalAchievements):
    totalAchieved=0
    userStatsForGame = callSteamWebAPIMethod('ISteamUserStats', 'GetUserStatsForGame', '0002', '&steamId='+steamId+'&appid='+str(appId))
    if 'playerstats' in userStatsForGame:
        if 'achievements' in userStatsForGame['playerstats']:
            for achievement in userStatsForGame['playerstats']['achievements']:
                if 'achieved' in achievement:
                    totalAchieved += 1
    return totalAchieved / totalAchievements * 100

print('Number of owned games: ' + str(getOwnedGameCount()))

totalRanked = 0
sumOfAllRates = 0
for game in getOwnedGameIds():
    totalAchievements = getNumberOfAchievementsForGame(game['appid'])
    #print('Total number of achievements for ' + game['name'] + ' is: ' + str(totalAchievements))
    if totalAchievements > 0:
        completionRate = getCompletionRateForGame(game['appid'], totalAchievements)
        if completionRate > 0:
            totalRanked +=1
            sumOfAllRates += math.floor(completionRate)
            print('Completion rate for "' + game['name'] + '" is ' + str(math.floor(completionRate)) + '%')

# Account for refunded games
totalRanked += 3

totalGameAchievementRate = sumOfAllRates / totalRanked
print('\nTotal game completion rate is ' + str(totalGameAchievementRate) + '%')

# TODO: calculate remaining % to boost total avg %

input()
