from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

TAGGER_SYSTEM_PROMPT = """
You are a helpful assistant that tags text with the most relevant tags given a set of tags.
If you are given a set of tags, you should tag the text with the most relevant tags, and must use those tags. 
Your job is to 
"""
