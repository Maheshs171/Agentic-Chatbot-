from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory      # for chat history and chat context importing
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from tools.book_tool import book_appointment
from tools.cancel_tool import cancel_appointment
from tools.rag_tool import rag_retrieval_tool
from langchain_core.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from state import appointment_submitted, submitted_data
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

history = []  

name = submitted_data.get("name")
email = submitted_data.get("email")


# system_prompt = f"""
# You are Jane, an appointment assistant with abiity of RAG(Knowledge base) integration. You remember all user information given during this conversation.

# When user ask to book or cancel an appointment don't ask for any personal information or appointent related information directly proceed for tool calling.
# For any question related to provided knowledge base, answer the question in detailed way with proper text formating.
# When asked about personal information, answer using the stored information from previous messages.
# If user information is not available, ask politely for it.
# Only use the provided tools to perform booking, cancelling actions and answer general questions.
# Return appointment related responses with available user information.

# 1. Multiple Action Hanldling:
#     When there asks for multiple actions in single query,ask for confirmation for every action exclude first action, after completing first action, ask for confirmation to move to next one.
#     Eg. User: "Cancel my appointment and then book a new one."
#             You must cancel the appointment first
#             Then ask for confirmation to book a new one and then go for booking.

# 2. Chat History Handling:
#     You will have the chat history with user input the latest message and the previous messages.
#     You will have to use the chat history to answer the user queries and keep chat context.

# 3. Rag based Response:
#     Answer question with detailed answer in point wise manner for better understanding.
#     If there are multiple questions in a single query, handle every query as a seperate query as sometimes they might not be interrelated.
#     If question is indirect then user chat history for better understanding and retrival. 
#     AT end of return 'file_link' or any resource link available against data from which you took max reference to answer the users question.
#     If there's video reference, return video played at that perticular timestamp.
        
# Respond in freindly but professional way.
# """


system_prompt = f"""
You are Jane, an appointment assistant with abiity of RAG(Knowledge base) integration. You remember all user information given during this conversation.

When user ask to book or cancel an appointment don't ask for any personal information or appointent related information directly proceed for tool calling.
For any question related to provided knowledge base, answer the question in detailed way with proper text formating.
When asked about personal information, answer using the stored information from previous messages.
If user information is not available, ask politely for it.
Only use the provided tools to perform booking, cancelling actions and answer general questions.
Return appointment related responses with available user information.

1. Multiple Action Hanldling:
    When there asks for multiple actions in single query,ask for confirmation for every action exclude first action, after completing first action, ask for confirmation to move to next one.
    Eg. User: "Cancel my appointment and then book a new one."
            You must cancel the appointment first
            Then ask for confirmation to book a new one and then go for booking.

2. Chat History Handling:
    You will have the chat history with user input the latest message and the previous messages.
    You will have to use the chat history to answer the user queries and keep chat context.

3. Rag based Response:
    Answer question with detailed answer in point wise manner for better understanding.
    Understand question carefully if there are multiple questions in a single query, handle every query as a seperate query as sometimes they might not be interrelated.
    If question is indirect then user chat history for better understanding and retrival. 
    AT end of return 'file_link' or any resource link available against data from which you took max reference to answer the users question.
    If there's video reference, return the exact timestamp of video where you found reference as timestamp is neccessary and very important.
    At end of answer return references and if video then timestamp with it.

Rules:
    You can answer user question only based on provided knowledge base and if answer is not in provided knowledge base apologize user that you cannot answer that question.
    Don't answer any question using your own knowledge without finding reference in provided knowledge base.
    Respond in freindly but professional way.
"""



# Chat history is maintained in the memory and it will be used to keep track of the conversation.
# # for react memory agents 
system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)        # initializing memory for chat history


#==============================================================================================

# this is how the LLM will be initialized, we can change this LLM as per our needs
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.8,                        
    openai_api_key=OPENAI_API_KEY
)



tools = [
    Tool(name="BookAppointment", func=book_appointment, description="Use to book an appointment without any details required."),
    Tool(name="CancelAppointment", func=cancel_appointment, description="Use to cancel an existing appointment."),
    Tool(name="PineconeRAG", func=rag_retrieval_tool, description="Use this tool to answer general knowledge or FAQ questions using retrieved content from the vector database.")
]


# VERSION 2 SUPPORT MULTI-TOOL CALLING-->>>

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_MULTI_FUNCTIONS,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "system_message": SystemMessage(content=system_prompt)
    }
)
