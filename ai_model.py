# MIT License
# Copyright (c) 2023-2024 wunderwuzzi23
# Greetings from Seattle! 

from abc import ABC, abstractmethod
from openai import OpenAI
from groq import Groq
from ollama import Client
from openai import AzureOpenAI 
from anthropic import Anthropic
import os

class AIModel(ABC):
    @abstractmethod
    def chat(self, model, messages):
        pass

    @abstractmethod
    def moderate(self, message):
        pass

    @staticmethod
    def get_model_client(config):
        api_provider=config["api"]

        if api_provider == "" or api_provider==None:
            api_provider = "groq"
        
        if api_provider == "groq":
            return GroqModel(api_key=os.environ.get("GROQ_API_KEY"))
        
        elif api_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:  
                api_key=config["openai_api_key"]       
            if not api_key:  #If statement to avoid "invalid filepath" error
                home_path = os.path.expanduser("~")   
                api_key=open(os.path.join(home_path,".openai.apikey"), "r").readline().strip()
                api_key = api_key

            return OpenAIModel(api_key=api_key)
        
        elif api_provider == "azure":
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            if not api_key:  
                api_key=config["azure_openai_api_key"]
            if not api_key: 
                home_path = os.path.expanduser("~")   
                api_key=open(os.path.join(home_path,".azureopenai.apikey"), "r").readline().strip()

            return AzureOpenAIModel(
                    api_key=api_key,
                    azure_endpoint=config["azure_endpoint"], 
                    api_version=config["azure_api_version"])
        
        elif api_provider == "ollama":
            ollama_api   = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
            #ollama_model = os.environ.get("OLLAMA_MODEL", "llama3-8b-8192")
            return OllamaModel(ollama_api)

        if api_provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key: 
                api_key=config["anthropic_api_key"]
            return AnthropicModel(api_key=api_key) 
        else:
            raise ValueError(f"Invalid AI model provider: {api_provider}")

class GroqModel(AIModel):
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def chat(self, messages, model, temperature, max_tokens):
        resp = self.client.chat.completions.create(model=model, 
                                                   messages=messages, 
                                                   temperature=temperature, 
                                                   max_tokens=max_tokens)
        return resp.choices[0].message.content
    
    def moderate(self, message):
        pass

class OpenAIModel(AIModel):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def chat(self, messages, model, temperature, max_tokens):
        resp = self.client.chat.completions.create(model=model, 
                                                   messages=messages, 
                                                   temperature=temperature,
                                                   max_tokens=max_tokens)
        
        return resp.choices[0].message.content
    
    def moderate(self, message):
        return self.client.moderations.create(input=message)

class OllamaModel(AIModel):
    def __init__(self, host):
        self.client = Client(host=host)
    
    def chat(self, messages, model, temperature, max_tokens):
        resp = self.client.chat(model=model, 
                                messages=messages)
        return resp["message"]["content"]
    
    def moderate(self, message):
        pass


class AzureOpenAIModel(AIModel):
    def __init__(self, azure_endpoint, api_key, api_version):
        self.client = AzureOpenAI(azure_endpoint=azure_endpoint, api_key=api_key, api_version=api_version)

    def chat(self, messages, model, temperature, max_tokens):

        resp = self.client.chat.completions.create(model=model, 
                        messages=messages, 
                        temperature=temperature, 
                        max_tokens=max_tokens)
        
        return resp.choices[0].message.content
    
    def moderate(self, message):
        return self.client.moderations.create(input=message)

class AnthropicModel(AIModel):
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def chat(self, messages, model, temperature, max_tokens):
        ## Anthropic requires the system prompt to be passed separately
        ## Hence extracting system prompt role from the messages
        ## and then passing the messages without the system role 
        ## messages is not subscriptable, so we need to convert it to a list
        system_prompt = next((m.get("content", "") for m in messages if m.get("role") == "system"), "")

        # Remove system messages from the list
        user_messages = [m for m in messages if m.get("role") != "system"]
        resp = self.client.messages.create(model=model, 
                                    system=system_prompt,
                                    messages=user_messages,
                                    temperature=temperature, 
                                    max_tokens=max_tokens)
        
        return resp.content[0].text
    
    def moderate(self, message):
        pass
