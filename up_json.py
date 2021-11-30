import json
import data
big_data={}
big_data["goals"] = data.goals 
big_data["teachers"] = data.teachers 
#print (big_data["teachers"][0]["about"])
with open ('data.json','w') as f:
    json.dump(big_data,f,indent=4,ensure_ascii=False)