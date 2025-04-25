# llm_handler.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Google Gemini API client
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
    # Handle the error appropriately if the key is missing, maybe raise an Exception
    # For now, the configure call below will likely fail, which is caught.
else:
     try:
        genai.configure(api_key=api_key)

        
     except Exception as e:
          # Catch errors during the initial configuration of the SDK
          print(f"Error configuring Google AI SDK: {e}")
          # Depending on the application's needs, might raise the error or handle it
          # For Streamlit, printing the error might be sufficient for debugging

# Define safety settings for content generation (optional but recommended)
# Adjust thresholds as needed (BLOCK_NONE is most permissive, others are stricter)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Define generation configuration (optional)
generation_config = {
  "temperature": 0.2, # Lower temperature for more deterministic, factual answers
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 250, # Limit output length
}


def get_llm_response(context, query):
    """Sends context and query to Google Gemini Pro and gets response."""

    # Double-check if the API key was successfully loaded and configured
    if not api_key:
         return "Error: Google API key not configured. Please check your .env file and ensure the key is set."

    # Select the Gemini model
    # !!! IMPORTANT: Keep this as 'gemini-1.0-pro' for now. !!!
    # !!! After running the debug code, change this line !!!
    # !!! to use a valid model name printed in your terminal. !!!
    # Example: model_name="models/gemini-1.5-flash-latest"
    target_model_name = "models/gemini-1.5-pro-latest"
 # <-- Keep this for the debug run

    try:
        model = genai.GenerativeModel(
            model_name=target_model_name, # Use the variable defined above
            generation_config=generation_config,
            safety_settings=safety_settings
            )
    except Exception as e:
         print(f"Error creating Gemini model instance for '{target_model_name}': {e}")
         # Check if the error message specifically mentions the model name is invalid
         if "model not found" in str(e).lower() or "is not found" in str(e).lower():
              return f"Error: The specified model '{target_model_name}' could not be found or accessed. Please check the model name and ensure it's available (see terminal output from model listing)."
         return f"Error: Could not initialize the Gemini model: {e}"


    # Construct the prompt for Gemini
    prompt = f"""You are a helpful financial assistant. Your task is to answer the user's question based *only* on the provided 'Context'. Do not use any external knowledge or information you might have. If the context does not contain the information needed to answer the question, state clearly that the information is not available in the provided knowledge base. Keep your answer concise and directly address the user's question.

Context:
---
{context}
---

User Question: {query}

Answer:"""

    try:
        # Generate content using the model
        response = model.generate_content(prompt)

        # Extract the text from the response
        # Add checks for response structure and potential safety blocks
        if hasattr(response, 'text'):
             answer = response.text
        elif response.parts:
             # If .text isn't available but parts are, try concatenating them
             answer = "".join(part.text for part in response.parts)
        else:
             # Handle cases where the response might be blocked due to safety settings
             # or is otherwise empty. Check response.prompt_feedback for details.
             feedback = getattr(response, 'prompt_feedback', None)
             block_reason = getattr(feedback, 'block_reason', None) if feedback else None
             if block_reason:
                  safety_ratings_str = "\n".join([f"- {rating.category}: {rating.probability}" for rating in getattr(feedback, 'safety_ratings', [])]) if getattr(feedback, 'safety_ratings', []) else "N/A"
                  return f"Error: The response was blocked due to safety settings. Reason: {block_reason}\nSafety Ratings:\n{safety_ratings_str}"
             else:
                  # Check if the response object itself has helpful error info
                  try:
                      # Sometimes error details might be within the object representation
                      print(f"Debug: Received unusual response object: {response}")
                  except Exception:
                      pass # Avoid errors during printing the response object itself
                  return "Error: Received an empty or unexpected response structure from the LLM."


        return answer.strip()

    except Exception as e:
        # Catch potential errors during API call (e.g., network issues, invalid requests)
        print(f"Error calling Google Gemini API: {e}")
        # Provide a user-friendly error message
        # Check specific exception types if needed (e.g., google.api_core.exceptions.ResourceExhausted)
        error_str = str(e).lower()
        if "api key not valid" in error_str or "permission denied" in error_str:
             return "Error: The provided Google API key is not valid or lacks permissions. Please check your .env file and Google Cloud project settings."
        if "resource has been exhausted" in error_str or "quota exceeded" in error_str:
             return "Error: Google API quota exceeded (e.g., requests per minute). Please wait and try again or check your usage limits."
        if "is not found for api version" in error_str or "not supported for generatecontent" in error_str:
             # This error *should* be caught earlier during model instantiation, but added as a fallback
             return f"Error: Model '{target_model_name}' is likely not supported or found via the current API connection. Check the model listing output in the terminal. Details: {e}"

        return f"Error: An unexpected error occurred while communicating with the Google Gemini API: {e}"