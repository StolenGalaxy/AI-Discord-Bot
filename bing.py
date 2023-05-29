from EdgeGPT import Query, ImageQuery
import shutil, os
from uuid import uuid4

def askBing(query, type):
    try:
        if type == "image":
            ImageQuery(query)
            
            generatedImages = []
            for file in os.listdir():
                if file.endswith(".jpeg"):
                    fileName = f"{uuid4()}.jpeg"
                    
                    os.rename(file, fileName)
                    shutil.move(fileName, "GeneratedImages")
                    
                    generatedImages.append(f"GeneratedImages\{fileName}")
            return generatedImages
                    
        elif type == "text":
            response = Query(query)
            return response
        
        elif type == "code":
            response = Query(query)
            return response.code
    except Exception as error:
        print()
    
print(askBing("Edinburgh", "image"))