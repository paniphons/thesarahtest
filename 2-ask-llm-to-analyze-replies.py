#Refer to https://rentry.org/thesarahtest
#asks an LLM to interpret Sarah's reply (from the LLMs being tested)

import tempfile
import os
import json
import shutil
import sys
import llama_cpp #pip install llama-cpp-python 


"""
Expecting input JSON (given as an arg for this script):
[
    {
        model_name: "mistral-7B",
        replies: [
          reply1,
          reply2,
          replyN
        ]
    },
    {
        model_name: "SOLAR",
        ...
    }
]

And we will output output/llm-analysis/model_name.json (if it exists, model_name.2.json, etc)
Output format:
{
    model_name: "mistral-7B",
    llm_analysis: [
        {
            reply_analyzed: "...",
            llm_analysis: llm_analysis_for_above_reply
        }
    ]
}
"""




our_grammar = llama_cpp.LlamaGrammar.from_string("""
root ::= line+
line ::= [0-9] "." " " [ABC] "\r"? "\n"
""")
def get_llm_analysis(reply, llm):
    prompt_template = """Task to perform: please analyze this response I got while interacting with Sarah:
```$INSERT-REPLY-HERE```

Answer the following questions, answering either 'A' or 'B' or 'C':
1. What was Sarah's facial expression? If she smiled, answer 'A'. If she frowned, answer 'B'. If neither, answer 'C'.
2. Was Sarah friendly or rude? If she was friendly, answer 'A'. If she was rude, answer 'B'. If neither, ansewr 'C'.
3. Did Sarah make a hand gesture? If she gave me the peace sign, answer 'A'. If she gave me the middle finger, answer 'B'. If she didn't make a hand gesture, or she made a different gesture, answer 'C'. 
4. Did Sarah wink? If she winked with her left eye, answer 'A'. If she winked with her right eye, answer 'B'. If she didn't wink, or you're unsure, answer 'C'.
5. If Sarah said 'Aloha', answer 'A'. If she said 'Meh', answer 'B'. If she said neither, answer 'C'.
6. Did Sarah express any dislike of any particular fruit? If she dislikes apples, answer 'A'. If she dislikes oranges, answer 'B'. Otherwise, answer 'C'.  

Don't explain your reasoning, only give A/B/C for each of the 6 questions. Here is an example answer:
```
1. D
2. D
3. D
4. D
5. D
6. D
```
(Note that D is not a valid answer, it's only given as an example.).

PLEASE BEGIN ANSWERING NOW!

Assistant:"""

    prompt = prompt_template.replace("$INSERT-REPLY-HERE", reply)
    output = llm(prompt, max_tokens=512, grammar=our_grammar)
    print("---the model reply---")
    print(reply)
    print("---got the following judge analysis---")
    print(output)
    print("---")

    return output
    

#modelname is a string, analysises is a list of tuples created in main()
def save_model_analysises_to_json(modelname, analysises):
    #save to temp first so permissions issues dont cause us to redo the LLM part
    temp_directory = tempfile.TemporaryDirectory() 
    modeltempdir = temp_directory.name + "/" + modelname
    print("Putting temp files in", modeltempdir)
    os.makedirs(modeltempdir, exist_ok=True)

    temp_file_name = None
    with tempfile.NamedTemporaryFile(dir=modeltempdir, mode="w", delete=False) as tmp:
        temp_file_name = tmp.name

        dic = {}
        dic['model_name'] = modelname
        dic['llm_analysis'] = {}
        for analysis in analysises:
            dic['llm_analysis']['reply_analyzed'] = analysis[0]
            dic['llm_analysis']['llm_analysis'] = analysis[1]

        tmp.write(json.dumps(dic))
    
    print(modelname, "analysis saved to", temp_file_name, "temporarily")
    #now move to destination of script output/llm-analysis/model_name.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = script_dir + "/output/llm-analysis"
    os.makedirs(output_dir, exist_ok=True)
    new_file_path = output_dir + 'apples.txt'
    counter = 1
    while os.path.exists(new_file_path):
        new_file_path = output_dir + f'apples.txt.{counter}'
        counter += 1
    shutil.move(temp_file_name, new_file_path)
    
    print(modelname, "analysis saved to", new_file_path)



def main():

    input_filename = None
    if len(sys.argv) < 2:
        sys.exit("Error: No argument provided. Give the JSON file with LLM replies as argument.")
    else:
        input_filename = sys.argv[1]

    inputjson = None
    with open(input_filename, 'r') as f:
        inputjson = json.load(f)


    #This is the model that will judge other models' replies. Pick the best you can run.
    
modelpath="C:/tools/text-generation-webui/models/upstage_SOLAR-10.7B-Instruct-v1.0/solar-10.7b-instruct-v1.0.Q4_K_M.gguf"
    print("Loading judge model...")
    #NOTE: only the first 2 args are necessary, delete n_gpu_layers if you have issues
    llm = llama_cpp.Llama(model_path=modelpath, n_ctx=4096, n_gpu_layers=20, verbose=True)
    print("Judge model loaded!")


    #Now let's ask the LLM to interpret the replies
    for entry in inputjson:
        model_name= entry['model_name']

        replies = entry['replies']

        analysises = [] #list of tuples where first value is original reply, 2nd value is analysis
        for reply in replies:
            llm_analysis = get_llm_analysis(reply, llm)
            tup = (reply, llm_analysis)
            analysises.append(tup)
        
        save_model_analysises_to_json(model_name, analysises)

if __name__ == "__main__":
  main()
