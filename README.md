
# Idiomix Chatbot

**Idiomix** is an idiom solitaire chatbot for helping users learn and enjoy English idioms.

---

## Installation and operation

### 1. Create and activate a virtual environment

If the virtual environment has not been created yet, run the following command:

#### macOS/Linux.
```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows.
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Installing dependencies

After activating the virtual environment, run:

```bash
pip install -r requirements.txt
```

### 3. Download the language model

Install the language model for spacy:

```bash
python -m spacy download en_core_web_sm
```

### 4. Run the chatbot

Make sure the virtual environment is activated and run the following command to start the program:

```bash
python my_chatbot.py
```

---

## File structure

- **my_chatbot.py**: main program file, run this file to start the chatbot.
- **english_idioms.csv**: dataset of idioms and explanations.
- **requirements.txt**: list of Python libraries that the project depends on.

---

## Notes

Before running the code each time, make sure the virtual environment is activated.  
If you accidentally exit the virtual environment, you can reactivate it with the following command:

#### macOS/Linux.
```bash
source .venv/bin/activate
```

#### Windows: ``bash source .venv/bin/activate
``bash
.venv\Scripts\activate
```

Translated with DeepL.com (free version)