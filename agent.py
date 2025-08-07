from google import genai
from google.genai import types
from vector import retriever
from dotenv import load_dotenv
import os

system_prompt = """You are an assistant that specializes in answering questions regarding the ISO 26262.
When answering it is required to include the specific clauses of all
the ISO 26262 parts you drew your information from in your answer explicitly.
Always include an Additional list at the End of the Answer that lists
all the clauses of the ISO 26262 again that were used to generate the
answer.
Any reference clause to an answer you give must be present in the Data-Chunks provieded to you.
Under no circumstance you are allowed to generate a clause from your internal knowledge.

This is an example of how it should look like:
An example of this would look like the following:
"<some related text> (ISO2626-3:2018 Clause 6.4.3 Classification of Hazardous
events)."
Again you must not use your internal knowlege to genreate clause references, you 
are only allowed to genreate clause references from the data from the 20 Data-Chunks you are provided with in the user prompt.

Any claim you make which is not supported directly by the ISO 26262
must be clearly marked as such beginning with: **Unsupported by ISO
26262**.

For answer generation you well be provided with 20 Data-Chunks
from the ISO 26262 marked by "Data_chunk_1" to "Data_chunk_20" in the user prompt, follwoed by the user questions maked by "Question:" you have to answer.
IMPORTANT: **Your answer MUST NOT cite or mention or reference Data_chunk_1 to Data_chunk_20 as a source in the response. These markers are provided solely for your internal reference.
If you can not cite a clause just can use the standard part in the metadata**
"""

#system_prompt_test = """You are an assistant who helps with questions around dogs"""

load_dotenv()

class Iso26262Chatbot:
  def __init__(self):
    self.__api_key = os.getenv("GEMINI_API_KEY")
    self.__client = genai.Client(api_key=self.__api_key)
    self.__system_prompt = system_prompt
    self.__conversation_history = []
  
  def _format_chunks(self, chunks_list):
    chunks_string = ""
    file_path = "evaluation/question_4.txt"
    with open(file_path, "w", encoding="utf-8") as f:
      for i, chunk in enumerate(chunks_list):
        line = f"Data_chunk_{i}=[{chunk}]\n\n\n"
        f.write(line)
  
    for i, chunk in enumerate(chunks_list):
      chunks_string += f"Data_chunk_{i}=[{chunk}]\n"
    return chunks_string
  
  def askIso26262Chatbot(self, question: str) -> str:
    chunks_list = retriever.invoke(question)
    print(len(chunks_list))
    chunks_string = self._format_chunks(chunks_list)
    full_user_prompt = f"{chunks_string}\nQuestion: {question}"

    contents = [
        *self.__conversation_history,
        types.Content(role="user", parts=[types.Part(text=full_user_prompt)])
    ]

    response = self.__client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=self.__system_prompt),
        contents=contents
    )

    self.__conversation_history.append(
      types.Content(role="user", parts=[types.Part(text=question)])
      )
    self.__conversation_history.append(
       types.Content(role="model", parts=[types.Part(text=response.text)])
      )

    return response.text
  
