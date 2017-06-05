import time
from urllib.parse import urlparse
import requests
import json
import backoff


def get_my_friend_list(user_id, params):
    # get list of friends of the incoming user
    response_my_friends_list = []
    params['user_id'] = user_id
    response = requests.get(
        'https://api.vk.com/method/friends.get?fields=deactivated', params)
    my_friends_list = response.json()['response']['items']
    for friend in my_friends_list:
        try:
            if friend['deactivated']:
                pass
        except:
            response_my_friends_list.append(friend['id'])
    return response_my_friends_list


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException, max_tries=5000)
def get_group_list(user_list, params):
    # get groups of incoming lsit of ids/id
    response_groups = []
    for user in user_list:
        time.sleep(3)
        print(user)
        params['user_id'] = user
        group_list = requests.get('https://api.vk.com/method/groups.get',
                                  params)
        response_groups.append(group_list.json()['response']['items'])
    return response_groups


def get_my_unique_groups_list(my_friends_groups_list, my_groups, params):
    # compare the list of groups of Oleg Blokhin in
    # comparasion with list of groups of his friends
    my_unique_group_list = []
    end_result_file_list = []
    my_friends_groups_list = sum(my_friends_groups_list, [])
    for group_name in my_groups:
        print(group_name)
        if group_name not in my_friends_groups_list:
            my_unique_group_list.append(group_name)
    print(my_unique_group_list)
    for group in my_unique_group_list:
                params['group_ids'] = group
                params['fields'] = 'members_count'
                groups = requests.get(
                    'https://api.vk.com/method/groups.getById', params)
                for group_el in groups.json()['response']:
                    data = {'name': group_el['name'].replace('ō', 'o'),
                            'gid': group_el['id'],
                            'members_count': group_el['members_count']}
                    end_result_file_list.append(data)
    print(end_result_file_list)
    with open('groups.json', 'w', encoding='cp1251') as groups_output:
        json.dump(end_result_file_list, groups_output, ensure_ascii=False)


def main():
        user_id = 5030613
        VERSION = '5.63'
        token_url = 'https://oauth.vk.com/blank.html#' \
                    'access_token=d13e692be6959' \
                    '2b09fd22c77a590dd34e186e6d696da' \
                    'a88d6d981e1b4e296b14acb377e82dcbc81dc0f22&' \
                    'expires_in=86400&' \
                    'user_id=5030613'
        o = urlparse(token_url)
        fragments = dict((i.split('=') for i in o.fragment.split('&')))
        access_token = fragments['access_token']
        params = {'access_token': access_token,
                  'v': VERSION,
                  }
        my_friends_list = get_my_friend_list(user_id, params)
        print(my_friends_list)
        params = {'access_token': access_token,
                  'v': VERSION,
                  }
        my_groups = get_group_list([user_id], params)
        print(my_groups)
        params = {'access_token': access_token,
                  'v': VERSION,
                  }
        my_friends_groups_list = get_group_list(
            my_friends_list, params)
        print(my_friends_groups_list)
        params = {'access_token': access_token,
                  'v': VERSION,
                  }
        get_my_unique_groups_list(my_friends_groups_list, my_groups, params)

main()
