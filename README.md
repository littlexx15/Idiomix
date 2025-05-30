
# Idiomix

**Idiomix** is a simple terminal-based chatbot game where users play an idiom relay challenge. It responds with English idioms based on user input, tracks scores, and helps expand your idiom vocabulary through fun interaction.

## Demo Preview

Here are some demo screenshots of the chatbot in action:

### 1. Greeting and Rule Explanation

<div align="center">
  <img src="images/greeting_demo.gif" width="400"/>
</div>

### 2. Idiom Chain Example

<div align="center">
  <img src="images/idiom_chain_demo.gif" width="400"/>
</div>

### 3. Score and Rating After Game

<div align="center">
  <img src="images/game_score_demo.gif" width="400"/>
</div>


# Install and run

## 1. Create and activate a virtual environment

If the virtual environment has not been created yet, run the following command:

### macOS/Linux.
```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows.
```bash
python -m venv .venv
.venv\Scripts\activate
```

## 2. Installing dependencies

After activating the virtual environment, run the following command to install the dependencies required by the project:

```bash
pip install -r requirements.txt
```

## 3. Download the language model

Install the `spacy` language model:

```bash
python -m spacy download en_core_web_sm
```

## 4. Run the chatbot

Ensure that the virtual environment is activated and run the following command to start the program:

```bash
python run_chatbot.py
```

---

## File structure

- **run_chatbot.py**: main entry file, run this file to start the chatbot.
- **my_chatbot.py**: implement the chatbot logic.
- **english_idioms.csv**: dataset of idioms and explanations.
- **requirements.txt**: list of Python libraries that the project depends on.