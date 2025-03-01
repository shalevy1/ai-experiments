from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
from agno.utils.log import logger
import json
from textwrap import dedent

class TripConversationAgent(Agent):
    def __init__(self, api_key):
        
        super().__init__(
            name="Conversational Trip Data Extractor",
            description="Have a conversation with the user about their trip to extract their trip requirements in a structured format.",
            model=Groq(
                id="llama-3.3-70b-versatile",
                api_key=api_key
            ),
          
            
            instructions=dedent("""\
                Your task is to extract trip details from the user's query.
                - Identify the following parameters: trip_type, origin, destination, dates, travelers, accommodation,budget,requirements
                - The origin and destination should be a city.
                - If any parameter is missing, note it as null.
                - Return a structured JSON response with the extracted parameters and a message within the json asking for missing information in a conversational manner.
                - The retuned JSON should only have the follwing keys trip_type, origin, destination, dates,accommodation, travelers,budget,requirements, message. No extra keys should be added and None should be assigned to keys if they do not have a value
                - The dates key should be always in this format "dates": {"start_date": "2024-04-01", "end_date": "2024-04-05"}
                - Make sure to always add a message key to the output JSON
                - Respond only with a valid JSON do not add any extra information like json or ```
            """
            )
            
        )
        self.finalParams = {
            "trip_type": None,
            "origin": None,
            "destination": None,
            "dates": None,
            "travelers": None,
            "accommodation": None,
            "budget": None,
            "requirements": None
            
            
        }
       
        self.suffix = ""

    
    def __process_tripdata(self,params_llm):
        
       
        
        logger.info(f"Final params before -- items: {self.finalParams}")
        logger.info(f"Parama -- items: {params_llm}")
        missing = []
        if not self.finalParams["trip_type"]:
            if params_llm["trip_type"]:
                self.finalParams["trip_type"] = params_llm["trip_type"]
            else:
                missing.append("trip_type")
                
        if not self.finalParams["origin"]:
            if params_llm["origin"]:
                self.finalParams["origin"] = params_llm["origin"]
            else:
                missing.append("origin")
                
        if not self.finalParams["destination"]:
            if params_llm["destination"]:
                self.finalParams["destination"] = params_llm["destination"]
            else:
                missing.append("destination")
                
        if not self.finalParams["dates"]:
            if params_llm["dates"]:
                try:
                    if params_llm["dates"]["start_date"] and params_llm["dates"]["end_date"]:
                        self.finalParams["dates"] = params_llm["dates"]
                except:
                    pass
                
            else:
                missing.append("dates")
                
        if not self.finalParams["travelers"]:
            if params_llm["travelers"]:
                self.finalParams["travelers"] = params_llm["travelers"]
            else:
                missing.append("travelers")
                
        if not self.finalParams["accommodation"]:
            if params_llm["accommodation"]:
                self.finalParams["accommodation"] = params_llm["accommodation"]
            else:
                missing.append("accommodation")
                
        if not self.finalParams["budget"]:
            if params_llm["budget"]:
                self.finalParams["budget"] = params_llm["budget"]
            else:
                missing.append("budget")
                
        if not self.finalParams["requirements"]:
            if params_llm["requirements"]:
                self.finalParams["requirements"] = params_llm["requirements"]
            else:
                missing.append("requirements")
        
        logger.info(f"missing -- items: {missing}")
        logger.info(f"Final params After -- items: {self.finalParams}")
        logger.info("__________________________\n-------------------------------------")
        
        if missing:
            missing_params = ", ".join(missing)
            return {"user_message":f"Please provide the follwing missing params which are required  : {missing_params}.",
                    "query_suffix":f"Identify the following parameters: {missing_params}.","missing":True}
        else:
            return {"user_message":"Thank you! Planning your trip..",
                    "query_suffix":"",
                    "missing":False}
            
    def reset(self):
        self.finalParams = {
            "trip_type": None,
            "origin": None,
            "destination": None,
            "dates": None,
            "travelers": None,
            "accommodation": None,
            "budget": None,
            "requirements": None
            
            
        }
       
        self.suffix = ""

        

    def process_query(self, query):
        
       
        if len(self.suffix) == 0:
            final_query = query+" Identify the following parameters: trip_type, origin, destination, dates, travelers."
        else:
            final_query = query+" "+self.suffix
            
        logger.info(f"final_query------------------------: {final_query}")
        response: RunResponse = self.run(final_query)
        
        """Only in case of deepseek"""
        cleaned  = response.content.split("</think>")
        if len(cleaned) > 1:
            modified = cleaned[1].replace("```json", "")
        else:
            modified = cleaned[0].replace("```json", "")
        modified = modified.replace("```", "")
        
        params = json.loads(modified)
        
        result = self.__process_tripdata(params)
        self.suffix = result["query_suffix"]
        user_message = result["user_message"]
        have_further_conversation = result["missing"]
        
    
        if not params["message"] or not have_further_conversation:
            return {"message":user_message,"have_further_conversation":have_further_conversation,'data':self.finalParams}
            
        else:
            return {"message":params["message"],"have_further_conversation":have_further_conversation,'data':self.finalParams}
       