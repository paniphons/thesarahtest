
import json
import os

tablestring = """
Model | Bad-Sarah-Score-Capped | Bad-Sarah-Score | Consistency-Ratio | % Interesting Replies
------ | ------ | ------ | ------ | ------
"""

script_dir = os.path.dirname(os.path.abspath(__file__))
with open(script_dir + "/scores.json", 'r') as f:
    inputjson = json.load(f)

# for model in inputjson:
#     scores = inputjson[model]
#     newline = f"{model} | {scores['bad_sarah_score_capped']} | {scores['bad_sarah_score']} | {scores['mean_consistency_ratio']} | {scores['interesting_replies_percent']}%\n"
#     tablestring += newline

# print(tablestring)

sorted_models =  sorted(inputjson, key=lambda x: (inputjson[x]['bad_sarah_score_capped']), reverse=True)
for model in sorted_models:
    scores = inputjson[model]
    newline = f"{model} | {scores['bad_sarah_score_capped']} | {scores['bad_sarah_score']} | {scores['mean_consistency_ratio']} | {scores['interesting_replies_percent']}%\n"
    tablestring += newline

print(tablestring)
