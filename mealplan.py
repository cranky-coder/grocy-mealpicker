#   {
#     "day": "2023-12-01",
#     "type": "recipe",
#     "recipe_id": 10,
#     "section_id": 1
#   }

# use the above json to post the recipe ID to a spcecific day to add to meal plan.  Endpoint to send to is
# https://grocy.k8.mybackflip.com/api/objects/meal_plan
# returns the meal plan iD  shouldn't be needed




import requests
import json
from datetime import datetime, timedelta,date
import random
import ast
import sys
from datetime import datetime, timedelta
headers = {
    'cache-control': "no-cache",
    'GROCY-API-KEY': <YOUR_GROCY_API_KEY>,
    "accept": "application/json"
    }



import urllib3

urllib3.disable_warnings()
dinnerneedcount=0
dinnerdaysneeddinner =[]

mygrocy_url = "https://YOUR_GROCY_URL"


def checkdayforplan(dayofweek):
   
    
    global dinnerneedcount, dinnerdaysneeddinner
   
    dt = datetime.today() + timedelta(days=dayofweek)
    from dateutil.relativedelta import relativedelta, FR
    

    url = mygrocy_url + "/api/objects/meal_plan?query%5B%5D=day%3D" + dt.strftime('%Y-%m-%d') + "&query%5B%5D=section_id%3D1"
    print(url)
    response = requests.request("GET", url, headers=headers, verify=False)
    responsejson = response.json()
    print(len(responsejson))
    if (len(responsejson) == 0 ):
        ## no dinner found increase dinnerneedcount
        dinnerneedcount=dinnerneedcount+1
        dinnerdaysneeddinner.append(dayofweek)

    



# get current datetime
dt = datetime.today() + timedelta(days=1)
from dateutil.relativedelta import relativedelta, FR
nextFriday = datetime.now() + relativedelta(weekday=FR(1))
nextFriday.replace(hour=16,minute=0,second=0,microsecond=0)
#print(nextFriday)
headers = {
    'cache-control': "no-cache",
    'GROCY-API-KEY': "oDxSIiHEFZaAsKb727Bsh9rspcKAElFK8001bYsMxxlcpQHnB4",
    "accept": "application/json"
    }

for loopweekdays in range(6):
    checkdayforplan(loopweekdays)

# get day of week as an integer
weekdaynum = dt.weekday()
print(nextFriday.strftime('%Y-%m-%d'))


########################## first make sure friday has pizza

url = mygrocy_url + "/api/objects/meal_plan?query%5B%5D=day%3D" + nextFriday.strftime('%Y-%m-%d') + "&query%5B%5D=section_id%3D1&query%5B%5D=%20recipe_id%3D10"
print(url)

print()
print()
print()
print()
print("end")



response = requests.request("GET", url, headers=headers, verify=False)
fridaymp = response.json()
print("res len")
print(fridaymp)
if (len(fridaymp) == 0):
    ## that means no pizza
    jsondata={"day": nextFriday.strftime('%Y-%m-%d'),"type": "recipe","recipe_id": 10,    "recipe_servings": 1,    "section_id": 1  }
    url=mygrocy_url + "/api/objects/meal_plan"
    resp = requests.post(url=url,headers=headers, verify=False,json=jsondata)
    print(resp.status_code)
    print("added pizza")

print(len(fridaymp))
print("res len")
####### end friday pizza





#response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

#print(type(response.json()))




url = mygrocy_url + "/api/objects/recipes?query%5B%5D=type%3Dnormal"



response = requests.request("GET", url, headers=headers, verify=False)
allrecipes = response.json()
recipeDict = {}
#print(len(allrecipes))
for a in allrecipes:
    removed=False
    # print(a["id"],a["name"])
    # print(a["userfields"])
    # print(a["userfields"]['TypeOfRecipe'])
    if (a["userfields"]['TypeOfRecipe'] != None):
        my_list = str(a["userfields"]['TypeOfRecipe']).split(",")
        if("Dinner" not in my_list):
            #needs to be removed
            allrecipes.remove(a)
            #print("Remove " + a["name"])
            removed=True 
    
    if(a["userfields"]["restaurant"] == "1"):
        #print("removing")
        allrecipes.remove(a)
        removed=True   
    
    if(removed==False):
        url2 = mygrocy_url + "/api/objects/meal_plan?query%5B%5D=recipe_id%3D" + str(a["id"]) + "&order=day%3Adesc&limit=1"

        response2 = requests.request("GET", url2, headers=headers, verify=False)

        lasthad = ""
        for b in response2.json():
            #print("####{str(b[\"day\"])}")
            lasthad=b["day"]
        if (lasthad == ""):
            lasthad = date.today() - timedelta(days=len(allrecipes)+15)
    
    
        lastHadDateobj = datetime.strptime(str(lasthad), "%Y-%m-%d")    
        dayssince = (date.today() - lastHadDateobj.date()).days
        #print("Days Since:" + str(dayssince))
        recipeDict[a["id"]] = dayssince 


keys = list(recipeDict.keys())
vals = list(recipeDict.values())

for x in range(1):
    print("Iteration:" + str(x))
    picks = random.choices(keys,weights=vals,k=dinnerneedcount)
    #print(keys)
    #print(picks)
    for meh in allrecipes:
        
        if (meh["id"] in picks):
            print(meh["name"])

print(dinnerneedcount)
print(dinnerdaysneeddinner)
