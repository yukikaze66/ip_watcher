#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from multiping import multi_ping
from multiping import MultiPing
from functools import reduce

def load_equipment_list(file_name):
    data_list = None

    with open(file_name) as stream:
        try:
            data_list = yaml.load(stream)
        except yaml.YAMLError as err:
            print(err)

    return data_list

class Equipment(object):

    def __init__(self, data):
        self.name = data['name']
        self.ip = data['ip']
        self.position = data['position']
        self.type = data['type']
        self.campus = data['campus']

    def __repr__(self):
        return 'Equipment({}, {}, {}, {}, {})'.format(self.name, self.ip, self.position, self.type, self.campus)


class Room(object):

    def __init__(self, position):
        self.position = position
        self.intact = True

    def __repr__(self):
        return 'ROOM({}, {})'.format(self.position, self.intact)

    
def init_equipment_list(data_list):

    eq_list = []

    for data in data_list:
        eq_list.append(Equipment(data))
    
    return eq_list

def do_ping_test(eq_list, timeout):

    ip_eq_map = {}
    for eq in eq_list:
        ip_eq_map[eq.ip] = eq

    position_set = set([eq.position for eq in eq_list])
    
    position_room_map = {}
    for position in list(position_set):
        position_room_map[position] = Room(position)

    ip_list = ip_eq_map.keys()

    # no_results = multi_ping(ip_list, timeout, 3)[1]
    
    no_results = ip_list
    for i in range(10):
        mp = MultiPing(no_results)
        mp.send()
        no_results = mp.receive(3)[1]

    failed_eq_list = []
    for ip in no_results:
        failed_eq_list.append(ip_eq_map[ip])

    for eq in failed_eq_list:
        room = position_room_map[eq.position]
        room.intact = False
    room_list = list(position_room_map.values())
    room_list = sorted(room_list, key=lambda room: room.intact)
    
    return failed_eq_list, room_list


def room_list_to_yaml(room_list):

    room_list = sorted(room_list, key=lambda room: (room.intact, room.position))

    template = \
'''
- position: {}
  intact: {}
'''

    obj_list = []
    for room in room_list:
        string_token = template.format(room.position, room.intact)
        obj_list.append(string_token)
    str_buffer = reduce(lambda a, b: a+b, obj_list)
    return str_buffer


def failed_equipment_list_to_yaml(failed_eq_list):

    failed_eq_list = sorted(failed_eq_list, key=lambda eq: eq.position)

    template = \
'''
- name: {}
  ip: {}
  position: {}
  type:  {}
  campus: {}
'''
    obj_list = []
    for eq in failed_eq_list:
        string_token = template.format(
            eq.name,
            eq.ip,
            eq.position,
            eq.type,
            eq.campus,
        )
        obj_list.append(string_token)
    str_buffer = reduce(lambda a, b: a+b, obj_list)
    return str_buffer

def output_to_file(room_list_file_name, room_list_yaml_str, failed_equipment_list_file_name, failed_equipment_list_yaml_str):

    with open(room_list_file_name, 'w') as f:
        f.write(room_list_yaml_str)
        f.flush
    
    with open(failed_equipment_list_file_name, 'w') as f:
        f.write(failed_equipment_list_yaml_str)
        f.flush
    


if __name__ == '__main__':
    file_name = './gear/equipment_list.yml'
    data_list = load_equipment_list(file_name)
    eq_list = init_equipment_list(data_list)
    failed_eq_list, room_list = do_ping_test(eq_list, timeout=30)

    room_list_yaml_str = room_list_to_yaml(room_list)
    failed_equipment_list_yaml_str = failed_equipment_list_to_yaml(failed_eq_list)

    print(failed_equipment_list_yaml_str)

    failed_equipment_list_file_name = './_data/failed_equipment_list.yml'
    room_list_file_name = './_data/room_list.yml'

    output_to_file(room_list_file_name, room_list_yaml_str, failed_equipment_list_file_name, failed_equipment_list_yaml_str)
