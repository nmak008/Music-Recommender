PREF_FILE = 'musicrecplus.txt'

db = open("musicrecplus.txt", "a")
db.close()
db = open("musicrecplus.txt")
contents = db.read()
db.close()
fileName = "musicrecplus.txt"

def loadUsers(fileName):
    '''
        Reads in a file of stored users' preferences stored in the file 'fileName'.
        Returns a dictionary containing a mapping of user names to a list preferred artists
    '''

    file = open(fileName, 'r')
    userDict = {}
    for line in file:
        if ':' in line:
        #Read and parse a single line
        #print(line.strip().split(':'))
            [userName, bands] = line.strip().split(':')
            bandList = bands.split(',')
            bandList.sort()
            userDict[userName] = bandList
    file.close()
    return userDict

userMap = loadUsers(fileName)

def getPreferences(userName, userMap):
    '''
        Returns a list of the user's preferred artists.
        If the system already knows about the user, it gets the preferences out of the userMap dictionary
        and then asks the user if she has additional preferences.
        If the user is new, it simply asks the user for her preferences.
    '''
    newPref = ''
    if userName in userMap:
        prefs = userMap[userName]
    else:
        prefs = []
    if prefs == {}:
        return "No recommendations available at this time"
    while newPref != '':
        prefs.append(newPref.strip().title())
        #Always keep the lists in sorted order for ease of comparsion
    prefs.sort()
    return prefs

def getRecommendations(currUser, prefs, userMap):
    '''
        Get recommendations for a user (currUser) based on the users in userMap (a dictionary) and the user's preferences in pref (a list).
        Returns a list of recommended artists.
    '''
    users = {}
    for key in userMap:
        if key[-1] != '$':
            users[key] = userMap[key]
    if users == {}:
        return "No recommendations available at the time"
    bestUser = findBestUser(currUser, prefs, users)
    if bestUser is None:
        return "No recommendations available at the time"
    recommendations = drop(prefs, users[bestUser])
    recommendations.sort()
    return recommendations

def findBestUser(currUser, prefs, userMap):
    '''
        Find the user whose tastes are closest to the current user.
        Return the best user's name (a string)
    '''
    bestUser = None
    bestScore = 0
    for user in userMap.keys():
        score = numMatches(prefs, userMap[user])
        if score > bestScore and currUser != user:
            bestScore = score
            for preference in userMap[user]:
                if preference not in prefs:
                    bestUser = user 
    return bestUser 

def drop(list1, list2):
    '''
        Returns a new list that contains only the elements in list2 that were NOT in list1.
    '''
    list3 = []
    for l in list2:
        if l not in list1:
            list3 += [l]
    return list3

def numMatches(list1, list2):
    '''
        Return the number of elements that match between two sorted lists
    '''
    i = 0
    j = 0
    matches = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            matches += 1
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return matches

def saveUserPreferences(userName, prefs, userMap, fileName):
    '''
        Writes all of the user preferences to the file.
        Returns nothing.
    '''
    userMap[userName] = prefs
    file = open(fileName, 'w')
    for user in userMap:
        toSave = str(user) + ':' + ','.join(userMap[user]) + '\n'
        file.write(toSave)
    file.close()
    
cont = True

def mostPopular(userMap):
    '''Return the artist with the most likes'''
    users = {}
    for key in userMap:
        if key[-1] != '$':
            users[key] = userMap[key]
    artists = {}
    for user in users:
        for artist in users[user]:
            if artist in artists:
                artists[artist] += 1
            else:
                artists[artist] = 1
    if artists == {}:
        return 'Sorry, no artists found.'
    result, x = [], 0
    while x < 3:
        x += 1
        max = [0, '']
        for (artist, likes) in artists.items():
            if likes > max[0]:
                max[0] = likes
                max[1] = artist
        result += [max[1]]
        artists[max[1]] = 0
    return result[0] + '\n' + result[1] + '\n' + result[2]

def howPopular(userMap):
    '''Returns the number of likes that the most popular artist has'''
    artists = mostPopular(userMap).split('\n')
    artist = artists[0]
    likes = 0
    users = {}
    for key in userMap:
        if key[-1] != '$':
            users[key] = userMap[key]
    for key in users:
        if artist in users[key]:
            likes += 1
    return f"The most popular artist, {artist}, is liked by {likes} people."


def mostLiked(userMap):
    '''Returns the user who likes the most artists'''
    users = {}
    lens = []
    highest = 0
    for key in userMap:
        if key[-1] != '$':
            users[key] = userMap[key]
    if users == {}:
        return 'Sorry, no users found.'
    for key in users:
        r = users[key]
        lens += [[key, len(r)]]
    for item in lens:
        if item[1] > highest:
            highest = item[1]
    for item in lens:
        if item[1] == highest:
            return(item[0])
        
userName = input('Enter your name(put a $ symbol after your name if you wish your preferences to remain private): ')

if userName not in userMap:
    preferences = []
    while True:
        i = input('Enter an artist that you like (Enter to finish):')
        if i == '':
            saveUserPreferences(userName, preferences, userMap, fileName)
            break
        else:
            preferences.append(i)

while(cont):
    choice = input(
        'Enter a letter to choose an option: \n e - Enter preferences\n r - Get recommendations\n p - Show most popular artists\n h - How popular is the most popular\n m - Which user has the most like\n q - Save and quit\n')

    if choice == 'e':
        preferences = []
        while True:
            i = input('Enter an artist that you like (Enter to finish):')
            if i == '':
                saveUserPreferences(userName, preferences, userMap, fileName)
                break
            else:
                preferences.append(i)
    if choice == 'r':
        v = getRecommendations(userName, getPreferences(userName, userMap), userMap)
        if isinstance(v,str):
            print(v)
        else:
            for i in v:
                print(i)
    if choice == 'p':
        print(mostPopular(userMap))
    if choice == 'h':
        print(howPopular(userMap))
    if choice == 'm':
        print(mostLiked(userMap))
    if choice == 'q':
        saveUserPreferences(userName, getPreferences(userName, userMap), userMap, fileName)
        cont = False
