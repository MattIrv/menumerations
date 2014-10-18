import json
from twilio.rest import TwilioRestClient 
from flask import Flask, make_response, render_template
app = Flask(__name__)

def respond(text):
	resp = make_response(render_template('index.html', text=text))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
	
@app.route("/send/<path:IngList>&<num>")
def send(IngList, num):
	Output = "Ingredients: " + IngList
	ACCOUNT_SID = "" 
	AUTH_TOKEN = "" 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	try:
		client.messages.create(
			to=""+num, 
			from_="+12025172536", 
			body=str(Output),  
    	)
	except:
		return respond("Error: Text Unable To Send. Please Check number")
	return respond("Sent text message.")

@app.route("/create/<IngList>&<num>&<name>&<int:sendText>")
def create(IngList, num, name, sendText):
    WhatToMake = name
    WhatWeHave = IngList.split(',');
    WhatWeNeed = []
    PhoneNumber = num
    Item_Found_Flag = False
    Output = "Shopping List: "
    ACCOUNT_SID = "" 
    AUTH_TOKEN = "" 
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
    f = open('output.txt', 'r')
    to_decode = f.read()
    lst = json.loads(to_decode)
    print IngList + " " + num + " " + name + " " + `sendText`

    for baby_lst in lst:
        rcp_title = baby_lst['name']
        if rcp_title.lower() == WhatToMake.lower():
            Item_Found_Flag = True
            for itm in baby_lst['ingredients']:
                WhatWeNeed.append(itm['ingredient'])  

        if Item_Found_Flag == True:
#Removes the elements of WhatWeHave from WhatWeNeed-----
            for ingredient in WhatWeHave:
                try:
                    WhatWeNeed.remove(ingredient.lower())        
            	except:
		    pass
	    Output = "Shopping List: "
            for i in WhatWeNeed:
                Output+=' ' + i + ';'
        else:
            Output = "Recipe Not Found;"
    
    if sendText == 1:
	try:
            client.messages.create(
                to=""+PhoneNumber, 
                from_="+11234567890", 
                body=str(Output[:-1]),  
            )
        except:
            return respond("Error: Text Unable To Send. Please Check number")
    
    return respond(Output[:-1])
    
import grams
import random
import find_ins

global gram1_dict
global gram2_dict
global gram3_dict
global measures
global ingredients_to_ids
global ids_to_instructions
global ids_to_ingredients
global recipe_by_key
global recipe_by_id

gram1_dict = grams.gram1()
gram2_dict = grams.gram2()
gram3_dict = grams.gram3()
measures = grams.measures_of()
ingredients_to_ids = grams.ingredients_to_ids()
ids_to_instructions = grams.ids_to_instructions()
ids_to_ingredients = grams.ids_to_ingredients()
recipe_by_key = grams.recipe_by_key()
recipe_by_id = grams.recipe_by_id()

def getRandFromDict(d, num):
    for key, val in sorted(d.items(), key=lambda x: x[1]):
        if val > num:
            return key

def getRelevantInstructions(ingredient, instruction_list, bob=True, threshold=.4):
    ingredient_words = ingredient.split()
    rel_instructions = []
    for instruction in instruction_list:
        matched_word_count = 0
        for word in ingredient_words:
            if word in instruction:
                matched_word_count += 1
        if matched_word_count > threshold * len(ingredient_words):
            rel_instructions.append(instruction)
    #choose random element to add
    #if instruction_list and bob:
    #    rel_instructions.append(random.sample(instruction_list, 1)[0])
    return rel_instructions

def getIngredientFromStr(input_str, measures):
    if input_str in measures:
        unit_val_dict = random.sample(measures[input_str], 1)[0]
        return {'ingredient' : input_str, 'unit' : unit_val_dict['unit'], 'value' : unit_val_dict['value']}

def removeTooSimilar(input_list):
    to_remove = set()
    for string1 in input_list:
        for string2 in input_list:
            if string1 != string2:
                if string2.lower() in string1.lower():
                    to_remove.add(string2)
    for item in to_remove:
        input_list.remove(item)
    return input_list

@app.route("/generate/<ingredient_list_str>")
def generateRecipe(ingredient_list_str=''):
    global gram1_dict
    global gram2_dict
    global gram3_dict
    global measures
    global ingredients_to_ids
    global ids_to_instructions
    global ids_to_ingredients

    input_list = ingredient_list_str.split(',')
    ingredient_set = set()
    for ing in input_list:
        if getIngredientFromStr(ing, measures):
            ingredient_set.add(ing)
    num_ingredients = 6

    while len(ingredient_set) < num_ingredients:
        randy = random.random()
        new_ing = ''
        if not ingredient_set:
            new_ing = getRandFromDict(gram1_dict, randy)
        elif len(ingredient_set) == 1:
            ing = random.sample(ingredient_set, 1)[0]
            new_ing = getRandFromDict(gram2_dict[ing], randy)
        else:
            try:
                ings = random.sample(ingredient_set, 2)
                new_ing = getRandFromDict(gram3_dict[ings[0]][ings[1]], randy)
            except:
                ing = random.sample(ingredient_set, 1)[0]
                new_ing = getRandFromDict(gram2_dict[ing], randy)
        ingredient_set.add(new_ing)

    ins_set_one = find_ins.find_ins_set(ingredient_set)
    final_ins_set = find_ins.refine_ins_set(ins_set_one)
    banned = {'large', 'medium', 'small', 'grated', 'chopped', 'diced', 'sliced', 'mashed', 'red', 'green', 'black', 'yellow', 'teaspoon', 'tablespoon', 'cup', 'pint', 'hot', 'cold', 'warm', 'quart', 'gallon', 'prepared', 'boiling', 'thin', 'thick', 'stick', 'finely chopped', 'crushed', 'lean', 'melted', 'heated', 'cooled', 'chilled', 'packed', 'cooked', 'baked', 'hop', 'salted', 'unsalted', 'sweetened', 'unsweetened', 'whole', 'dried', 'm', 'brown', 'sweet', 'spicy', 'fresh', 'frozen', 'whipped', 'fried', 'sauteed', 'grilled', 'broiled', 'grilled', 'broiled', 'toasted', 'diced', 'uncooked', 'minced', 'cubed', 'ripe', 'steamed', 'freshly ground'}
    for ins in final_ins_set:
        for key in measures.keys():
            if key in ins:
                if not key.lower() in banned:
                    ingredient_set.add(key)
    
    ingredient_set = removeTooSimilar(ingredient_set)
    to_print = []
    ingredient_set_list = []
    for item in ingredient_set:
        ingredient_set_list.append(getIngredientFromStr(item, measures))
    for item in ingredient_set_list:
        if not item['unit']:
            to_print.append(item['value'] + ' ' + item['ingredient'])
        elif item['unit'] == 'to taste':
            to_print.append(item['ingredient'] + ', to taste')
        else:
            to_print.append(item['value'] + ' ' + item['unit'] + ' ' + item['ingredient'])
    print to_print
    print final_ins_set
    print_str = ''
    for item in to_print:
        print_str += str(item) + ';;;'
    print_str += ';;;'
    for item in final_ins_set:
    	print_str += str(item) + ';;;'
    return respond(print_str)

@app.route("/getbest/<input_str>")
def getBestMatch(input_str):
    global recipe_by_key
    input_words = input_str.split()
    max_count = 0
    max_recipe = None
    for recipe_name in recipe_by_key.keys():
        cur_count = 0
        for word in input_words:
            if word.lower() in recipe_name.lower():
                cur_count += 1
        if cur_count > max_count:
            max_count = cur_count
            max_recipe = recipe_by_key[recipe_name]

    return respond(recipeToString(max_recipe))

def recipeToString(recipe):
    to_print = ''
    to_print += recipe['name'] + ';;;;;;'
    for item in recipe['ingredients']:
        if not item['unit']:
            to_print += item['value'] + ' ' + item['ingredient']
        elif item['unit'] == 'to taste':
            to_print += item['ingredient'] + ', to taste'
        else:
            to_print += item['value'] + ' ' + item['unit'] + ' ' + item['ingredient']
        to_print += ';;;'
    to_print += ';;;'
    for item in recipe['instructions']:
        to_print += item['instruction']
        to_print += ';;;'
    return to_print

@app.route("/getrec/<input_str>")
def getRecipeNamesWithIngredients(input_str):
    global ingredients_to_ids
    global recipe_by_id
    input_ings = input_str.split(',')
    ids_dict = {}
    for ing in input_ings:
        if ing in ingredients_to_ids:
            associated_ids = ingredients_to_ids[ing]
            for associated_id in associated_ids:
                if associated_id not in ids_dict:
                    ids_dict[associated_id] = 0
                ids_dict[associated_id] += 1
    ids_list = []
    for recipe in sorted(ids_dict, key=ids_dict.get, reverse=True):
        ids_list.append(recipe)
    relevant_recipes = ids_list[:10]
    to_print = ''
    for recipe_id in relevant_recipes:
        recipe = recipe_by_id[recipe_id]
        to_print += recipe['name'] + ';;;'
    return respond(to_print)

@app.route("/nametorec/<recipe_name>")
def nameToRecipe(recipe_name):
    global recipe_by_key
    if recipe_name in recipe_by_key:
        return respond(recipeToString(recipe_by_key[recipe_name]))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
