"""
Parses manual-reply-evaluations.json and assigns a score to each model.

For each model, it outputs:
Bad-Sarah-Score: 123
Bad-Sarah-Score-Capped: 50
Consistency-Score: 123
Percentage-Of-Interesting-Replies: 50%
"""

import os
import json
import sys
import statistics

#-1 point for Good Sarah reference, +1 point per Bad Sarah reference, -1 point for incoherences 
def calculate_bad_sarah_score(reply):
    score = 0
    score -= reply[0]
    score += reply[1]
    score -= reply[2]
    return score

#-1 point for Good Sarah reference, +1 point per Bad Sarah reference, -1 point for incoherences
#maximum 2 point penalty or bonus
def calculate_bad_sarah_score_capped(reply):
    score = 0
    score -= reply[0] if reply[0] < 2 else 2
    score += reply[1] if reply[1] < 2 else 2
    score += reply[2] if reply[2] < 2 else 2
    return score


def calculate_consistency_ratio(reply):
    absolute_purity_score = abs(reply[0] - reply[1])
    total_response_score = reply[0] + reply[1]
    if total_response_score == 0:
        return 1

    consistency_ratio = absolute_purity_score / total_response_score
    return round(consistency_ratio, 2)
    



script_dir = os.path.dirname(os.path.abspath(__file__))

with open(script_dir + "/manual-reply-evaluations.json", 'r') as f:
    inputjson = json.load(f)

final_scores = {}
for model in inputjson:
    replies = inputjson[model]

    combined_bad_sarah_score = 0
    combined_bad_sarah_score_capped = 0
    consistency_ratios = []
    combined_interesting_replies = 0
    for reply in replies:
        reply_bss = calculate_bad_sarah_score(reply)
        combined_bad_sarah_score += reply_bss

        reply_bssc = calculate_bad_sarah_score_capped(reply)
        combined_bad_sarah_score_capped += reply_bssc

        consistency_ratio = calculate_consistency_ratio(reply)
        consistency_ratios.append(consistency_ratio)

        combined_interesting_replies += reply[3]


    interesting_replies_value = combined_interesting_replies * 100 / len(replies)
    interesting_replies_value = round(interesting_replies_value, 2)
    
    mean_consistency_ratio = statistics.mean(consistency_ratios)
    mean_consistency_ratio = round(mean_consistency_ratio, 2)

    final_scores[model] = {
        "bad_sarah_score": combined_bad_sarah_score,
        "bad_sarah_score_capped": combined_bad_sarah_score_capped,
        "mean_consistency_ratio": mean_consistency_ratio,
        "interesting_replies_percent": interesting_replies_value
    }

print(final_scores)
with open(script_dir + "/scores.json", mode="w") as f:
    f.write(json.dumps(final_scores, indent=2))
