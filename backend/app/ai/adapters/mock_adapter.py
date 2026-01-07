from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()

class OpenAIAdapater:

    
        
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    res = client.responses.create(
        model="gpt-4.1-mini",
        input="Answer y if connections working"
    )

    print(res)