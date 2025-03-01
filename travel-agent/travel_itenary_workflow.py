from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
from agno.utils.log import logger
from agno.workflow import Workflow
from agno.tools.tavily import TavilyTools
from textwrap import dedent
from agno.tools.serpapi import SerpApiTools

class ItenaryGeneratorWorkflow(Workflow):
    description: str = "Comprehensive Travel Itinerary Workflow"
    def __init__(self, api_key_llm:str,api_key_search_tool:str,search_tool=1):
        self.travel_query_generator: Agent = Agent(
            name="Travel Query Enhancer",
            description="Generates structured trip-specific queries",
            instructions=dedent("""\
                Your task is to create a **human-readable, structured query** based on the provided JSON input.
                
                **Key Requirements:**
                - Use clear and concise language
                - Include all provided parameters
                - Maintain the order of parameters as specified
                - Use proper date formatting (YYYY-MM-DD)
                - Specify currency for budget (USD)
                - Include all special requirements
                
                **Formatting Guidelines:**
                - Start with the trip type (e.g., "Holiday trip" or "Business trip")
                - Include origin and destination cities
                - Specify dates in "from [start_date] to [end_date]" format
                - Mention number of travelers
                - Include budget with currency symbol
                - Add special requirements as separate phrases
                
                **Detailed Parameter Handling:**
                - **Trip Type:** Capitalize (e.g., "Holiday" or "Business")
                - **Dates:** Use exact dates provided in ISO format
                - **Travelers:** Specify as "for [number] travelers"
                - **Budget:** Format as "Budget: $[amount]"
                - **Requirements:** Use phrases like "Requires [requirement]" or "Needs [requirement]"
                
                **Example Output Structure:**
                "[Trip Type] trip from [origin] to [destination] from [start_date] to [end_date] for [travelers] travelers. 
                Budget: $[budget]. Requires [requirement1] and [requirement2]."
                
                **Example 1 (Holiday):**
                "Holiday trip from New York to Paris from 2024-04-01 to 2024-04-05 for 2 travelers. 
                Budget: $5000. Requires family-friendly hotels and attractions. Needs souvenir shopping options."
                
                **Example 2 (Business):**
                "Business trip from London to Tokyo from 2024-05-10 to 2024-05-15 for 1 traveler. 
                Budget: $3000. Requires business hotels near conference centers. Needs after-work dining options."
                
                **Important Notes:**
                - Do not add any extra information beyond the provided parameters
                - Use exact phrasing from the JSON input for requirements
                - Ensure proper capitalization and punctuation
                - Maintain consistent formatting for all queries
            """),
            model=Groq(
                id="llama-3.3-70b-versatile",
                api_key=api_key_llm
            ),
            debug_mode=False,
            
            add_datetime_to_instructions = True
        )
        if search_tool == 1:
            searchTool =  TavilyTools(api_key=api_key_search_tool)
        else:
            searchTool =  SerpApiTools(api_key=api_key_search_tool)

        self.researcher = Agent(
            name="Travel Data Gatherer",
            description="Collects real-time travel data and local information",
            instructions=dedent("""\
                Your task is to collect comprehensive travel data using Tavily tools based on the trip type.
                
                **General Instructions:**
                - Always use the most up-to-date information available.
                - Prioritize accuracy and relevance of data.
                - Include prices in USD where applicable.
                - Provide specific names and addresses for locations.
                - Limit results to the top 3 options per category unless specified otherwise.

                **Common Tasks (All Trips):**
                1. **Flights:**
                - Find 3 flight options with:
                    - Airline name
                    - Departure/arrival times
                    - Price per adult/child
                    - Airport codes (origin/destination)
                    - Layover information (if applicable)
                - Prioritize non-stop flights where possible.

                2. **Hotels:**
                - Find 3 hotel options with:
                    - Hotel name
                    - Address
                    - Price per night (family room preferred)
                    - Rating (out of 5 stars)
                    - Distance from city center/airport
                    - Amenities (pool, Wi-Fi, breakfast, etc.)

                3. **Transportation:**
                - Find 3 transportation options between airport and city center:
                    - Option 1: Private transfer (provider, price, vehicle type)
                    - Option 2: Public transport (cost, duration, route)
                    - Option 3: Ride-sharing service (estimated cost, wait time)

                **Holiday/Family Trip Specific:**
                1. **Attractions:**
                - Find top 5 family-friendly attractions:
                    - Name
                    - Address
                    - Opening hours
                    - Ticket price (adult/child)
                    - Description (suitable for ages)

                2. **Shopping:**
                - Identify 3 popular souvenir shopping locations:
                    - Market name
                    - Address
                    - Operating hours
                    - Type of items sold

                3. **Dining:**
                - Find 5 kid-friendly restaurants:
                    - Restaurant name
                    - Address
                    - Average price per meal
                    - Specialties
                    - Kid-friendly features (play area, menu)

                **Business Trip Specific:**
                1. **Business Facilities:**
                - Locate 2 business centers near the destination:
                    - Name
                    - Address
                    - Services offered
                    - Operating hours

                2. **After-Work Activities:**
                - Find 3 nearby restaurants/bars:
                    - Name
                    - Address
                    - Cuisine type
                    - Price range
                    - Operating hours

                3. **Quick Shopping:**
                - Identify 2 souvenir shops near business areas:
                    - Shop name
                    - Address
                    - Operating hours
                    - Type of items sold

                **Output Format:**
                Return all data in a structured JSON format:
                {
                    "trip_type": "string",
                    "flights": [
                        {
                            "airline": "string",
                            "departure_time": "string",
                            "arrival_time": "string",
                            "price_adult": "float",
                            "price_child": "float",
                            "airport_origin": "string",
                            "airport_destination": "string",
                            "layovers": "int"
                        },
                        ...
                    ],
                    "hotels": [
                        {
                            "name": "string",
                            "address": "string",
                            "price_per_night": "float",
                            "rating": "float",
                            "distance_from_center": "string",
                            "amenities": ["string"]
                        },
                        ...
                    ],
                    "transportation": [
                        {
                            "type": "string",
                            "provider": "string",
                            "cost": "float",
                            "duration": "string"
                        },
                        ...
                    ],
                    "attractions": [
                        {
                            "name": "string",
                            "address": "string",
                            "hours": "string",
                            "price_adult": "float",
                            "price_child": "float",
                            "description": "string"
                        },
                        ...
                    ],
                    "shopping": [
                        {
                            "name": "string",
                            "address": "string",
                            "hours": "string",
                            "items_sold": "string"
                        },
                        ...
                    ],
                    "dining": [
                        {
                            "name": "string",
                            "address": "string",
                            "price_range": "string",
                            "specialties": "string",
                            "features": ["string"]
                        },
                        ...
                    ]
                }
            """),
            tools=[searchTool],
            model=Groq(
                id="llama-3.3-70b-versatile",
                api_key=api_key_llm
            ),
            debug_mode=False,
           
            add_datetime_to_instructions = True
        )

        self.travel_agent = Agent(
            name="Itinerary Compiler",
            description="Generates visually appealing markdown itinerary",
            instructions=dedent("""\
                Your mission is to create a **visually engaging and comprehensive markdown itinerary** using the provided structured data.
                
                **Key Requirements:**
                - Use professional markdown formatting with headers, tables, and bullet points.
                - Include all provided data points without adding extra information.
                - Use emojis and icons for better visual appeal.
                - Maintain consistent currency formatting (USD).
                - Provide clear section headings and subheadings.
                
                **Detailed Structure:**
                
                1. **Header Section:**
                - Use a bold title with destination and trip type.
                - Include a trip summary with bullet points:
                    - Trip type (e.g., "Family Holiday")
                    - Dates (start - end)
                    - Number of travelers (adults/children)
                    - Budget (USD)
                
                2. **Options Section:**
                - **Flights Table:**
                    - Columns: Airline, Price (Adult/Child), Details
                    - Include all 3 flight options
                - **Hotels Table:**
                    - Columns: Hotel, Price/Night, Amenities
                    - Include all 3 hotel options
                - **Transportation Table:**
                    - Columns: Option, Provider, Cost, Duration
                    - Include all 3 transportation options
                
                3. **Daily Schedule:**
                - Create a day-by-day schedule using time-stamped bullet points
                - Format:
                    - **Day 1 (Date):**
                    - 🚄 09:00 AM: Departure
                    - 🏨 11:00 AM: Hotel check-in
                    - 🎠 02:00 PM: Visit [Attraction Name]
                - Include activities based on trip type:
                    - Family/Holiday: Attractions, dining, shopping
                    - Business: Meetings, after-work activities
                
                4. **Additional Sections:**
                - **Shopping Tips:**
                    - Use bullet points with icons
                    - Include 2-3 shopping locations
                - **Dining Recommendations:**
                    - Use bullet points with icons
                    - Include 3-5 restaurant recommendations
                - **Important Tips:**
                    - Local transportation tips
                    - Cultural considerations
                    - Emergency contacts
                
                5. **Budget Breakdown:**
                - Create a table with costs for:
                    - Flights
                    - Accommodation
                    - Transportation
                    - Activities
                    - Total
                - Format: 
                    | Category       | Cost     |
                    |----------------|----------|
                    | Flights        | $XXX     |
                    | Accommodation  | $XXX     |
                    | Total          | $XXX     |
                
                **Formatting Guidelines:**
                - Use bold headers for main sections
                - Use emojis consistently:
                - ✈️ for flights
                - 🏨 for hotels
                - 🚗 for transportation
                - 🛍️ for shopping
                - 🍴 for dining
                - Use consistent currency formatting ($XXX)
                - Include a friendly closing message
                
                **Example Template:**
                ```markdown
                # **Paris Family Holiday Itinerary**
                ## Trip Summary
                - **Type:** Family Holiday
                - **Dates:** April 1 - April 5, 2024
                - **Travelers:** 2 Adults, 2 Children
                - **Budget:** $5,000

                ## Flight Options
                | Airline          | Price (Adult/Child) | Details                  |
                |------------------|---------------------|--------------------------|
                | Air France       | $800/$400           | Non-stop, 7AM departure  |
                | Delta Airlines   | $850/$425           | 1 layover in Amsterdam   |
                | American Airlines| $820/$410           | Free in-flight entertainment |

                ## Daily Schedule
                - **April 1 (Day 1):**
                - ✈️ 09:00 AM: Departure from New York
                - 🚗 11:00 AM: Private transfer to hotel
                - 🏨 12:00 PM: Check-in at Le Bristol Paris
                - 🎠 03:00 PM: Visit Eiffel Tower

                ## Shopping Tips
                - 🛍️ Visit Galeries Lafayette for luxury souvenirs
                - 🎨 Explore Marché aux Puces de Saint-Ouen for antiques

                ## Budget Breakdown
                | Category       | Cost     |
                |----------------|----------|
                | Flights        | $2,400   |
                | Accommodation  | $2,000   |
                | Total          | $4,400   |

                *All done! Have a wonderful trip! 🌍✈️*
                ```
                
                **Important Notes:**
                - Use the exact data provided in the input
                - Do not add any extra information or assumptions
                - Ensure all tables and sections are properly formatted
                - Use consistent emoji usage throughout the document
            """),
            model=Groq(
                id="llama-3.3-70b-versatile",
                api_key=api_key_llm
            ),
            markdown=True,
            debug_mode=False,
                
            add_datetime_to_instructions = True
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

