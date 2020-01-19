import pandas
import json
best = json.load(open("/Users/Kaushik/programs/smile/reddit_jokes.json"))
top = sorted(best, key = lambda x:x["score"])
json.dump(top[-100:], open("best.json", "w"), indent = 4)
