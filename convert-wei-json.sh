#!/bin/bash

#Converts Wei's LLM outputs to the simpler format expected by 2-ask-llm-to-analyze-replies.py
#Usage: convert-weicon-json.sh ./20240111_07_23_56_sarah_test.json

rm -rf output.json output-final.json

#step 1: convert Weicon's JSON
jq 'to_entries | map({model_name: .key, replies: .value | map(.text)})' $1 > output.json

#step 2, rename model in new JSON file
while IFS= read -r line
do
  if [[ $line == *"model_name"* ]]; then
    line=${line%%.json*}
    line=${line##*result_}
    line=${line#*_}
    line="\"model_name\": \"$line\","
  fi
  echo "$line" >> $1.cleanedup.json
done <output.json

