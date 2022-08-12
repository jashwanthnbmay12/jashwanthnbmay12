from flask import Flask, request
from dmatables import Signin, TaskOperations, VMIOperations, TaskFeedback

app = Flask(__name__)


@app.route("/getUser", methods=['POST', 'GET'])
def getuser():
    try:
        username = request.json['username']
        password = request.json['password']
        profile = Signin(username, password)
        user = profile.getUserProfile()
        return user
    except Exception as e:
        print("Encountered exception. {0}".format(e))


@app.route("/getTask", methods=['POST', 'GET'])
def gettask():
    try:
        user = request.json['fname']
        Task = TaskOperations(user)
        tasklist = Task.taskList()
        return tasklist
    except Exception as e:
        print("Encountered exception. {0}".format(e))


@app.route("/PostFeedback", methods=['POST', 'GET'])
def postfeedback():
    try:
        feedbackJson = request.json
        feedbackList = TaskFeedback(feedbackJson)
        feedbackDetails = feedbackList.feedback()
        return feedbackDetails
    except Exception as e:
        print("Encountered exception. {0}".format(e))


@app.route("/getVMI", methods=['POST', 'GET'])
def getvmi():
    try:
        TASKID = request.json['TASKID']
        VMI = request.json['VMI']
        activityList = VMIOperations(TASKID, VMI)
        vmiDetails = activityList.vmiDetails()
        return vmiDetails
    except Exception as e:
        print("Encountered exception. {0}".format(e))


@app.route("/GetFeedback", methods=['POST', 'GET'])
def feedback():
    try:
        feedbackJson = request.json
        feedbackList = TaskFeedback(feedbackJson)
        feedbackDetails = feedbackList.getfeedback()
        return feedbackDetails
    except Exception as e:
        print("Encountered exception. {0}".format(e))


if __name__ == '__main__':
    app.run()
