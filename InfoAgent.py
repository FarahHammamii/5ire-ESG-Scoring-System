import os
import json


os.environ["GROQ_API_KEY"] = "enter key here"

from phi.agent import Agent
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.model.groq import Groq


def create_esg_crawler():
    agent = Agent(model=Groq(id='deepseek-r1-distill-llama-70b'),
                  tools=[Crawl4aiTools(max_length=None)])

    esg_keywords = [
        "ESG", "sustainability", "environmental", "social", "governance", "ethics",
        "impact", "carbon footprint", "sustainable development", "social responsibility",
        "renewable energy", "energy consumption", "green blockchain", "proof of stake",
        "proof of work", "consensus mechanism", "carbon neutral", "community", "engagement",
        "transparency", "decentralization", "security", "audit", "negative news",
        "controversy", "criticism", "environmental impact assessment", "SDG", "UN goals"
    ]

    query = f"""
Analyze the website https://www.5ire.org and extract the following information for an ESG and sustainability assessment:

**Core ESG & Sustainability Information:**

1.  **Consensus Mechanism:** Identify the consensus mechanism used (e.g., Proof-of-Stake, Proof-of-Work).  Describe how this mechanism impacts energy consumption and environmental sustainability.
2.  **Sustainability Strategy:** Detail the blockchain's overall sustainability strategy, including any stated goals for carbon neutrality or reducing environmental impact.  Include specific initiatives and targets.
3.  **Carbon Neutrality Efforts:** If applicable, describe any specific plans or actions taken towards achieving carbon neutrality. Include details on carbon offsetting programs, renewable energy usage, or other mitigation strategies.
4.  **Environmental Impact Assessment:**  Search for any published environmental impact assessments or reports related to the blockchain's operations. Summarize findings.
5.  **Community Engagement (Sustainability):** Describe any community engagement activities related to sustainability, environmental responsibility, or related social impact initiatives.
6.  **Alignment with SDGs:**  Identify any explicit mentions of the UN Sustainable Development Goals (SDGs) and how the blockchain's activities contribute to these goals.

**Governance & Social Responsibility:**

7.  **Governance Model:** Describe the governance structure of the blockchain project, including how decisions are made and how the community is involved.  Assess the level of decentralization.
8.  **Social Impact Initiatives:** Detail any social impact projects or initiatives supported by the blockchain or its community.
9.  **Community Engagement (General):** Describe the broader community engagement strategy, including forums, communication channels, and mechanisms for feedback. Provide links to relevant platforms.

**Technical & Security Information:**

10. **GitHub Repositories:** Provide links to all official GitHub repositories associated with the project.
11. **Security Audits:** Provide links to any publicly available security audits conducted on the blockchain's code or infrastructure.
12. **Blockchain Explorers:** Provide links to official or reputable blockchain explorers for the Cronos network.

**Negative News & Controversies:**

13. **Negative News:**  Research and summarize any significant negative news, controversies, or criticisms related to the blockchain, its environmental impact, governance, or social responsibility.  Cite sources.

**Output Format:**

Organize the extracted information clearly, following the numbered categories above.  Provide direct links to sources whenever possible.

**Keywords:** {', '.join(esg_keywords)}
"""

    response = agent.run(query, stream=False)
    return response


if __name__ == "__main__":
    blockchain_data = create_esg_crawler()
    print (blockchain_data.get_content_as_string)

    print(blockchain_data)
    web3_data = {"web3_page":[]}
    web3_data["web3_page"] = blockchain_data.get_content_as_string() 
    with open("web3_data.json", "w") as json_file:
        json.dump(web3_data, json_file, indent=4)

  
