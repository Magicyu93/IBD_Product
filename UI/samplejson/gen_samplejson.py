from langchain_core.prompts import PromptTemplate
from langchain import OpenAI
import yfinance as yf # source

API_KEY = os.getenv('OPENAI_API_KEY')
llm = OpenAI(openai_api_key=API_KEY)


def generate_sample_json(ticker):
    prompt_template = """
    I have a list of questions about a company identified by the stock ticker {TICKER}. 
    
    Please answer each question in the following format, returning only the question and the answer as plain text in Markdown style. 
    Ensure there is no extra text beyond this format.
    
    Example Format: **Question: What is the company's market cap?**
    Answer: $150 billion
    
    Please generate at least three sentences for question if it is not answered in one word.
    Please replace the ticker with the company name if it appears in the Answer.
    Please do not come up with questions not provided below
    
    Here is my questions: {question}.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    
    
    questions = ['what does the company do', 
                 'when was the company founded',
                 'what are their key products',
                 'what is there monetization model',
                 'who is their target customer',
                 'Any marquee customer logos?',
                 'who owns them?'
                ]

    allresponse = []
    for question in questions:
        chain = prompt | llm
        response = chain.invoke({"TICKER": ticker , "question": question})
        allresponse.append(response)

    jsondct = {}
    
    jsondct['overview'] = '\n'.join(allresponse)
    jsondct['financials'] = ticker
    
    
    stock = yf.Ticker(ticker)
    list_news = stock.news
    response = llm.invoke(f"what's in the news in url:{list_news[0]['link']}, title: {list_news[0]['title']}")
    jsondct['news'] = response
    
    with open(f'{ticker}.json', 'w') as jsfile:
        json.dump(jsondct, jsfile)
