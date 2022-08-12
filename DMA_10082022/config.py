import os

class DefaultConfig:
#-------------------------------------------------- MongoDB-----------------------------------------------------
#MongoDB requirements(cos-dma-mongo-001):
    CONNECTIONSTRING = os.environ.get("connectionstring", "mongodb://cos-dma-mongo-001:SEoeLj9KgoePNhXbEWRoKffGAUXSgiYtZxXMOMn63ukTsElqO1wbQ6dsmhGMHHocnArxd1WBZOeBA5B0UX0Zgg==@cos-dma-mongo-001.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cos-dma-mongo-001@")