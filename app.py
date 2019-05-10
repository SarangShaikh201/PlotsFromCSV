import os
import shutil
import pandas as pd

from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

import check_datatypes
import possible_combinations
import plot_graphs

UPLOAD_FOLDER = "csv_files"
ALLOWED_EXTENSIONS = ['csv']
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

plot_path = os.path.join(os.getcwd(),"static")

class Path():
    csv_path = None

data = Path()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data.path = os.path.join(os.getcwd(),"csv_files")
            data.path = os.path.join(data.path,filename)
            csv = pd.read_csv(data.path, delimiter=",",
                              encoding="ISO-8859-1", nrows=1).columns.tolist()
            return render_template('choose_axes.html', col_1 = csv)
    return render_template('upload.html')


@app.route('/visualize', methods=['GET','POST'])
def visualize():
    if os.path.isdir(plot_path):
        shutil.rmtree(plot_path)
        os.mkdir(plot_path)
    else:
        os.mkdir(plot_path)
    column_names = request.form.getlist("columns_names")
    csv = pd.read_csv(data.path, delimiter=",",
                      encoding="ISO-8859-1")
    csv_data = pd.DataFrame(csv)
    column_dtypes = {}
    for item in column_names:
        temp = [0, 0, 0, 0]  # [Numeric/Non-Numeric, Discrete/Continous, Date, Zip]
        if check_datatypes.check_is_date(csv_data, item):
            temp[2] = 1
        else:
            if check_datatypes.check_is_numeric(csv_data, item):
                temp[0] = 1
            if check_datatypes.check_is_discrete(csv_data, item):
                temp[1] = 1
            if check_datatypes.check_is_zip(csv_data, item):
                temp[3] = 1
        column_dtypes[item] = temp
    #
    print("column_names",column_names)
    print("column_dtypes",column_dtypes)
    column_types = plot_graphs.get_columns_types(column_dtypes)
    print("column_types", column_types)
    if len(column_names) > 1:
        possible_plots = possible_combinations.get_all_columns_combinations(column_names)
        print("possible_plots",possible_plots)
        valid_combinations = plot_graphs.get_valid_combinations(possible_plots,column_types)
        plot_graphs.plot_charts(csv_data,valid_combinations,plot_path)
        plot_graphs.dual_axis_chart(csv_data,possible_plots,column_types,plot_path)
        plot_graphs.plot_aggregate_data(csv_data,valid_combinations,plot_path)
    plot_graphs.plot_single_column_charts(csv_data,column_types,column_names,plot_path)
    image_names = os.listdir('static')
    return render_template("gallery.html", image_names=image_names)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('static')
    return render_template("gallery.html", image_names=image_names)


if __name__ == '__main__':
   app.run(host='0.0.0.0',port='5000')
