import requests, json

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
    ownedGameResponse = callSteamWebAPIMethod('IPlayerService', 'GetOwnedGames', '0001', '&include_appinfo=true&steamId='+steamId)
    gameIds = []
    for game in ownedGameResponse['response']['games']:
        gameIds.append({'appid':game['appid'], 'name':game['name']})
    return gameIds

def getNumberOfAchievementsForGame(appId):
    totalAchievements = 0
    gameStats = callSteamWebAPIMethod('ISteamUserStats', 'GetGlobalAchievementPercentagesForApp', '0002', '&gameid='+appId)
    if 'achievementpercentages' in gameStats:
        for achievement in gameStats['achievementpercentages']['achievements']:
            totalAchievements += 1
    return totalAchievements

def getAchievementRateForGame(appId, totalAchievements):
    totalAchieved=0
    userStatsForGame = callSteamWebAPIMethod('ISteamUserStats', 'GetUserStatsForGame', '0002', '&steamId='+steamId+'&appid='+appId)
    if 'playerstats' in userStatsForGame:
        #print(userStatsForGame['playerstats'])
        if 'achievements' in userStatsForGame['playerstats']:
            for achievement in userStatsForGame['playerstats']['achievements']:
                totalAchievements += 1
                if 'achieved' in achievement:
                    totalAchieved += 1
    completionRate = totalAchieved / totalAchievements * 100
    print('Completion rate is: ' + str(completionRate))
            
def getUserStatsForGame(appId):
    totalAchievements=0 #Must be replaced by call to getNumberOfAchievementsForGame()
    totalAchieved=0
    userStatsForGame = callSteamWebAPIMethod('ISteamUserStats', 'GetUserStatsForGame', '0002', '&steamId='+steamId+'&appid='+appId)
    if 'playerstats' in userStatsForGame:
        #print(userStatsForGame['playerstats'])
        if 'achievements' in userStatsForGame['playerstats']:
            for achievement in userStatsForGame['playerstats']['achievements']:
                totalAchievements += 1
                if 'achieved' in achievement:
                    totalAchieved += 1
            completionRate = totalAchieved / totalAchievements * 100
            print('Completion rate is: ' + str(completionRate))
        
print('Number of owned games: ' + str(getOwnedGameCount()))

for game in getOwnedGameIds():
    totalAchievements = getNumberOfAchievementsForGame(str(game['appid']))
    print('Total number of achievements for ' + game['name'] + ' is: ' + str(totalAchievements))
    if totalAchievements > 0:
        getAchievementRateForGame(str(game['appid']), totalAchievements)

input()
