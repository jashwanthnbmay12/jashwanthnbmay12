from jsonmerge import Merger

schema = {
    "properties": {
        "Response": {"mergeStrategy": "append"}
    }}
merger = Merger(schema)


def stepResponse(TaskJSon, stepsList):
    if 'StepID' in TaskJSon.keys():
        steps = {
            "StepID": TaskJSon['StepID'],
            "Response": TaskJSon['Response']
        }
        stepsList.append(steps)
        activities = {
            "ActivityID": TaskJSon['ActivityID'],
            "Steps": stepsList
        }
    else:
        activities = {
            "ActivityID": TaskJSon['ActivityID'],
            "Response": TaskJSon['Response'],
            "Steps": []
        }
    return activities


def checkResponse(resultJson, TaskJson):
    result = merger.merge(resultJson, TaskJson)
    return result


def getLatest(result):
    result['Response'] = result['Response'][-1]
    if result['Activities']:
        for activity in result['Activities']:
            activity['Response'] = activity['Response'][-1]
            if activity['Steps']:
                for steps in activity['Steps']:
                    steps['Response'] = steps['Response'][-1]
    return result
