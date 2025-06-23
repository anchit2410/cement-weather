from constant import OUTPUT_DIR, OUTPUT_FILENAME, SAMPLE_INPUT_FILENAME
# from .constant import OUTPUT_DIR, OUTPUT_FILENAME, SAMPLE_INPUT_FILENAME

def get_sample_file_path(base_path='samples'):
    import os
    try:
       
        _base_dir = os.path.join(os.getcwd(), base_path)
        file_path = os.path.join(_base_dir,SAMPLE_INPUT_FILENAME)
        return file_path
    
    except Exception as ex:
        raise Exception(f'No Sample File Exist')
    
def get_output_file_path():
    import os
    try:
        file_path = os.path.join(OUTPUT_DIR,OUTPUT_FILENAME)
        return file_path
    
    except Exception as ex:
        raise Exception(f'No Sample File Exist')