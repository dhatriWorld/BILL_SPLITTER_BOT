🧾 SplitBot: AI Receipt & Bill Splitter

Snap a photo of a bill, and SplitBot reads every item, tax and the total, then splits it evenly or by item among your group. The final breakdown is sent straight to Telegram. It works as a quick "emergency bill splitter" for restaurants, trips and shared expenses.

Built with Google Gemini (vision + chat) and the Telegram Bot API.

✨ Features
📸 Receipt reading from a photo: extracts item names, quantities, line amounts, subtotal, taxes (GST/VAT), service charge, discounts, tip and grand total.
✅ Math verification: checks that the items add up to the subtotal and that the subtotal plus charges matches the grand total. Mismatches are flagged, not silently fixed.
👥 Two split modes
Even split: the total is divided by the number of people.
By item: assign items to people, and shared items are divided among those sharing them. Taxes, service charge and tip are shared in proportion to each person's item subtotal.
🔢 Exact rounding: shares are rounded to 2 decimals, and any leftover paisa/cent is assigned to one person so the shares add up exactly to the total.
💬 Conversational: ask follow-ups or make corrections in plain language ("Rahul didn't have the dessert").
🎯 Stays on topic: the bot only handles bills and expenses, and politely declines anything else.
📲 Shareable summary: one clean plain-text summary of who pays what, sent in Telegram and easy to forward.


🔄 How It Works
Photo of receipt ──► Telegram bot ──► Gemini (vision) ──► Structured items & totals
                                                              │
                          Chat: "4 people, split by item" ◄───┘
                                                              │
                                   Final summary ──► Telegram message
The user starts the bot and receives a welcome message.
The user sends a photo of the receipt.
Gemini extracts the line items and totals and verifies the math.
The bot asks how many people are splitting and whether to split evenly or by item.
The user answers, and the bot calculates each person's share.
A hidden summary prompt asks Gemini to reread the whole conversation and produce one clean, shareable breakdown, which is sent to the chat.


🧠 Prompt Design

All prompts live in prompts.py:

Prompt	Purpose
SYSTEM_PROMPT	Sets the SplitBot persona and keeps replies on-topic (bills/expenses only). It is passed once via Gemini's system_instruction, so it applies to every message with no extra if statements in the app code. It also defines how to read receipts and how to split.
WELCOME_MESSAGE_TEMPLATE	The first message the user sees. {name} is filled in at runtime.
SUMMARY_REQUEST_PROMPT	Not shown to the user. It is sent to Gemini behind the scenes when the user asks for the final summary, and returns one clean, copy-paste-ready breakdown.


🛠️ Tech Stack
Python 3.10+
Google Gemini API (google-generativeai / google-genai) for image understanding and chat
Telegram Bot API (python-telegram-bot)

Adjust this list to match the libraries in your requirements.txt.

🚀 Getting Started
1. Clone the repo
bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
2. Install dependencies
bash
pip install -r requirements.txt
3. Get your API keys
Gemini API key: create one in Google AI Studio.
Telegram bot token: message @BotFather on Telegram, send /newbot, and follow the steps.
4. Configure environment variables

Create a .env file in the project root:

env
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

Never commit your .env file. Make sure it is listed in .gitignore.

5. Run the bot
bash
python app.py

Open your bot in Telegram and send /start.

💡 Example

You: (sends a photo of a restaurant bill)

SplitBot:

I found 5 items. Subtotal ₹1,450.00, GST ₹72.50, service charge ₹72.50, total ₹1,595.00. The math checks out ✅. How many people are splitting, and should I split evenly or by item?

You: 3 people, even

SplitBot:

Each person pays ₹531.67. One person pays ₹531.66 so the shares add up exactly to ₹1,595.00.

📁 Project Structure
.
├── app.py            # Telegram bot logic and Gemini calls
├── prompts.py        # SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE, SUMMARY_REQUEST_PROMPT
├── requirements.txt
├── .env              # API keys (not committed)
└── README.md
⚠️ Limitations
Accuracy depends on photo quality. Blurry, cropped or crumpled receipts may produce unclear lines, and the bot will ask you to confirm or re-upload.
Currency defaults to Indian Rupees (₹) when none is visible on the receipt.
Always glance over the extracted items before sharing the final amounts.


🔮 Future Ideas
Saved friend groups for one-tap splitting
Multi-currency support
Expense history and monthly summaries
UPI payment links in the final breakdown
