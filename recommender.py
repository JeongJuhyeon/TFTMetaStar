from enum import Enum
import operator
import json
from json import JSONEncoder
import jsonpickle
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

meta_comps_list = [
    {'name': 'Cybernetics', 'item_priorities': [1, 1, 1, 0, 0, 1, 2.5, 0, 0], 'picture': 'cybernetics.png'},
    {'name': 'Mech', 'item_priorities': [0, 2.2, 1.4, 2, 1.4, 0.2, 1, 2, 2], 'picture': 'mech_infiltrator.png'},
    {'name': 'Void Battery', 'item_priorities': [0, 0, 0, 1, 3, 0, 0.5, 3, 0], 'picture': 'void_battery.png'},
    {'name': 'Poppy Candyland', 'item_priorities': [0, 3, 1, 2, 1, 1, 0, 0, 0], 'picture': 'poppy_candyland.png'},
    {'name': 'Chrono Kayle', 'item_priorities': [1, 1, 0, 1.3, 1.9, 0.3, 0.3, 0], 'picture': 'chrono_kayle.png'},
    {'name': 'Brawler Blaster', 'item_priorities': [1, 0, 1, 0, 0, 2, 2, 0, 0], 'picture': 'brawler_blaster.png'},
    {'name': 'Xayah', 'item_priorities': [1, 0, .3, 0, 0.7, 1, 3, 0, 0], 'picture': 'xayah.png'},

]
meta_comps = []


class Item(Enum):
    SWORD = 1
    VEST = 2
    BELT = 3
    ROD = 4
    CLOAK = 5
    BOW = 6
    GLOVES = 7
    TEAR = 8
    SPATULA = 9


class ItemCollection:
    def __init__(self, item_values):
        self.item_values = {item: value for (item, value) in zip(Item, item_values)}

    def weighted_items(self):
        weighted_values = self.item_values
        value_sum = sum(weighted_values.values())
        for key in weighted_values:
            weighted_values[key] /= value_sum
        return weighted_values


class Comp:
    def __init__(self, name, item_priorities, picture):
        self.items = ItemCollection(item_priorities)
        self.name = name
        self.picture = picture

    def calculate_score(self, player_items):
        return sum(map(operator.mul, self.items.weighted_items().values(), player_items.item_values.values()))

    def toJson(self):
        return {'name': self.name, 'picture': self.picture}


def get_optimal_comp(player_items):
    score_list = []
    for comp in meta_comps:
        score = comp.calculate_score(player_items)
        score_list.append({'score': score, 'comp': comp})
        print(f"Score: {score}, {comp.name}")
    return max(score_list, key=lambda c: c['score'])['comp']


@app.route('/')
def main_page():
    return render_template('index.html', app_name='TFTMetaStar')


@app.route('/api/itemform', methods=['POST'])
def handle_item_form():
    item_json = request.get_json()
    print(item_json)

    # return {'a': 'b'}
    player_items = ItemCollection([int(v) for v in item_json.values()])
    optimal_comp = get_optimal_comp(player_items)
    return jsonify(optimal_comp.toJson())


if __name__ == '__main__':
    player_items = ItemCollection([0, 3, 0, 1, 0, 1, 2, 2, 1])
    for comp in meta_comps_list:
        meta_comps.append(Comp(**comp))

    app.run()
