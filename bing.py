from EdgeGPT import Query, ImageQuery
import shutil, os
from uuid import uuid4

def askBing(query, type):
    if type == "image":
        try:
            #ImageQuery(query)
            Query(query, style="image")
            
            generatedImages = []
            for file in os.listdir():
                if file.endswith(".jpeg"):
                    fileName = f"{uuid4()}.jpeg"
                    
                    os.rename(file, fileName) 
                    shutil.move(fileName, "GeneratedImages")
                    
                    generatedImages.append(f"GeneratedImages\{fileName}")
            return generatedImages
        except:
            return "ERROR"
                
    elif type == "text":
        response = str(Query(query, "creative"))
        print("Sending command:", response)
        return response
    
    elif type == "code":
        response = str(Query(query, "creative").code)
        print("Sending command:", response)
        return response
