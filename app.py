from flask import Flask, render_template
import csv
app = Flask(__name__)

@app.route('/')
def index():
    name = "Kaibing Zhang"  # 您的名字
    id_card = "12345"  # 您的身份证上的最后5位数字
    picture_url = "static/pic.png"  # 如果有照片，请将此变量设置为照片的URL
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




if __name__ == '__main__':
    app.run()
