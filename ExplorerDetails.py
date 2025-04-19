import os

# Set the API key before any other imports
os.environ["GROQ_API_KEY"] = "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"

# Now import necessary modules
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.baidusearch import BaiduSearch


def create_esg_crawler():
    
    
    

    # Création de l'agent avec le modèle et les outils
    agent = Agent(model=Groq(id="llama-3.1-8b-instant"),
              #tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)]
                tools=[BaiduSearch()],
                 description="You are a search agent that helps users find the most relevant information about blockchain decentralization metrics of Layer 1 blockchains using Baidu to later use them for ranking Layer 1 blockchains")
    

    # Construction de la requête
    query = f"""
  extract structured information on the decentralization of 5ire . Focus on key decentralization metrics.
    """
    
    return agent.print_response(query)

# Exécuter le crawler
if __name__ == "__main__":
    create_esg_crawler()
