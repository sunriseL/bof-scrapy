from flask import Flask,jsonify,render_template,request
import compact
import os

data_folder = "data"
static_folder = "static"
output_file = "data.csv"


app = Flask(__name__,static_url_path="",static_folder=static_folder)
def file_list(name):
	t = {"value":[]}
	for dirpath,dirnames,filenames in os.walk(data_folder):
		if dirpath.startswith(data_folder):
			for fn in filenames:
				if fn.startswith(name):
					t["value"].append(fn)
	t["value"].sort()
	return t


@app.route("/")
def main():
    return "hello"

@app.route('/compact/list', methods=['POST'])
def compact_with_list():
	data = request.form.getlist('value[]')
	print(data)	
	
	
	compact.compact_with_list(data)		
	return 'Compact Success'	


@app.route('/compact/all', methods=['GET','POST'])
def compact_all():
	return 'Compact Success'

@app.route("/bargraph")
def bargraph():
	return render_template('bargraph.html')

@app.route("/select/<name>")
def select(name):
	return render_template('select.html',names=file_list(name)['value'])

@app.route("/files/<name>")
def files(name):
	return jsonify(file_list(name))
	
def latest_file(name):
	return file_list(name)["value"][-1]


@app.route("/select/item/<name>")
def latest_player_list(name):
	with open("data/" + latest_file(name)) as f:
		reader = csv.reader(f)
		rows = [row for row in reader][1:]

	return render_template("select_item.html",names = rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8089)
