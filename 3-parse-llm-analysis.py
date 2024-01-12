





#Parses a single answer from the judge LLM, and puts its data in a dictionary
def parse_llm_analysis(llm_analysis):
    facial_expression = re.findall("1\.\s(.)", llm_analysis)
    friendliness = re.findall("2\.\s(.)", llm_analysis)
    hand_gesture = re.findall("3\.\s(.)", llm_analysis)
    wink = re.findall("4\.\s(.)", llm_analysis)
    greeting = re.findall("5\.\s(.)", llm_analysis)
    fruit = re.findall("6\.\s(.)", llm_analysis)

    As = len([r for r in [facial_expression, friendliness, hand_gesture, wink, greeting, fruit] if r == ['A']])
    Bs = len([r for r in [facial_expression, friendliness, hand_gesture, wink, greeting, fruit] if r == ['B']])
    Cs = len([r for r in [facial_expression, friendliness, hand_gesture, wink, greeting, fruit] if r == ['C']])

    result = {}
    result['facial_expression'] = facial_expression[0] if facial_expression else 'N/A'
    result['friendliness'] = friendliness[0] if friendliness else 'N/A'
    result['hand_gesture'] = hand_gesture[0] if hand_gesture else 'N/A'
    result['wink'] = wink[0] if wink else 'N/A'
    result['greeting'] = greeting[0] if greeting else 'N/A'
    result['fruit'] = fruit[0] if fruit else 'N/A'
    result['number_of_A_answers'] = As
    result['number_of_B_answers'] = As
    result['number_of_C_answers'] = As

    return result




def main():
    print("TODO")


if __name__ == "__main__":
  main()