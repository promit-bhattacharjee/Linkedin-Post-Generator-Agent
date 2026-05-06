# AI-Powered LinkedIn Post Generator

This project is a multi-agent AI system built using **FastAPI** and **LangChain** that automatically generates professional LinkedIn posts based on a user-provided topic and an optional language preference.

## Features & Assignment Requirements Met
1. **Accept User Inputs:** The system accepts a `Topic` and a `Language` selection. If "Auto-Detect" is chosen, it automatically detects the language from the topic.
2. **Conditional Routing Agent:** A "Structured Router" classifies topics as `technology` or `general` with high precision.
3. **Specialized Writer Agents:**
   - **Tech Writer Agent:** Focuses on professional, industry-specific tech content.
   - **General Writer Agent:** Focuses on relatable, professional general-interest content.
4. **Post Formatting:** Generates 2-4 short paragraphs with a professional tone and a strong Call-to-Action (CTA).
5. **Conditional Handover:** Automated routing logic ensures the correct expert handles the specific topic.
6. **Premium User Interface:**
   - **LinkedIn Branding:** Professional UI with the official LinkedIn color palette and logo.
   - **Language Dropdown:** Support for 15+ major languages.
   - **Copy to Clipboard:** One-click copying for easy posting.
   - **Full Metadata Visibility:** Displays the AI's internal reasoning (Classification, Confidence scores, Corrected Topic Name).

## Agent Workflow & Routing Logic
The application follows a clean, 2-step LangChain workflow:

1. **Step 1: The Routing Phase (`router_chain`)**
   - The user submits a `POST /generate` request containing the `topic` and `language` (optional).
   - The `router_chain` uses `llm.with_structured_output` to evaluate the topic and return a guaranteed classification string: `"technology"` or `"general"`.
   
2. **Step 2: The Conditional Handover & Generation**
   - The FastAPI endpoint evaluates the classification.
   - If the category contains `"technology"`, the execution is handed over to the `tech_writer` chain.
   - If the category is anything else, the execution is handed over to the `general_writer` chain.
   - A `language_instruction` is dynamically injected into the writer's prompt. If the user provided a language (e.g., "Spanish"), it instructs the LLM: `"Write the post in Spanish"`. If left blank, it instructs the LLM to `"Detect the input language and write the post in that language"`.
   - The selected writer generates the post using `llm.with_structured_output(FinalOutput)`, ensuring the final payload contains perfectly typed fields (topic name, confidence scores, and the formatted post) which is then returned to the user interface.

## How to Run
1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn langchain langchain-openai langchain-core python-dotenv pydantic pydantic-settings rich
   ```
2. **Setup environment**: Create a `.env` file with your `BASE_URL`, `API_KEY`, and `MODEL_NAME`.
3. **Run the server**:
   ```bash
   python main.py
   ```
4. **Open the UI**: Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Demonstration Examples

Here are two examples demonstrating the system's routing and generation capabilities.

### Example 1: Tech Topic in English
**Input:**
```json
{
  "topic": "AI in Healthcare",
  "language": "English"
}
```

**Routing Decision:**
The router classifies this as `technology`, triggering the **Tech Writer Agent**.

**Output:**
```json
{
  "topic_name": "AI in Healthcare",
  "topic_class": "technology",
  "topic_confidence": 0.98,
  "post": "Artificial Intelligence is rapidly transforming the healthcare industry. From predictive analytics to personalized medicine, AI-driven solutions are enabling faster and more accurate diagnostics, ultimately improving patient outcomes and streamlining hospital operations. 🏥💻\n\nBy leveraging advanced machine learning algorithms, healthcare professionals can now identify patterns in medical data that were previously impossible to detect. This not only empowers doctors to make data-backed decisions but also reduces administrative burdens, allowing them to focus more on patient care. ⚕️📊\n\nAs we continue to see massive investments in health-tech, it is clear that AI is no longer just a futuristic concept—it is a critical tool saving lives today. How do you see AI impacting the future of your specific sector in healthcare? Let me know your thoughts below! 👇\n\n#HealthTech #ArtificialIntelligence #HealthcareInnovation #MachineLearning",
  "translation_confidence": 1.0
}
```

### Example 2: General Topic in Bengali
**Input:**
```json
{
  "topic": "Healthy eating habits",
  "language": "Bengali"
}
```

**Routing Decision:**
The router classifies this as `general`, triggering the **General Writer Agent**.

**Output:**
```json
{
  "topic_name": "স্বাস্থ্যকর খাদ্যাভ্যাস",
  "topic_class": "general",
  "topic_confidence": 0.95,
  "post": "সুস্বাস্থ্য বজায় রাখার জন্য স্বাস্থ্যকর খাদ্যাভ্যাস অত্যন্ত গুরুত্বপূর্ণ। প্রতিদিনের খাবারে পর্যাপ্ত পরিমাণে শাকসবজি, ফলমূল এবং প্রোটিন যুক্ত করা আমাদের শরীরের রোগ প্রতিরোধ ক্ষমতা বাড়াতে সাহায্য করে। এর ফলে আমরা সারাদিন কর্মক্ষম ও সতেজ থাকতে পারি। 🥗🍎\n\nসঠিক সময়ে এবং পরিমিত পরিমাণে খাবার খাওয়া আমাদের ওজন নিয়ন্ত্রণে রাখতে দারুণ ভূমিকা পালন করে। প্রক্রিয়াজাত খাবার এবং অতিরিক্ত চিনি এড়িয়ে চলা দীর্ঘমেয়াদী সুস্থতার চাবিকাঠি। ছোট ছোট ইতিবাচক পরিবর্তন আমাদের জীবনে বিশাল প্রভাব ফেলতে পারে! 💧💪\n\nআপনি প্রতিদিনের খাদ্যতালিকায় কোন স্বাস্থ্যকর অভ্যাসটি মেনে চলেন? নিচে কমেন্ট করে আপনার মতামত শেয়ার করুন! 👇\n\n#Health #HealthyLifestyle #Nutrition #Wellness",
  "translation_confidence": 0.99
}
```
