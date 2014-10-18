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

gram1_dict = grams.gram1()
gram2_dict = grams.gram2()
gram3_dict = grams.gram3()
measures = grams.measures_of()
ingredients_to_ids = grams.ingredients_to_ids()
ids_to_instructions = grams.ids_to_instructions()
ids_to_ingredients = grams.ids_to_ingredients()

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
    banned = {'large', 'medium', 'small', 'grated', 'chopped', 'diced', 'sliced', 'mashed', 'red', 'green', 'black', 'yellow', 'teaspoon', 'tablespoon', 'cup', 'pint', 'hot', 'cold', 'warm', 'quart', 'gallon', 'prepared', 'boiling', 'thin', 'thick', 'stick', 'finely chopped', 'crushed', 'lean', 'melted', 'heated', 'cooled', 'chilled', 'packed', 'cooked', 'baked', 'hop', 'salted', 'unsalted', 'sweetened', 'unsweetened', 'whole', 'dried', 'm', 'brown', 'sweet', 'spicy', 'fresh', 'frozen', 'whipped', 'fried', 'sauteed', 'grilled', 'broiled', 'toasted', 'diced', 'uncooked', 'minced', 'cubed', 'ripe', 'steamed'}
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
    return (to_print, final_ins_set)

if __name__ == '__main__':
    generateRecipe()


