from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
from agno.utils.log import logger
from agno.workflow import Workflow
from agno.tools.tavily import TavilyTools
from textwrap import dedent

class ItenaryGeneratorWorkflow(Workflow):
    description: str = "Comprehensive Travel Itinerary Workflow"
    def __init__(self, api_key_llm:str,api_key_tavily:str):
        self.travel_query_generator: Agent = Agent(
            name="Travel Query Enhancer",
            description="Generates structured trip-specific queries",
            instructions=dedent("""\
                You will be given a structured json with the follwing keys trip_type, origin, destination, dates,accommodation, travelers,budget,requirements
                Create a structured query from the structured json input including:
                - Trip type (holiday/business)
                - Origin/Destination
                - Dates
                - Travelers
                - Accomodation
                - Budget
                - Special requirements (family-friendly, business focus)
                
                Example Output:
                "Holiday trip from New York to Paris from 2024-04-01 to 2024-04-05 for 2 travelers. 
                Budget: $5000. Requires family-friendly hotels and attractions. Needs souvenir shopping options."
            """),
            model=Groq(
                id="llama-3.3-70b-versatile",
                api_key=api_key_llm
            ),
            debug_mode=False,
        )

        self.researcher = Agent(
            name="Travel Data Gatherer",
            description="Collects real-time travel data and local information",
            instructions=dedent("""\
                Based on the trip type, perform the following:
                
                1. **Common Tasks**:
                    - Find 3 flight options with prices and timings.
                    - Find 3 hotel options with prices, ratings, and locations.
                    - Find 3 transportation options (taxis, trains, etc.) with costs.
                
                2. **Holiday/Family Trip**:
                    - Search for top 5 family-friendly attractions.
                    - Find local markets/shopping areas for souvenirs.
                    - Identify popular restaurants for local cuisine.
                
                3. **Business Trip**:
                    - Locate business centers and conference venues.
                    - Find after-work activity options (restaurants, bars).
                    - Identify nearby souvenir shops for quick purchases.
                
                Return structured data in JSON format:
                {
                    "flights": [...],
                    "hotels": [...],
                    "transportation": [...],
                    "attractions": [...],
                    "shopping": [...],
                    "dining": [...]
                }
            """),
            tools=[TavilyTools(api_key=api_key_tavily)],
            model=Groq(
                id="llama-3.3-70b-versatile",
                api_key=api_key_llm
            ),
            debug_mode=False,
        )

        self.travel_agent = Agent(
            name="Itinerary Compiler",
            description="Generates visually appealing markdown itinerary",
            instructions=dedent("""\
                Your mission is to craft a **content-rich markdown itinerary** using structured data.
                
                1. **Header**:
                - Start with a bold title and trip summary in bullet points.
                
                2. **Options Section**:
                - Format flights, hotels, and transportation as markdown tables.
                
                3. **Daily Schedule**:
                - List each day's activities using time-stamped bullet points.
                
                4. **Additional Sections**:
                - Use icons and bullet points for tips, dining, and shopping.
                
                Use the following template to ensure consistent formatting:
                
                ```markdown
                # {Destination} Itinerary
                ## Trip Summary
                - **Type:** {trip_type}
                - **Dates:** {start_date} - {end_date}
                - **Travelers:** {adults} adult(s), {children} child(ren)
                - **Budget:** ${budget}
                
                ## Flight Options
                | Airline          | Price (Adult/Child) | Details                  |
                |------------------|---------------------|--------------------------|
                | {flight1_name}   | ${flight1_price_A}/${flight1_price_C} | {flight1_details} |
                | {flight2_name}   | ${flight2_price_A}/${flight2_price_C} | {flight2_details} |
                | {flight3_name}   | ${flight3_price_A}/${flight3_price_C} | {flight3_details} |
                
                ## Hotel Options
                | Hotel                | Price/Night | Amenities |
                |----------------------|-------------|-----------|
                | {hotel1_name}        | ${hotel1_price} | {hotel1_amenities} |
                | {hotel2_name}        | ${hotel2_price} | {hotel2_amenities} |
                | {hotel3_name}        | ${hotel3_price} | {hotel3_amenities} |
                
                ## Daily Schedule
                - **{start_date}**:
                - 🚄 09:00 AM: Departure
                - 🛒 11:00 AM: Shopping at {shopping1}
                - 🍴 13:00 PM: Lunch at {restaurant1}
                
                ## Shopping & Dining
                - *Shopping:* {shopping_tip1}, {shopping_tip2}
                
                ## Budget Breakdown
                - Flights: ${flights_total}
                - Accommodation: ${hotels_total}
                - Transportation: ${transport_total}
                - Total: ${total_cost}
                
                *All done!*
                ```
                
                Follow the template closely, replacing placeholders with relevant data. Use dollars for currencies and include emojis for visual clarity.
            """),
            model=Groq(
                id="llama-3.3-70b-versatile",
                api_key=api_key_llm
            ),
            markdown=True,
            debug_mode=False,
        )
        
    def __generate_trip_query(self,queryJSON):                                                                                                                                                                                                                                                                                                 
            
        query = f"""I want to plan a {queryJSON['trip_type']} trip from {queryJSON['origin']} to {queryJSON['destination']} 
                      from {queryJSON['dates']['start_date']} to {queryJSON['dates']['end_date']} 
                      for {queryJSON['travelers']} travelers. Budget: {queryJSON['budget']}.
                      Needs: {queryJSON['requirements']}.
                      Budget: {queryJSON['budget']}.
                      Please include multiple options for flights, accomodation, and transportation."""                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        return query          

    def run(self, payload: str) -> RunResponse:
        
        raw_query = self.__generate_trip_query(payload)
        
        # Step 1: Generate enhanced query
        enhanced_query = self.travel_query_generator.run(raw_query)
        logger.info(f"Enhanced Query: {enhanced_query.content}")

        # Step 2: Collect travel data
        data = self.researcher.run(enhanced_query.content)
        logger.info(f"Collected Data: {data.content}")

        # # Step 3: Generate itinerary
        itinerary = self.travel_agent.run(data.content)
        return itinerary

if __name__ == "__main__":
    workflow = ItenaryGeneratorWorkflow(api_key_llm="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",api_key_tavily='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') 
    queryJSON = {
        "trip_type": "Business",
        "origin": "New York",
        "destination": "Paris",
        "dates": {"start_date": "2024-04-01", "end_date": "2024-04-05"},
        "travelers": 2,
        "budget": "$5000",
        "requirements": "business hotels, attractions, souvenir shopping"
    }
    input_payload = f"""I want to plan a {queryJSON['trip_type']} trip from {queryJSON['origin']} to {queryJSON['destination']} 
                      from {queryJSON['dates']['start_date']} to {queryJSON['dates']['end_date']} 
                      for {queryJSON['travelers']} travelers. Budget: {queryJSON['budget']}.
                      Needs: {queryJSON['requirements']}.
                      Please include multiple options for flights, hotels, and transportation."""
    response = workflow.run(payload=queryJSON)
    logger.info(response)