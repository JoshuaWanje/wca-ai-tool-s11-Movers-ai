# NAMES
1.Victor Ngundo
2.Joshua Wanje
3.Elisha Kibichii
4.Nevyl Cherop
5.Susan Odinga

# ABOUT THE TOOL
 It is an AI-driven Conversational Booking Engine specifically architected for a moving company operating in the regions of Kenya

 
 # WHAT THE TOOL DOES
Instead of forcing users to fill out long, rigid contact forms, this tool uses a Large Language Model (LLM) to extract information through natural, friendly conversation. Here is exactly what happens under the hood when a customer interacts with it:


**1. Conversational Extraction (AI Layer)**
   Natural Dialogue: The chatbot starts a friendly conversation using an embedded specialized persona.
   Context Tracking: It monitors the chat history to pick up four specific parameters: Origin town, Destination town, House size (Bedsitter to 4B),      and Sofa seat count.
   Strict Guardrails: If a user mentions moving somewhere outside the  service zone (like Mombasa, Nakuru, or Eldoret), the AI immediately flags it      and declines the job to keep your operations focused locally.

   
**2. Autonomous Function Execution (The Bridge)**
   Open AI Function Calling: The moment the AI extracts all four pieces of information, it stops asking questions
   It automatically triggers the calculate_moving_quote Python function behind the scenes, bridging the gap between conversational text and math. [1]

   
**3.Regional  Spatial Mapping**
   The tool maintains a hardcoded geographic grid of major  Region logistics hubs (Kiambu,Nairobi City ).
   It passes the locations into the Haversine formula to compute the distance between the two towns, applying a 1.3× scale factor to accurately. **4.Transparent Price Computation **
The backend pipes the variables into a structured rate card formula to generate a quote in Kenyan Shillings (KSh):
    Base Truck Rate: Determined by house volume (Bedsitter = KSh 3,500 up to 4B = KSh 18,000) to account for vehicle size.
    Seat Surcharge: KSh 300 per seat to cover extra crew loaders and specialized transit wrapping materials.
    Fuel Fee: KSh 150 per calculated kilometer to offset fuel consumption and emDistance pty return trips.

    
**5. Automated CRM Storage & Response**
Persistent CSV Logging: The script instantly commits the client's information, timestamp, and calculated price to a running central,nairobi_movers_leads.csv spreadsheet on the  server for the dispatch team.
Clean Formatting: Finally, it loops back to the user with a nicely formatted, broken-down price estimation message, asking if they would like to lock in a booking.



  
     
 
