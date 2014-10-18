#@Martin Kellogg


import sys
import fractions

def unit_convert( val, unit ):
    val_parts = val.split()
    acc = 0
    for item in val_parts:
        try:
            acc += float(fractions.Fraction(item))
        except:
            continue
    if "cup" in unit or unit == "c" or unit == "c.":
        return (acc, "cups")
    elif "tablespoon" in unit or "tbl" in unit or "tbs" in unit or "tbsp" in unit or unit == "T" or unit == "T.":
        return (acc/16., "cups")
    elif "teaspoon" in unit or "tsp" in unit or unit == "t" or unit == "t.":
        return (acc/48., "cups")
    elif "quart" in unit or unit == "q" or unit == "qt" or unit == "fl qt":
        return (acc/0.25, "cups")
    elif "fluid ounce" in unit or "ounce" in unit or "fl oz" in unit or unit == "oz" or unit =="oz.":
        return (acc*0.125, "cups")
    elif "pint" in unit or unit == "p" or unit =="p." or unit == "pt" or "fl pt" in unit:
        return (acc*2.0, "cups")
    elif "gill" in unit:
        return (acc*.5, "cups")
    elif "gallon" in unit or unit =="g" or unit == "gal":
        return (acc*16.0, "cups")
    elif "mL" in unit or unit == "ml" or "milliliter" in unit or "millilitre" in unit or unit == "cc":
          return (acc*0.00422675, "cups")
    elif "litre" in unit or "liter" in unit or unit == "l" or unit == "L":
        return (acc*0.422675, "cups")
    elif "deciliter" in unit or "decilitre" in unit or unit == "dL" or unit == "dl":
        return (acc* 0.0422675, "cups")
    elif "pound" in unit or unit == "lbs" or unit == "lb" or unit =="#":
        return (acc*.5, "cups")
    elif unit == "g" or "gram" in unit or "gramme" in unit:
        return (0.00220462*0.5*acc, "cups")
    elif unit == "kg" or "kilogram" in unit or "kilogramme" in unit:
        return (0.00220462*0.5*acc/1000.0, "cups")
    else:
        return (acc, unit)

def fract_parse(val):
    val_parts = val.split()
    acc = 0
    for item in val_parts:
        try:
            acc += float(fractions.Fraction(item))
        except:
            continue
    return acc

if __name__ == "__main__":
    ret_val = unit_convert(raw_input(), raw_input())
    print str(ret_val[0]) + " " + ret_val[1]
