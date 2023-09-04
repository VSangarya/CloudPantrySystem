from flask import Flask, request, jsonify
import random
import json
import csv
import ast

app = Flask(__name__)

#In grams
coffee_1_serv = {"coffee_powder" : 10, "milk" : 20, "sugar" : 5}
latte_1_serv = {"coffee_powder" : 5, "milk" : 5, "sugar" : 2}
tea_1_serv = {"tea_powder" : 5, "milk" : 10, "sugar" : 3}

all_recipe_dicts ={
    "Coffee" : coffee_1_serv,
    "Latte" : latte_1_serv,
    "Tea" : tea_1_serv
}

ingredient_dict = {
    "Milk": ["milk", 1],
    "Sugar": ["sugar", 2],
    "Coffee powder": ["coffee_powder", 3],
    "Tea powder": ["tea_powder", 4]
}

def read_csv(ingredient_str, ingredient_dict):
    with open('/var/www/FlaskApp/FlaskApp/response.csv', 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
    data = last_line.split(",")
    data = [int(i) for i in data]
    if ingredient_str == "all":
        ret_dict = {
            "inventory" : {
            "Milk": data[1],
            "Sugar": data[2],
            "Coffee powder": data[3],
            "Tea powder": data[4]
        }}
    elif ingredient_str == "Coffee" or ingredient_str == "Latter":
        ret_dict = {
            "milk": data[1],
            "sugar": data[2],
            "coffee_powder": data[3]
        }
    elif ingredient_str == "Tea":
        ret_dict = {
            "milk": data[1],
            "sugar": data[2],
            "tea_powder": data[4]
        }
    else:
        ret_dict = {
            "quantity_left": data[ingredient_dict[ingredient_str][1]]
        }
    return ret_dict

def compute_possible_coffee(ingredients_avail_dict, servings_request, recipe_dict, recipe_string):
    flag = 0
    possible_servings = {}
    servings_str = {"blank":""}

    if recipe_string == "Coffee" or recipe_string == "Latte":
        str1 = "coffee_powder"
        str2 = "milk"
        str3 = "sugar"
    elif recipe_string == "Tea":
        str1 = "tea_powder"
        str2 = "milk"
        str3 = "sugar"

    if recipe_dict[str1]*servings_request > ingredients_avail_dict[str1] : 
        flag = 1
        servings_str[str1] = f"Shortage of {str1}, required: {recipe_dict[str1]*servings_request}g, but available: {ingredients_avail_dict[str1]}g"
    if recipe_dict[str2]*servings_request > ingredients_avail_dict[str2] : 
        flag = 1
        servings_str[str2] = f"Shortage of {str2}, required: {recipe_dict[str2]*servings_request}g, but available: {ingredients_avail_dict[str2]}g"
    if recipe_dict[str3]*servings_request > ingredients_avail_dict[str3] : 
        flag = 1
        servings_str[str3] = f"Shortage of {str3}, required: {recipe_dict[str3]*servings_request}g, but available: {ingredients_avail_dict[str3]}g"
    
    min_servings = min([int(ingredients_avail_dict[str1]/recipe_dict[str1]),
                        int(ingredients_avail_dict[str2]/recipe_dict[str2]),
                        int(ingredients_avail_dict[str3]/recipe_dict[str3])])
    possible_servings["possible_question_mark"] = False if flag == 1 else True
    possible_servings["possible_servings"] = min_servings
    possible_servings["misc_string_info"] = servings_str

    #Computing just to see how the requested vs available ingredients look, can be used for later debugging
    request_based_required_servings = {
        str1: recipe_dict[str1]*servings_request,
        str2: recipe_dict[str2]*servings_request,
        str3: recipe_dict[str3]*servings_request
    }
    print("#"*120)
    print(f"Requested recipe: {recipe_string}")
    print(f"Servings reqested: {servings_request}")
    print(f"Servings possible: {min_servings}")
    print(f"Required ingredients per requested servings: {request_based_required_servings}")
    print(f"Available ingredients(recived by pi):        {ingredients_avail_dict}")
    print(f"Miscellaneous string info: {servings_str}")
    print("#"*120)
    return possible_servings

@app.route('/query1', methods=['POST'])
async def query1():
    print("*"*60)
    print("User called query 1")
    print("*"*60)
    ddb1 = request.form['ddb1']
    ib1 = request.form['ib1']
    response = read_csv(ddb1, ingredient_dict)
    ret_dict = compute_possible_coffee(response, int(ib1), all_recipe_dicts[ddb1], ddb1)
    return ret_dict
    
@app.route('/query2', methods=['POST'])
async def query2():
    print("*"*60)
    print("User called query 2")
    print("*"*60)
    ddb2 = request.form['ddb2']
    response = read_csv(ddb2, ingredient_dict)
    print(response)
    return response

@app.route('/query3', methods=['POST'])
async def query3():
    print("*"*60)
    print("User called query 3")
    print("*"*60)
    response = read_csv("all", ingredient_dict)
    print(response)
    return response

@app.route('/query4', methods=['POST'])
async def query4():
    print("*"*60)
    print("User called query 4")
    print("*"*60)
    ib2 = int(request.form['ib2'])
    with open('/var/www/FlaskApp/FlaskApp/response.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
        last_few_data = data[-ib2:]
    return jsonify(last_few_data)

@app.route('/query6', methods=['GET'])
async def query6():
    print("*"*60)

    print("*"*60)
    return "OK"

@app.route('/query5', methods=['GET'])
async def query5():
    print("*"*60)
    print("User called query6")
    print("*"*60)
    with open('/var/www/FlaskApp/FlaskApp/heartbeat/pi_active.csv', 'r') as f:
        lines = f.readlines()
        latest_val = lines[-1]
        data = latest_val.strip().split(",")
        timestamp = data[0].strip()
        status =  data[1].strip()
    data_return = {"time":timestamp, "status":status}
    print(data_return)
    return data_return

if __name__ == '__main__':
    app.run()
