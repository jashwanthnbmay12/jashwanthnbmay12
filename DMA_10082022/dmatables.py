import pymongo
import pandas as pd
import json
from feedbacksync import *
import datetime

client = pymongo.MongoClient("localhost", 27017)
db = client.DMA


class Signin(object):
    try:
        def __init__(self, Username, Password):
            self.Username = Username
            self.Password = Password

        def getUserProfile(self):
            try:
                user_collection = db.userProfile
                user = user_collection.find_one({"Username": self.Username, "Password": self.Password}, {"_id": 0})
                if user:
                    message = user
                else:
                    message = json.dumps({'message': "Login denied"})
                return message
            except Exception as e:
                print("Encountered exception. {0}".format(e))
    except Exception as e:
        print("Encountered exception. {0}".format(e))


class TaskOperations(object):
    try:
        def __init__(self, user):
            self.user = user

        def taskList(self):
            try:
                task_collection = db.taskList
                task = task_collection.find({"User": self.user}, {"_id": 0})
                df = pd.DataFrame(task)
                task_list = df.to_dict('records')
                result = json.dumps({"taskList": task_list})
                return result
            except Exception as e:
                print("Encountered exception. {0}".format(e))
    except Exception as e:
        print("Encountered exception. {0}".format(e))


class VMIOperations(object):
    def __init__(self, TaskID, VMI):
        self.TaskID = TaskID
        self.VMI = VMI

    def vmiDetails(self):
        try:
            vmi_collection = db.VMI
            vmi_data = vmi_collection.find_one({"$text": {"$search": self.VMI}}, {"_id": 0})
            vmi_data['TaskID'] = self.TaskID
            if vmi_data:
                return vmi_data
            else:
                message = json.dumps({'message': "No VMI Found"})
                return message
        except Exception as e:
            print("Encountered exception. {0}".format(e))


class TaskFeedback(object):
    def __init__(self, TaskJSon):
        self.response = {}
        self.TaskJSon = TaskJSon
        self.collection = db.Feedback

    def feedback(self):
        self.TaskJSon['Response']['TimeStamp'] = datetime.datetime.now()
        self.TaskJSon['Response'] = [self.TaskJSon['Response']]
        try:
            result = self.collection.find_one({"Man": self.TaskJSon['Man'], "TaskID": self.TaskJSon['TaskID'],
                                               "WorkOrderNo": self.TaskJSon['WorkOrderNo']})
            if result:
                if 'ActivityID' in self.TaskJSon.keys():
                    condition = {"ActivityID": self.TaskJSon['ActivityID']}
                    activityList = [d for d in result['Activities'] if
                                    all(k in d and d[k] == v for k, v in condition.items())]
                    if activityList:
                        for activity in activityList:
                            if 'StepID' in self.TaskJSon.keys():
                                condition = {"StepID": self.TaskJSon['StepID']}
                                StepList = [d for d in activity['Steps'] if
                                            all(k in d and d[k] == v for k, v in condition.items())]
                                if StepList:
                                    for Step in StepList:
                                        UpdatedResponse = checkResponse(Step, self.TaskJSon)
                                        Step['Response'] = UpdatedResponse['Response']
                                        # activity['Steps'] = [steps]
                                else:
                                    print('enter')
                                    steps = {
                                        "StepID": self.TaskJSon['StepID'],
                                        "Response": self.TaskJSon['Response']
                                    }
                                    activity['Steps'].append(steps)
                            else:
                                if 'Response' in activity.keys():
                                    UpdatedResponse = checkResponse(activity, self.TaskJSon)
                                    activity['Response'] = UpdatedResponse['Response']
                                else:
                                    activity['Response'] = self.TaskJSon['Response']

                    else:
                        stepsList = []
                        self.response['Man'] = self.TaskJSon['Man']
                        self.response['TaskID'] = self.TaskJSon['TaskID']
                        self.response['WorkOrderNo'] = self.TaskJSon['WorkOrderNo']
                        if 'ActivityID' in self.TaskJSon.keys():
                            activities = stepResponse(self.TaskJSon, stepsList)
                        result['Activities'].append(activities)
                else:
                    if 'Response' in result.keys():
                        UpdatedResponse = checkResponse(result, self.TaskJSon)
                        result['Response'] = UpdatedResponse['Response']
                    else:
                        result['Response'] = self.TaskJSon['Response']

                result = self.collection.update_one(
                    {"_id": result['_id']},
                    {
                        "$set": result
                    },

                    upsert=True
                )
            else:
                activityList = []
                stepsList = []
                self.response['Man'] = self.TaskJSon['Man']
                self.response['TaskID'] = self.TaskJSon['TaskID']
                self.response['WorkOrderNo'] = self.TaskJSon['WorkOrderNo']
                if 'ActivityID' in self.TaskJSon.keys():
                    activities = stepResponse(self.TaskJSon, stepsList)
                    activityList.append(activities)
                    self.response['Activities'] = activityList
                else:
                    self.response['Response'] = self.TaskJSon['Response']
                    self.response['Activities'] = activityList
                result = self.collection.insert_one(self.response)
            message = json.dumps({'message': "Feedback submitted successfully"})
        except Exception as e:
            print("Encountered exception. {0}".format(e))
            message = json.dumps({'message': "Encountered exception. {0}".format(e)})
        return message

    def getfeedback(self):
        try:
            result = self.collection.find_one({"Man": self.TaskJSon['Man'], "TaskID": self.TaskJSon['TaskID'],
                                               "WorkOrderNo": self.TaskJSon['WorkOrderNo']},
                                              {"_id": 0})
            if result:
                result = getLatest(result)
                message = result
            else:
                message = json.dumps({'message': "Feedback not found"})
            return message
        except Exception as e:
            print("Encountered exception. {0}".format(e))
            message = json.dumps({'message': "Encountered exception. {0}".format(e)})
            return message
