import os
import requests
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
import autogen
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "model": os.getenv("MODEL"),
    "api_key": os.getenv("OPENAI_API_KEY")
}


# Step 1: Fetch paragraph texts from a webpage
def fetch_paragraphs(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return [p.text.strip() for p in soup.find_all("p")]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []


# url="https://www.gov.uk/government/news/careers-guidance-for-students-from-lower-socioeconomic-backgrounds-variable-new-report"
# paragraphs = fetch_paragraphs(url)
# print(paragraphs)


# Step 2: Define URLs to scrape
urls = [
    "https://www.gov.uk/government/news/careers-guidance-for-students-from-lower-socioeconomic-backgrounds-variable-new-report",
    "https://www.gov.uk/government/news/campaign-to-tackle-dirty-money-steps-up-with-new-sanctions",
    "https://www.gov.uk/government/news/uk-to-tackle-western-balkan-migrant-transit-routes-and-serious-organised-crime-with-closer-ties-in-the-region",
    "https://www.gov.uk/government/news/ukraine-donor-platform-confirms-support-for-ukraines-recovery-and-reconstruction",
    "https://www.gov.uk/government/news/homes-england-and-octopus-real-estate-launch-150m-greener-homes-alliance-phase-2",
    "https://www.gov.uk/government/news/boost-to-british-business-in-the-usa-as-top-uk-legal-firms-travel-stateside",
    "https://www.gov.uk/government/news/isabel-doverty-appointed-as-the-interim-chair-of-the-advisory-committee-on-business-appointments",
    "https://www.gov.uk/government/news/responsibility-for-all-fire-functions-moves-to-mhclg",
    "https://www.gov.uk/government/publications/secretary-of-state-letter-to-the-first-minister-of-wales",
    "https://www.gov.uk/government/news/almost-two-million-people-on-universal-credit-not-supported-to-look-for-work"
]

# Step 3: Keywords to match
keywords = [
    "Landfill Tax", "Solid waste", "Concrete", "Return", "General Waste",
    "Batteries", "Electronics", "WEEE", "E-waste", "Plastic", "Packaging"
]

# Step 4: Scrape and find matched paragraphs
matched_rows = []

for url in urls:
    paragraphs = fetch_paragraphs(url)
    for paragraph in paragraphs:
        matched_keywords = [keyword for keyword in keywords if keyword.lower() in paragraph.lower()]
        if matched_keywords:
            matched_rows.append({
                "url": url,
                "keywords": ", ".join (matched_keywords),
                "paragraph": paragraph
            })

# Step 5: Prepare data for AutoGen
scraped_text = ""
for row in matched_rows:
    scraped_text += f"URL: {row['url']}\nParagraph: {row['paragraph']}\n\n"

# Step 6: Prompt for the assistant
prompt = (
    f"Below are paragraphs scraped from the websites:\n\n"
    f"{scraped_text}\n\n"
    f"Check if any of these keywords are present: {keywords}.\n"
    f"For each paragraph, list which keywords were found and return the matched paragraphs.\n"
)

# Step 7: Run AutoGen to verify keywords

# with open("OAI_CONFIG_LIST.json", "r") as f:
#     llm_config = json.load(f)



with autogen.coding.DockerCommandLineCodeExecutor(work_dir="coding") as code_executor:
    assistant = AssistantAgent("assistant", llm_config=llm_config)
    user_proxy = UserProxyAgent(
        "user_proxy",
        code_execution_config={"executor": code_executor},#to execute the code in Docker
        human_input_mode="NEVER"
    )

    user_proxy.initiate_chat(assistant, message=prompt)

    # Wait for the assistant's response
    time.sleep(10)  # Adjusting time for better chance of response

    # Debugging: Print the chat messages to inspect the response structure
    print("Assistant's chat messages:", assistant.chat_messages)

    # Extract the assistant's response
    assistant_response = None
    for msg in assistant.chat_messages.get(user_proxy, []):
        if isinstance(msg, dict) and "content" in msg:
            assistant_response = msg["content"]
            break

    if assistant_response is None:
        assistant_response = "No valid response from assistant."

    # Print the assistant response for verification
    print("Assistant Response:", assistant_response)

# Step 8: Save matched paragraphs to Excel, without including assistant_response
df = pd.DataFrame(matched_rows)
excel_file_path = "matched_paragraphs.xlsx"
df.to_excel(excel_file_path, index=False)
print(f"Data saved to: {excel_file_path}")
