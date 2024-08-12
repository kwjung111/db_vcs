import objecthandler
from db import Database
from config import Config,Mode
from object import DB_Object
from logger import logger
from gitManager import git_manager

if __name__=="__main__":
    
    logger.info('started')
    conf = Config()
    mode = conf.get_mode()
    db = Database(conf)
    connections = db.connect_all()
    
    oj_handler = objecthandler.Object_handler
    gm = git_manager(conf)
         
    trigger_sql = """
                   SELECT CONCAT(ist.TRIGGER_SCHEMA, '.',ist.TRIGGER_NAME) as FILE_NAME 
                   ,ist.TRIGGER_NAME
                   ,ist.EVENT_MANIPULATION
                   ,ist.ACTION_TIMING
                   ,ist.DEFINER
                   ,ist.CREATED
                   ,ist.TRIGGER_SCHEMA 
                   ,ist.EVENT_OBJECT_SCHEMA
                   ,ist.EVENT_OBJECT_TABLE
                   ,ist.ACTION_STATEMENT AS CONTENT
                   ,ist.SQL_MODE
                   ,ist.ACTION_ORIENTATION
                   ,ist.ACTION_REFERENCE_OLD_ROW
                   ,ist.ACTION_REFERENCE_NEW_ROW
                   from information_schema.triggers ist
                   """
    
    procedure_sql = """
                    SELECT 
                    CONCAT(isr.ROUTINE_SCHEMA ,'.',isr.ROUTINE_NAME) AS FILE_NAME
                    ,isr.ROUTINE_NAME
                    ,isr.ROUTINE_TYPE
                    ,isr.DEFINER 
                    ,isr.CREATED 
                    ,isr.LAST_ALTERED 
                    ,isr.ROUTINE_DEFINITION AS CONTENT
                    ,isr.SQL_MODE 
                    ,isr.IS_DETERMINISTIC 
                    ,isr.SQL_DATA_ACCESS 
                     FROM information_schema.routines isr
                    """
    
    if mode == Mode.WHEN_ALTERED:
        interval_days = conf.get_interval_days()
        trigger_sql   += f"WHERE CREATED >= date_sub( curdate(),INTERVAL {interval_days} day)"
        procedure_sql += f"WHERE LAST_ALTERED >= date_sub( curdate(),INTERVAL {interval_days} day)"
    
    for system,conn in connections.items():
        
        triggers = DB_Object(db.read(conn,trigger_sql),system, "triggers")
        procedures = DB_Object(db.read(conn,procedure_sql),system, "procedures")
    
        oj_handler.save_all_to_file(triggers)
        oj_handler.save_all_to_file(procedures)
        
    
    gm.commit_and_push()
    #gm.clean()
    logger.info('fin')