from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from haive.core.aug_llm import AugLLMConfig
from haive_agents.simple.factory import create_simple_agent

map_prompt = ChatPromptTemplate.from_messages([('human',"Write a concise summary of the following:\\n\\n{contex}")])
#map_prompt_template_config = PromptTemplateConfig(chat_prompt_template=map_prompt)
map_aug_llm_config = AugLLMConfig(
    name='simple_summarizer',
    prompt_template=map_prompt,
    output_parser = StrOutputParser()
)

simple_summarizer = create_simple_agent(
    engine=map_aug_llm_config,
    name='simple_summarizer'
)
