# 🔍 AutoGen Web Scraper for Keyword Detection

This Python script scrapes UK government news websites, extracts relevant paragraphs based on environment and waste-related keywords, and uses **LLM (via AutoGen)** to validate and analyze results. It stores the final output in an Excel file for easy sharing and review.

---

## 📌 Features

- Scrapes paragraph content from a list of UK government news URLs
- Matches content using a list of predefined environmental/waste-related keywords
- Validates matches using **AutoGen** with GPT-based assistant
- Saves matched results into an Excel file (`matched_paragraphs.xlsx`)
- Loads environment variables securely from `.env` file

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/shobhraj650/Webscrapping.git
cd Webscrapping
```

### 2. Install Dependencies

```bash
pip install -r requirement.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory based on `.env.sample`.

```env
# .env
OPENAI_API_KEY=your_openai_api_key
MODEL=gpt-4
```

✅ **Note:** Never commit `.env` to GitHub. Use `.env.sample` for public templates.

---

## 🧠 How It Works

1. Loads list of UK government URLs
2. Extracts `<p>` tag text using BeautifulSoup
3. Checks if any paragraph contains keywords (case-insensitive match)
4. Formats the matched data into a prompt for the LLM assistant via AutoGen
5. Assistant returns validated keyword matches
6. Results are saved to `matched_paragraphs.xlsx`

---

## 🧪 Sample Keywords

```python
keywords = [
    "Landfill Tax", "Solid waste", "Concrete", "Return", "General Waste",
    "Batteries", "Electronics", "WEEE", "E-waste", "Plastic", "Packaging"
]
```

---

## 🧰 Project Structure

```
📁 your-repo/
├── Scrapping.py           # Main script
├── .env.sample            # Sample environment variable config
├── requirement.txt        # Python dependencies
└── matched_paragraphs.xlsx # Output file (generated after run)
```

---

## ✅ To Run the Script

```bash
python Scrapping.py
```

The script will scrape the websites, perform keyword matching, send the data to the LLM, and save the results to Excel.

---

## ⚙️ Built With

- Python 3.8+
- [AutoGen](https://github.com/microsoft/autogen)
- OpenAI LLM (via API)
- BeautifulSoup
- Pandas
- Python-dotenv

---

## 📌 Notes

- Script only works with **static content** (non-JS rendered pages).
- Keyword matching is currently **case-insensitive**.
- The assistant logic includes a `10-second sleep` to allow time for the response—this may be optimized later.
- Ensure Docker is installed and running if you're using `DockerCommandLineCodeExecutor`.

---

## 🔐 Security Tip

Always use `.env` for storing sensitive data like your API keys. Avoid hardcoding them in Python or JSON files.

---