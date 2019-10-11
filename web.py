from flask import Flask,jsonify
from . import compact
import os

data_folder = "/home/sunrise/bofxv/bof-scrapy/data"
static_folder = "/home/sunrise/static"
output_file = "data.csv"


app = Flask(__name__,static_url_path="/static",static_folder="/home/sunrise/static")
@app.route("/")
def main():
    return "hello"

@app.route("/files/<name>")
def files(name):
	t = {"value":[]}
	for dirpath,dirnames,filenames in os.walk(data_folder):
		print(dirpath)
		if dirpath.startswith(data_folder):
			for fn in filenames:
				if fn.startswith(name):
					t["value"].append(fn)
	t["value"].sort()
	return jsonify(t)
	
	    

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8089)
