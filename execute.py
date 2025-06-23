# from .models.apl_coal import execute_code
import os
from models.weather_forecast import execute_code
from io import BytesIO
import pandas as pd
# from .utills import get_output_file_path
from utills import get_output_file_path


import logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def save_result_to_result_file(result_data:dict):
    LOGGER.info(f"save_result_to_result_file run successfully")
    
    _output_file_path = get_output_file_path()
    df_new = pd.DataFrame(result_data)
    

    if os.path.exists(_output_file_path):
        df_old = pd.read_excel(_output_file_path)

        df_merge = pd.merge(df_new,df_old[["date","rain_sum","County/District"]],how="left",on=["date","County/District"],suffixes=("_new","_old"))
        # print(df_merge)
        # df_combined = pd.concat([df_old,df_new], ignore_index=True)
        
        # df_combined.drop_duplicates(subset=["Lat","Long","County/District", "date"], keep='last', inplace=True)
        
        # print(df_combined)
        # print('>>>>>>>>>>>>>>>>>>')
        

        df_merge["rain_sum_new"]=df_merge.apply(lambda row: row["rain_sum_old"] if pd.isna(row["rain_sum_new"]) else row["rain_sum_new"], axis=1)


        # df_combined["rain_sum"] = df_combined["rain_sum"].combine_first(df_combined["rain_sum_old"])
        

        df_merge.drop( columns=["rain_sum_old"] ,inplace=True)
        df_merge.rename(columns={"rain_sum_new": "rain_sum"}, inplace=True)

    
    else:
        df_merge = df_new
    
    
    df_merge.sort_values(by=["County/District", "date"], inplace=True)
    with pd.ExcelWriter(_output_file_path) as writer:
        # df = pd.DataFrame(result_data)
        df_merge.to_excel(writer, sheet_name="Sheet1", index=False)
        LOGGER.info(f"result file save at location {_output_file_path}")
   
def run(data: dict):

    result_dict = execute_code(data)
    LOGGER.info(f"model executed successfully")

    save_result_to_result_file(result_dict)
    LOGGER.info(f"model result save successfully")

    return {
        "code": 200,
        "message": "Job created and results saved successfully."
    }
