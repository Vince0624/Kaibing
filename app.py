import csv
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = "Kaibing Zhang"  # 名字
    id_card = "75996"  # 最后5位数字
    picture_url = "static/pic.jpg"  # 照片URL
    return render_template('index.html', name=name, id_card=id_card, picture_url=picture_url)

@app.route('/reviews')
def reviews():
    # 读取amazon-reviews.csv文件
    reviews = []
    with open('amazon-reviews.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviews.append(row)

    # 读取us-cities.csv文件
    cities = {}
    with open('us-cities.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cities[row['city']] = row

    return render_template('reviews.html', reviews=reviews, cities=cities)

@app.route('/city/<city>')
def city_details(city):
    cities = {}
    with open('us-cities.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cities[row['city']] = row

    city_info = cities.get(city)
    return render_template('city_details.html', city_info=city_info, cities=cities)

@app.route('/popular_words', methods=['GET'])
def popular_words():
    city = request.args.get('city')  # 获取请求参数中的city
    limit = int(request.args.get('limit', -1))  # 获取请求参数中的limit，默认为-1

    # 读取amazon-reviews.csv文件
    reviews = []
    with open('amazon-reviews.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if city is None or row['city'] == city:  # 如果city为None或者与请求参数中的city相等
                reviews.append(row)

    # 统计每个单词的出现次数
    word_count = {}
    for review in reviews:
        words = review['review'].lower().split()  # 将评论内容转为小写并拆分为单词
        for word in words:
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1

    # 根据出现次数降序排序
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # 构建响应列表
    response = []
    for term, popularity in sorted_words[:limit]:
        response.append({"term": term, "popularity": popularity})

    # return jsonify(response)
    return render_template('popular_words.html', words=response)

if __name__ == '__main__':
    app.run()
