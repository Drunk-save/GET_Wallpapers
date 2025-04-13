from flask import Flask, render_template
from flask import request, jsonify
from urllib.request import urlopen
from urllib import  request as urllib_request
from json import loads,dumps
from bs4 import BeautifulSoup
import os
app = Flask(__name__)

# 示例数据
wallpapers = []
pictures_path = 'static\pictures'

def a():
    global wallpapers
    headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    length = ['week','day'][1]
    sercj_url = urllib_request.Request("https://api.anime-pictures.net/api/v3/posts?page=0&search_tag={search_tag}&order_by=date&ldate=0&lang=zh-cn",headers=headers,method="GET")
    top = "https://api.anime-pictures.net/api/v3/top?length={length}"
    posts_url = "https://anime-pictures.net/posts/{id}"
    response = loads(
        urlopen(
            urllib_request.Request(
                top.format(length=length),
                headers=headers,
                method="GET"
            )
        ).read().decode('utf-8'))['top']
    print(0)
    for i in response:
        json_format = {
                'id':i['id'],
                'url' : ''
            }
        wallpapers.append(json_format)
    print(1)
    for i in wallpapers:
        response = urlopen(urllib_request.Request(posts_url.format(id=i['id']),headers=headers,method="GET")).read().decode('utf-8')
        soup = BeautifulSoup(response, 'lxml')
        i['url'] = soup.select_one('#big_preview').get('src')
@app.route('/')
def index():
    a()
    return render_template('index.html', wallpapers=wallpapers)

@app.route('/api/data', methods=['POST'])
def post_data():
    datas = request.get_json()
    if datas is None:
        return jsonify({"error": "No JSON data found"}), 400

    for data in datas:
        urllib_request.urlretrieve(data, os.path.join(pictures_path,data.split("/")[-1]+'.jpg'))

    return jsonify({"response":'0'})

if __name__ == '__main__':
    app.run(debug=True)