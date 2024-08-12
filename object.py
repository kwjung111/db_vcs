import os

class DB_Object:
    WORKSPACE="./workspace"
    def __init__(self,query_res,branch,dir):
        self.__query_results=query_res
        self.__branch=branch
        self.__dir=dir
        
    def get_query_results(self):
        return self.__query_results
    
    def get_branch(self):
        return self.__branch
    
    def get_dir(self):
        return self.__dir
    
    def get_path(self):
        return os.path.join(DB_Object.WORKSPACE,self.__branch,self.__dir)
    
