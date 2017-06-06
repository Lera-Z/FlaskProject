import requests
import json

def get_groups(group1, group2):
    error_1 = False
    error_2 = False
    count_1 = 0
    count_2 = 0
    intersect = []
    is_closed_1 = 0
    is_closed_2 = 0

    response_1 = requests.get('https://api.vk.com/method/groups.getMembers?group_id={}'.format(group1))
    response_2 = requests.get('https://api.vk.com/method/groups.getMembers?group_id={}'.format(group2))
    info_1 = requests.get('https://api.vk.com/method/groups.getById?group_id={}'.format(group1))
    info_2 = requests.get('https://api.vk.com/method/groups.getById?group_id={}'.format(group2))

    d_1_info = json.loads(info_1.text)
    d_2_info = json.loads(info_2.text)
    if 'error' in d_1_info:
        error_1 = True
    else:
        is_closed_1 = d_1_info['response'][0]['is_closed']
        d_1 = json.loads(response_1.text)
        count_1 = d_1['response']['count']

    if 'error' in d_2_info:
        error_2 = True
    else:
        is_closed_2 = d_2_info['response'][0]['is_closed']
        d_2 = json.loads(response_2.text)
        count_2 = d_2['response']['count']

        intersect = list(set(d_1['response']['users']) & set(d_2['response']['users']))
        len_intersect = len(intersect)

    return count_1, count_2, intersect, is_closed_1, is_closed_2, error_1, error_2, len_intersect


def main():
    count1, count2, intersect, is_closed_1, is_closed_2, error_1, error_2, len_intersect = get_groups(
        'притотвры',
        'pikabu'
    )
    print(count1, count2, intersect)

if __name__ == '__main__':
    main()
