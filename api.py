import time
from urllib.parse import urlencode, urlparse
import requests
import json


def get_my_friend_list(user_id, params):
    response_my_friends_list = []
    params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get?fields=deactivated', params)
    my_friends_list = response.json()['response']['items']
    for friend in my_friends_list:
        try:
            if friend['deactivated']:
                print(friend)
        except:
            response_my_friends_list.append(friend['id'])
    return response_my_friends_list


def get_my_groups_list(user_id, params):
    params['user_id'] = user_id
    my_groups = requests.get('https://api.vk.com/method/groups.get', params).json()['response']['items']
    return my_groups


def get_my_friends_groups_list(my_friends_list, params):
    response_my_friends_groups = []
    for friend in my_friends_list:
        params['user_id'] = friend
        print(friend)
        try:
            response_my_friends = requests.get('https://api.vk.com/method/groups.get', params)
            response_my_friends_groups.extend(response_my_friends.json()['response']['items'])
        except:
            try:
                time.sleep(3)
                response_my_friends = requests.get('https://api.vk.com/method/groups.get', params)
                response_my_friends_groups.extend(response_my_friends.json()['response']['items'])
            except:
                pass
    return response_my_friends_groups


def get_my_unique_groups_list(my_friends_groups_list, my_groups, params):
    my_unique_group_list = []
    end_result_file_list = []
    for group_name in my_groups:
        if str(group_name) not in my_friends_groups_list:
            my_unique_group_list.append(group_name)
            print(my_unique_group_list)
    for group in my_unique_group_list:
                params['group_ids'] = group
                params['fields'] = 'members_count'
                groups = requests.get('https://api.vk.com/method/groups.getById', params)
                for group_el in groups.json()['response']:
                    data = {'name': group_el['name'].replace('ō', 'o'),
                            'gid': group_el['id'],
                            'members_count': group_el['members_count']}
                    end_result_file_list.append(data)
                    print(end_result_file_list)
    with open('groups.json', 'w', encoding='cp1251') as groups_output:
                    json.dump(end_result_file_list,
                              groups_output, ensure_ascii=False)

def main():
        user_id = 5030613
        VERSION = '5.63'
        token_url = 'https://oauth.vk.com/blank.html#access_token=d13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22&expires_in=86400&user_id=5030613'
        o = urlparse(token_url)
        fragments = dict((i.split('=') for i in o.fragment.split('&')))
        access_token = fragments['access_token']
        params = {'access_token': access_token,
                  'v': VERSION,
                  }
        my_friends_list = get_my_friend_list(user_id, params)
        print(my_friends_list)
        my_groups = get_my_groups_list(user_id, params)
        print(my_groups)
        my_friends_groups_list = get_my_friends_groups_list(my_friends_list,params)
        print(my_friends_groups_list)
        # with open('friends_groups_test.txt', 'r') as friends_groups:
        #     for line in friends_groups:
        #         my_friends_groups_list = line
        params = {'access_token': access_token,
                 'v': VERSION,
                 }
        get_my_unique_groups_list(my_friends_groups_list, my_groups, params)

main()
