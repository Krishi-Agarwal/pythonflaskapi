from flask import Flask, request, jsonify
import io
import numpy as np
from rembg import remove
from PIL import Image

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    # Get image from request
    img_file = request.files['image']
    input_img = Image.open(img_file.stream)

    # Remove background from image
    output_img = remove(input_img).convert("RGBA")

    # Convert the image to a numpy array
    img_array = np.array(output_img)

    # Find the non-zero rows and columns
    rows, cols = np.where(img_array[:, :, 3] != 0)
    top_row, bottom_row = rows.min(), rows.max()
    left_col, right_col = cols.min(), cols.max()

    # Crop the image
    cropped_img = output_img.crop((left_col, top_row, right_col, bottom_row))

    # Get colors of cropped image
    colors = cropped_img.getcolors(maxcolors=2**24)
    newcolors=list(colors)

    # Find second most common color and remove it from list of colors
    def colorextraction():
        first_most_common_color=max(newcolors, key=lambda x: x[0])
        for i in newcolors:
            if(i==first_most_common_color):
                newcolors.remove(i)
        fmc=first_most_common_color[1]
        cfmc=first_most_common_color[0]
        if(fmc[0]!=0 and fmc[1]!=0 and fmc[2]!=0):
            return fmc,cfmc
        else:
            return colorextraction()

    rc=colorextraction()
    fmc=rc[0]
    cfmc=rc[1]

    # Second most common color and remove it from list of colors
    second_most_common_color=max(newcolors, key=lambda x: x[0])
    for i in newcolors:
        if(i==second_most_common_color):
            newcolors.remove(i)
    smc=second_most_common_color[1]
    csmc=second_most_common_color[0]

    #third most common color
    third_most_common_color=max(newcolors, key=lambda x: x[0])
    for i in newcolors:
        if(i==third_most_common_color):
            newcolors.remove(i)
    tmc=third_most_common_color[1]
    ctmc=third_most_common_color[0]

    # Return results as JSON
    result = {
        #'first_most_common_color': fmc,
        'second_most_common_color': smc,
        # 'third_most_common_color': tmc,
       # 'first_most_common_count': cfmc,
        'second_most_common_count': csmc,
        # 'third_most_common_count': ctmc,
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run()
