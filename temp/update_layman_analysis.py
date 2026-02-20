import json

path = '/Users/yeshwanth/Desktop/ai-engineering-fordham/5.you-can-just-build-things.ipynb'
with open(path, 'r') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'markdown' and '### Evaluation Analysis' in cell.get('source', [''])[0]:
        cell['source'] = [
            "### How Good is Our Fordham Chatbot?\n",
            "\n",
            "We just tested our chatbot's ability to pull up the right webpage when answering 40 different simulated student questions. Here is how well it did:\n",
            "\n",
            "**1. The \"Ctrl+F\" Method (BM25 / Full Text Search)**\n",
            "- **How it works:** It looks for the exact words typed by the user, just like when you use \"Find\" on an article.\n",
            "- **The Results:** It found the right page in the top 10 results **62.5%** of the time. \n",
            "- **The Problem:** If a student asks, *\"How much are classes?\"*, but the webpage says *\"Tuition\"*, this method gets confused because the exact words don't match.\n",
            "\n",
            "**2. The \"Meaning\" Method (Vector Search)**\n",
            "- **How it works:** It understands the *meaning* or *intent* of a question. \n",
            "- **The Results:** It did slightly better, finding the right page **67.5%** of the time. \n",
            "- **The Problem:** It can sometimes overthink things. If a student asks for the *\"Phone number of the Biology teacher\"*, it might pull up an article about *\"Biology class descriptions\"* because the meaning is similar, completely missing the exact phone number.\n",
            "\n",
            "**3. The Best of Both Worlds (Hybrid Search)**\n",
            "- **How it works:** We smashed both methods together. We told the computer: *\"Look for the exact words, AND look for the meaning, and combine the scores.\"*\n",
            "- **The Results:** It found the correct page in the top 10 results **72.5%** of the time, beating both of the other methods!\n",
            "- **The Takeaway:** By using Hybrid Search, if a student uses the exact right word, we find it. If they use a synonym, we still find it. This is why Netflix, Google, and Amazon all use Hybrid Search today!"
        ]
        break

with open(path, 'w') as f:
    json.dump(nb, f, indent=1)
