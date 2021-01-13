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

def getUserStatsForGame(appId):
    userStatsForGame = callSteamWebAPIMethod('ISteamUserStats', 'GetUserStatsForGame', '0002', '&steamId='+steamId+'&appid='+appId)
    if 'playerstats' in userStatsForGame:
        if 'achievements' in userStatsForGame['playerstats']:
            for achievement in userStatsForGame['playerstats']['achievements']:
                
            print(userStatsForGame['playerstats']['achievements'])
        
print('Number of owned games: ' + str(getOwnedGameCount()))

for game in getOwnedGameIds():
    print(game)
    getUserStatsForGame(str(game['appid']))
    

input()
