from flask import Flask, request, jsonify
from webcolors import rgb_to_name, CSS3_HEX_TO_NAMES, hex_to_rgb
from scipy.spatial import KDTree

app = Flask(__name__)

@app.route('/get_color_name', methods=['POST'])
def get_color_name():
    # Get RGB color from request
    data = request.get_json()
    rgb_tuple = tuple(data['rgb'])

    try:
        # first try to get the name of the color directly
        color_name = rgb_to_name(rgb_tuple, spec='css3')
    except ValueError:
        # if the color is not found, find the closest matching color
        css3_db = CSS3_HEX_TO_NAMES
        names = []
        rgb_values = []
        for color_hex, color_name in css3_db.items():
            
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))
        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        color_name = names[index]

    # Return results as JSON
    result = {
        'color_name': color_name,
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
