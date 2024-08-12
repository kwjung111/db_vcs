import git
import os
from logger import logger
from config import Config
from datetime import datetime
import shutil

class git_manager:
    REPO_PATH= "./workspace"
    
    def __init__(self,conf: Config ):
        self.__conf = conf
        repository = conf.get_repository()
        url=repository['url']
        username=repository['username']
        password=repository['password']
        
        self.__remote_url=f"https://{username}:{password}@{url}"
    
        if not os.path.exists(self.REPO_PATH):
            os.makedirs(self.REPO_PATH)
        else:
            shutil.rmtree(self.REPO_PATH)
            os.makedirs(self.REPO_PATH)
            
        #not init-pull, just clone
        self.__repo = git.Repo.clone_from(self.__remote_url,self.REPO_PATH)
        
    def commit(self,msg="default commit msg"):
        repo = self.__repo
        mode = self.__conf.get_mode()
        today = datetime.now().date()
        msg = f"date : {today} , mode : {mode}"

        repo.git.add(A=True)
        if repo.is_dirty(untracked_files=True):
            repo.index.commit(f"{msg}")
            logger.info(f"{msg}")
            return True
        else:
            logger.info("no changes to commit")
            return False
        
    def push(self):
        repo = self.__repo
        origin= repo.remote(name='origin')
        origin.push()
        
        
    def commit_and_push(self):
        if self.commit():
            #self.push()
            pass 
            
    def clean(self):
        if os.path.exists(self.REPO_PATH):
            shutil.rmtree(self.REPO_PATH)