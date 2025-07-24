# Jester

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⣤⣦⣤⡀⠠⣿⣿⣿⠟⢁⣴⣾⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣦⠈⠿⠃⣰⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀
⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⡗⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀⠀⣿⡿⠛⠿⣿⣿⣿⣿⡟⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀
⠀⠀⢸⠏⠀⠀⠀⠈⢻⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⠋⣉⡉⠻⣿⣿⡇⠀⠀⠀
⠀⠀⣈⠀⠀⠀⠀⠀⠈⣿⠃⣼⣿⣿⣿⣿⣿⣿⣿⠁⠘⢿⡇⠀⠈⢻⣿⠀⠀⠀
⠀⢾⣿⡇⠀⠀⠀⠀⠀⠏⢰⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢀⣀⣀⠀⠀⢻⠀⠀⠀
⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠸⠿⠿⠀⠀⠈⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⢿⣿⣿⣿⡿⣿⣿⣿⡄⠀⠀⠀⠀⠀⢠⣶⣆⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠀⣿⡿⢁⠘⣿⣿⣿⠁⡈⢻⣿⠃⣰⡄⠀⠀⠀⠘⠛⠋⠀
⠀⠀⠀⠀⠀⠀⠀⣾⣆⠈⠁⣾⣦⠘⢿⠃⣰⣷⡄⠁⣰⣿⣿⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣷⣤⣿⣿⣷⣤⣾⣿⣿⣷⣾⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠛⠛⠋⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

A customizable AI that runs in your console, and can make notes in Obsidian. 

## Install 

1. Download the release zip file or clone this repo
2. Go to https://openrouter.ai and log in to make a key
    - Find the model you want to use, the one in here uses qwen/qwen3-235b-a22b-07-25:free which is a free model, it is pretty slow, so you can change it if you want(shown later in the document)
    - Go to your account->keys and generate a new key
3. Copy your key and paste it in the .env file.
4. IF you are going to use obsidian with it, add a path to the folder in the .env file, I would recommend making a new folder so all AI generated notes will be seperated.
### Not needed but recommended.
5. Create a path to the folder. This will make it much easier to run the bot, without it you would have to run it like this:
```pwsh
 py "./path/to/jester.py" -s "Othello"
```
  After:
```pwsh
jes -s "Othello"
```
Here is a guide to setting a path: https://www.java.com/en/download/help/path.html

## How to Use

Just open your terminal and call it by typing jes, then the argument, then in quotes your prompt

```pwsh
jes -arg "something"
```

### Arguments
 - -s  --summarize   Summarize literature or a concept
 - -q  --question    Get a short answer + summary
 - -iq --quotes      Get interesting quotes from a book
 - -hh --helpme      Show this help menu
 - -nf --neofetch    Show Jester ASCII intro
 - -g  --generate    Create something (story, poem, etc.)
 - -w  --wordfor     Suggest a word or phrase
 - -cd --code        Help with code-related questions
 - -dm --dnd         Answer a Dungeons and Dragons question
 - -cv --convertnote Convert a PDF to clean, AI-formatted markdown and save to Obsidian, your prompt should be the path to the pdf you want to send
 - -o  --obsidian    Save the response to Obsidian (optional filename)
   - -o is special, it as to be used at the end, jes -s "Othello" -o
Arguments are used when you do not want to type out an entire prompt over and over again. 

## Customize 

All of these will be in the jester.py file

### How to Change the Model 

Locate where it says MODEL, should be line 27. Go to Openrouter and pick another model to use, just get its name

### How to add commands 

Inside the main function, add a new argument:

```python
parser.add_argument("-shortcut", "--name", help="description")
```
Right below that in args.helpme, add what your new command does.

Create a new elif:

```python
elif args.name:
        prompt = f"your prompt using this user response: {args.name}"
```

### How to edit prompts  

Edit the elifs around line 200.

## To Do

- make -o be able to take previous responses and send them to obsidian
- allow for -o to pick what folder it goes in

