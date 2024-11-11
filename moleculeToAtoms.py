# SOLUTION USING RECURSION

import re
def algo(
        regexResults,           # List of raw regex results
        outside_multiplier,     # Index encompassing the entire group (NH3)4. <--- 4 is the outside_multiplier
        regexString,            # The regex query.
        elements):              # Dict(string, int) of all the elements.
    
    group_and_multipliers = {}

    # results is the raw list of groups, including brackets, parenthesis, and indexes.
    for res in regexResults:
        last_char = res[-1]
        # if the last character is a number, a multiplier is present.
        if last_char.isdigit():
            
            # multipliers can be a string of length greater than 2, 
            # so we traverse the string from last element until we find a non digit character.
            howFarAwayFromEndAreWeUntilWeMeetElement = 0
            initial_multiplier = ""
            for c in res[::-1]:
                if c.isdigit():
                    initial_multiplier += c
                    howFarAwayFromEndAreWeUntilWeMeetElement += 1
                else:
                    break
            group = res[0: len(res) - howFarAwayFromEndAreWeUntilWeMeetElement]

                
            # we also need to reverse the initial multiplier because we traversed the string backwards.
            initial_multiplier = int(initial_multiplier[::-1])
            multiplier = initial_multiplier*outside_multiplier
        # if the last character is not a number, no multiplier is present, it is 1.
        else:
            group = res
            multiplier = 1*outside_multiplier

        # check if its a group or an element by checking the first character
        if group.startswith("{") or group.startswith("[") or group.startswith("("):
            group = group[1 : len(group) - 1]

        # key is the group string and the value is the multiplier
        if group not in group_and_multipliers.keys():
            group_and_multipliers[group] = multiplier
        else:
            group_and_multipliers[group] += multiplier

    # BASE CASE
    if len(group_and_multipliers.keys()) == 1:
        for group in group_and_multipliers.keys():
            if group not in elements.keys():
                elements[group] = group_and_multipliers[group]
                return elements
            else:
                elements[group] += group_and_multipliers[group]
                return elements
            
    for group in group_and_multipliers.keys():
        _results = re.findall(regexString, group)
        algo(_results, group_and_multipliers[group], regexString, elements)
    return elements
                
def parse_molecule(formula):
    regex = [
        "{.*}[0-9]*",
        "\\[.*\\][0-9]*",
        "\\([A-Za-z-0-9]*\\)[0-9]*",
        "[A-Z][a-z][0-9]*|[A-Z][0-9]*"
    ]
    regexOfAllTime = "|".join(regex)
    results = re.findall(regexOfAllTime, formula)
    print(regexOfAllTime)
    return algo(results, 1, regexOfAllTime, {})