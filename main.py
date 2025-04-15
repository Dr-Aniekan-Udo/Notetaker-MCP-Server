# server.py
from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server
mcp = FastMCP("Notetaker Assistant")

# create a new note in resoruces folder
NOTEBOOK = os.path.join(os.path.dirname(__file__), "resources", "notebook.txt")


def check_file():
    if not os.path.exists(NOTEBOOK):
        with open(NOTEBOOK, 'w') as file:
            # create the file
            file.write('')


# Add a tool to add note
@mcp.tool()
def add_note(message: str) -> str:
    """This function appends a new note to the notebook file

    Args:
        message (str): takes in the new note

    Returns:
        str: returns successful if it was done
    """
    check_file()
    with open(NOTEBOOK, 'a') as file:
        # create the file
        file.write(message + "\n")
        return "Note successfully saved!"
    return "Note not saved!"


@mcp.tool()  #resource("note://all")
def read_all_notes() -> str:
    """This function reads all the note contents and returns it

    Returns:
        str: Returns the note content or No note yet
    """
    check_file()
    with open(NOTEBOOK, 'r') as file:
        # read the file and strip off new line and spaces
        note_message = file.read().strip()
    return note_message or "No Note yet!"


@mcp.tool()  #resource("note://latest")
def read_latest_notes() -> str:
    """This function reads the lastest note contents and returns it

    Returns:
        str: Returns the latest note content or No note yet
    """
    check_file()
    with open(NOTEBOOK, 'r') as file:
        # read the note and extract the last line in the notes
        note_message = file.readlines()
    return note_message[-1].strip() if note_message else "No Note yet!"


@mcp.tool()
def read_indexed_notes(index: int) -> str:
    """This function reads note by indicated index. Least accepted index is 1.

    Returns:
        str: Returns the note content or "No note yet!"
    """
    check_file()  # Ensure the file exists or is created
    with open(NOTEBOOK, 'r') as file:
        # Filter out empty lines
        note_message = [line.strip() for line in file.readlines() if line.strip()]
        if not note_message:
            return "No note yet!"
        if len(note_message) < abs(index):  # Ensure the index is within bounds
            return f"You have {len(note_message)} notes currently-- No note {index} to return!"
        return note_message[abs(index) - 1].strip()

@mcp.prompt()
def note_summary_prompt() -> str:
    """This function reads the note contents and returns the summary of the note

    Returns:
        str: Returns the latest note content or No note yet
    """
    check_file()
    with open(NOTEBOOK, 'r') as file:
        # read the note and extract the last line in the notes
        note_message = file.read().strip()
    if not note_message:
        return "no note yet"
    return f"Summarize this message:\n{note_message}"


@mcp.prompt()
def search_note_prompt(message: str) -> str:
    """Generate a prompt for the LLM to search notes for specific information.

    Returns:
        str: A well-formatted prompt for the LLM.
    """
    check_file()
    with open(NOTEBOOK, 'r') as file:
        note_message = [line.strip() for line in file.readlines() if line.strip()]
        if not note_message:
            return "No information is saved in note yet!"
        
        # Construct the prompt for the LLM
        prompt = f"""Here is a list of notes:
{note_message}

Instructions for the LLM:
- Search the notes for information about "{message}".
- Return the matching note(s) along with their index.
- If nothing is found, reply: 'No information on this topic in your note.'"""

        return prompt



if __name__ == "__main__":
    main()
