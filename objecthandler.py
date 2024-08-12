import os
from object import DB_Object
from logger import logger
from concurrent.futures import ThreadPoolExecutor


class Object_handler:
    @staticmethod
    def save_to_file(obj, path):
        file_name = obj['FILE_NAME']
        try:
            file_path= os.path.join(path,f"{file_name}.yml")
            
            with open(file_path,'w',encoding='UTF-8') as file:
                for key, value in obj.items():
                    # key-value 쌍을 "key: value" 형식으로 작성
                    if key == 'CONTENT':
                        file.write(f"{key}:\n{value}\n")
                    else:
                        file.write(f"{key}: {value}\n")
                file.write("\n")  # 각 객체 사이에 공백 줄 추가
        except Exception as e :
            logger.debug(f"Error: {e}")
        
    @staticmethod        
    def save_all_to_file(db_obj: DB_Object):
        query_results = db_obj.get_query_results()
        path = db_obj.get_path()
        if not os.path.exists(path):
            os.makedirs(path)
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(Object_handler.save_to_file,obj,path) for obj in query_results]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error in threaded exectuion: {e}")
                    
