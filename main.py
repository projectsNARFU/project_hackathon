import json
import ast


def create_coord(info_coord):
    with open("choosed_coords.geojson", 'w') as f:
        f.write(json.dumps(info_coord))
    f.close()


def input_coord(coord):
    """вводим координаты местности"""
    # coord = input("введите координаты в формате: широта долгота")
    coord = coord.replace(',', '')
    coord = coord.split()
    if -90 <= int(coord[0]) <= 90 and -180 <= int(coord[1]) <= 180:
        info_coord = {"coordinates": coord, "type": "Point"}
        create_coord(info_coord)
        return True
    else:
        return False


if __name__ == '__main__':
    input_coord('1221 12')

    with open("choosed_coords.geojson", 'r') as f:
        info_coord = f.readline()
        info_coord = ast.literal_eval(info_coord)
    f.close()
