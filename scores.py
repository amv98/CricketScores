import json
import time
import requests
import notify2

notify2.init('Scores')
base_url = 'http://cricapi.com/api/'

def read_api_key():
    f = open('apikey', 'r')
    return f.readline().strip()

def get_matches():
    api_url = base_url + 'matches/'
    request_header = {"apikey": api_key}
    response = requests.get(api_url, headers = request_header)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))

def started_matches(data):
    matches = []
    for i in data['matches']:
        if i['matchStarted']:
            matches.append(i)
    return matches

def get_score(match_id):
    api_url ='http://cricapi.com/api/cricketScore/?unique_id=' +str(match_id) + '&apikey=' + api_key;
    response = requests.get(api_url)
    if response.status_code == 200:
        temp = json.loads(response.content.decode('utf-8'))
        if 'score' not in temp.keys():
            return "Match not started yet."
        else:
            return temp['score']

def select_match(started_matches):
    index = 1
    print("Select the match: ")
    for i in started_matches:
        print(index, i["team-2"],"vs", i["team-1"])
        index += 1
    match_id = int(input())
    t = started_matches[match_id - 1]
    return t["unique_id"], t["team-2"], t["team-1"]

def display_message(title, message):
    n = notify2.Notification(title, message, "notification-message-im")
    n.show()

if __name__ == '__main__':
    api_key = read_api_key()
    data = get_matches()
    started_matches = started_matches(data)
    match_id, team_2, team_1 = select_match(started_matches)
    while True:
        title = team_2 + " vs " + team_1
        score = get_score(match_id)
        display_message(title, score)
        time.sleep(8 * 60)
