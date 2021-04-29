from flask import Flask
from flask import request, redirect, render_template, url_for, send_from_directory

import urllib3
from lxml import etree

app = Flask(__name__)


@app.route('/')
def index():
    get_data()
    return render_template('index.html', from_text=str(0),
                           get_data=get_data, into_text=0)


def get_data():
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://www.cbr.ru/scripts/XML_daily.asp')
    r.data.decode('cp1251')
    xml = r.data
    root = etree.fromstring(xml)
    data = {}
    for appt in root.getchildren():
        l = appt.getchildren()
        data[l[1].text] = {}
        for item in l[1:]:
            data[l[1].text][item.tag] = item.text
    print(data)
    return data


@app.route('/', methods=['POST'])
def convert():
    data = get_data()
    currency_from = request.form.getlist('from_selector')
    currency_from1 = currency_from[0][:3]
    currency_into = request.form.getlist('into_selector')
    currency_into1 = currency_into[0][:3]
    value = float(request.form.get('from_text'))
    print(currency_into)
    print('\n')
    print(currency_from)
    res = process_convertation(currency_from1, currency_into1, value)
    print(str(res))
    from1 = currency_from[0] + ' ' + data[currency_from1]['Name']
    into1 = currency_into[0] + ' ' + data[currency_into1]['Name']
    return render_template('index.html', from_selector=from1, into_selector=into1, from_text=value,
                           get_data=get_data, into_text=res)


def process_convertation(s1, s2, var):
    data = get_data()
    temp = var * (float(data[s1]['Value'].replace(',', '.')) / float(data[s1]['Nominal']))
    res = temp / (float(data[s2]['Value'].replace(',', '.')) / float(data[s2]['Nominal']))
    return res


if __name__ == '__main__':
    app.run(debug=True)
