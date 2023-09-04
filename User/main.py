import time
import math
from flask import Flask, render_template, request
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests

app = Flask(__name__)

server_ip_port = 'http://34.69.210.151'

def return_graph():
    df = pd.read_csv('history.csv')
    df['Time'] = pd.to_datetime(df['Time'], unit='s').dt.tz_localize('utc').dt.tz_convert('US/Eastern')
    fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(12, 18))
    axs[0].plot(df["Time"], df["Milk"], color="red")
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Milk")
    axs[0].set_title("Milk vs Time")
    axs[1].plot(df["Time"], df["Sugar"], color="green")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Sugar")
    axs[1].set_title("Sugar vs Time")
    axs[2].plot(df["Time"], df["Coffee_powder"], color="blue")
    axs[2].set_xlabel("Time")
    axs[2].set_ylabel("Coffee_powder")
    axs[2].set_title("Coffee_powder vs Time")
    axs[3].plot(df["Time"], df["Tea_powder"], color="orange")
    axs[3].set_xlabel("Time")
    axs[3].set_ylabel("Tea_powder")
    axs[3].set_title("Tea_powder vs Time")
    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    plt.savefig("static/images/plot.jpg")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        if query == 'query1':
            return query1()
        elif query == 'query2':
            return query2()
        elif query == 'query3':
            return query3()
        elif query == 'query4':
            return query4()
        elif query == 'query5':
            return query5()
        elif query == 'query6':
            return query6()
    return render_template('index.html')

def query1():
    ddb1 = request.form['ddb1']
    ib1 = request.form['ib1']
    data = {}
    data['ddb1'] = ddb1
    data['ib1'] = ib1
    response = requests.post(f"{server_ip_port}/query1", data=data)
    response = json.loads(response.content)
    requested_servings_status = response['possible_question_mark']
    possible_servings = response['possible_servings']
    miscellaneous_str_info = response['misc_string_info']
    return render_template('recipe.html', ddb1=ddb1, ib1=ib1, rs=requested_servings_status, ps=possible_servings, msi=miscellaneous_str_info)

def query2():
    ddb2 = request.form['ddb2']
    data = {}
    data['ddb2'] = ddb2
    response = requests.post(f"{server_ip_port}/query2", data=data)
    response_data = json.loads(response.content)
    quantity_left = response_data['quantity_left']
    return render_template('spec_ingredients.html', ddb2=ddb2, quantity_left=quantity_left)

def query3():
    response = requests.post(f"{server_ip_port}/query3")
    response_data = json.loads(response.content)
    inventory = response_data['inventory']
    return render_template('all_ingredients.html', quantities=inventory)

def query4():
    ib2 = request.form['ib2']
    data = {}
    data['ib2'] = ib2
    response = requests.post(f"{server_ip_port}/query4", data=data)
    response_data = json.loads(response.content)
    with open("history.csv", "w") as f:
        f.write("Time,Milk,Sugar,Coffee_powder,Tea_powder")
    for each in response_data:
        with open("history.csv", "a") as f:
            f.write(f"\n{each['Time']},{each['Milk']},{each['Sugar']},{each['Coffee_powder']},{each['Tea_powder']}")
    f.close()
    return_graph()
    return render_template("graph.html", user_image="plot.jpg")

def query5():
    response = requests.get(f"{server_ip_port}/query5")
    response_data = json.loads(response.content)
    status = response_data['status']
    time_stamp = datetime.datetime.fromtimestamp(float(response_data['time']))
    time_diff = int(math.ceil((time.time()-float(response_data['time']))/3600))
    time_stampstr = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('pi_status.html', status=status, time_stampstr=time_stampstr, time_diff=time_diff)

def query6():
    try:
        response = requests.get(f"{server_ip_port}/query6")
        response_status = response.status_code
        response_message = response.ok
    except:
        response_status = 500
        response_message = "Connection refused"
    return render_template('connection.html', resp_stat=response_status, resp_msg=response_message)


if __name__ == '__main__':
    app.run(debug=True)
