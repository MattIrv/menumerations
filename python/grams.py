import json
import conversion_utility

def gram1():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    ngram_dict = {}
    ing_count = 0.0
    cur_count = 0.0
    for recipe in my_list:
        for ingredient in recipe['ingredients']:
            key = ingredient['ingredient']
            if key not in ngram_dict:
                ngram_dict[key] = 0.0
            ngram_dict[key] += 1.0
            ing_count += 1.0

    for key, val in ngram_dict.iteritems():
        new_val = val / ing_count
        cur_count += new_val
        ngram_dict[key] = cur_count

    return ngram_dict

def gram2():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    ngram_dict = {}
    for recipe in my_list:
        for ingredient in recipe['ingredients']:
            key = ingredient['ingredient']
            if key not in ngram_dict:
                ngram_dict[key] = {}
            for ingredient2 in recipe['ingredients']:
                key2 = ingredient2['ingredient']
                if key2 != key:
                    if key2 not in ngram_dict[key]:
                        ngram_dict[key][key2] = 0.0
                    ngram_dict[key][key2] += 1.0

    for ingredient in ngram_dict:
        cur_sum = 0.0
        val_sum = 0.0
        for key, val in ngram_dict[ingredient].iteritems():
            val_sum += val
        for key, val in ngram_dict[ingredient].iteritems():
            cur_sum += val / val_sum
            ngram_dict[ingredient][key] = cur_sum

    return ngram_dict

def gram3():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    ngram_dict = {}
    for recipe in my_list:
        for ingredient in recipe['ingredients']:
            key = ingredient['ingredient']
            if key not in ngram_dict:
                ngram_dict[key] = {}
            for ingredient2 in recipe['ingredients']:
                key2 = ingredient2['ingredient']
                if key2 != key:
                    if key2 not in ngram_dict[key]:
                        ngram_dict[key][key2] = {}
                    for ingredient3 in recipe['ingredients']:
                        key3 = ingredient3['ingredient']
                        if key3 != key2 and key3 != key:
                            if key3 not in ngram_dict[key][key2]:
                                ngram_dict[key][key2][key3] = 0.0
                            ngram_dict[key][key2][key3] += 1.0

    for ingredient in ngram_dict:
        for ingredient2 in ngram_dict[ingredient]:
            cur_sum = 0.0
            val_sum = 0.0
            for key, val in ngram_dict[ingredient][ingredient2].iteritems():
                val_sum += val
            for key, val in ngram_dict[ingredient][ingredient2].iteritems():
                cur_sum += val / val_sum
                ngram_dict[ingredient][ingredient2][key] = cur_sum

    return ngram_dict

#does not quite work...
def ratios():
    print "DONT USE THIS PLZ"
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    ngram_dict = {}
    for recipe in my_list:
        for ingredient in recipe['ingredients']:
            key = ingredient['ingredient']
            value = ingredient['value']
            unit = ingredient['unit']
            converted_val = conversion_utility.unit_convert(value, unit)[0]
            if key not in ngram_dict:
                ngram_dict[key] = {}
            for ingredient2 in recipe['ingredients']:
                key2 = ingredient2['ingredient']
                try:
                    value2 = conversion_utility.fract_parse(ingredient2['value']) / converted_val
                    unit2 = ingredient2['unit']
                    if key2 != key:
                        if key2 not in ngram_dict[key]:
                            ngram_dict[key][key2] = []
                        ngram_dict[key][key2].append({'value' : value2, 'unit' : unit2})
                except:
                    continue

    return ngram_dict

def measures_of():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    ngram_dict = {}
    for recipe in my_list:
        for ingredient in recipe['ingredients']:
            key = ingredient['ingredient']
            val = ingredient['value']
            u = ingredient['unit']
            if key not in ngram_dict:
                ngram_dict[key] = []
            ngram_dict[key].append({'value' : val, 'unit' : u})

    return ngram_dict

def ingredients_to_ids():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    all_ingredients = {}
    for recipe in my_list:
        recipe_id = recipe['id']
        for ing in recipe['ingredients']:
            ingredient = ing['ingredient']
            if ingredient not in all_ingredients:
                all_ingredients[ingredient] = []
            all_ingredients[ingredient].append(recipe_id)

    return all_ingredients

def ids_to_instructions():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    all_instructions = {}
    for recipe in my_list:
        recipe_id = recipe['id']
        all_instructions[recipe_id] = []
        for ins in recipe['instructions']:
            all_instructions[recipe_id].append(ins['instruction'])

    return all_instructions

def ids_to_ingredients():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    all_ingredients = {}
    for recipe in my_list:
        recipe_id = recipe['id']
        all_ingredients[recipe_id] = []
        for ing in recipe['ingredients']:
            all_ingredients[recipe_id].append(ing['ingredient'])

    return all_ingredients

def recipe_by_key():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    all_names = {}
    for recipe in my_list:
        recipe_name = recipe['name']
        all_names[recipe_name] = {}
        all_names[recipe_name]['id'] = recipe['id']
        all_names[recipe_name]['ingredients'] = recipe['ingredients']
        all_names[recipe_name]['instructions'] = recipe['instructions']
        all_names[recipe_name]['name'] = recipe_name

    return all_names

def recipe_by_id():
    f = open('output.txt', 'r')
    to_decode = f.read()
    my_list = json.loads(to_decode)
    all_ids = {}
    for recipe in my_list:
        recipe_id = recipe['id']
        all_ids[recipe_id] = {}
        all_ids[recipe_id]['id'] = recipe_id
        all_ids[recipe_id]['ingredients'] = recipe['ingredients']
        all_ids[recipe_id]['instructions'] = recipe['instructions']
        all_ids[recipe_id]['name'] = recipe['name']

    return all_ids
