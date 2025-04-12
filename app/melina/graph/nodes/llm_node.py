import json
import re
from typing import Optional, Dict, Any
from pydantic import ConfigDict
import uuid
from pydantic import Field

from app.melina.services.node_cruds.node_crud import NodeCrud
from app.melina.models.node import BaseNode
from app.melina.models.llm import LLMConfig
from langchain.schema.language_model import BaseLanguageModel


class LLMNode(BaseNode):
    """Node that uses an LLM to process data."""
    model_config = ConfigDict(extra="allow")

    llm_config: LLMConfig = Field(...)
    prompt: str = Field(...)
    
    def __init__(
            self, 
            name: str,
            provider: str,
            model_name: str,
            prompt: str, 
            temperature: float = 0.7, 
            max_tokens: int = 1000, 
            top_p: float = 1.0, 
            frequency_penalty: float = 0.0,
            api_key: Optional[str] = None,
            id: Optional[str] = None,
            **kwargs
        ):
        llm_config = LLMConfig(
            provider=provider,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            api_key=api_key
        )
        
        super().__init__(
            name=name,
            description=f"LLM Node using {provider}/{model_name}",
            llm_config=llm_config,
            prompt=prompt,
            id=id,
            **kwargs
        )

        self._llm = None

    @property
    def llm(self) -> BaseLanguageModel:
        """Get or create the LLM instance."""
        if self._llm is None:
            self._llm = self.llm_config.create_model()
        return self._llm
    
    async def save_node(self):
        """Save the node to the database."""
        result = await NodeCrud().create_node(self)
        # self.id = result  
        return result
    
    async def update_node(self):
        """Update the node in the database."""
        await NodeCrud().update_node(self.id, self)

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run the node with the given inputs."""
        try:
            # Format the prompt with input values
            formatted_prompt = self.prompt

            # Simple template formatting
            for key, value in inputs.items():
                if isinstance(value, str):
                    formatted_prompt = formatted_prompt.replace(f"{{{key}}}", value)
                elif isinstance(value, list):
                    formatted_prompt = formatted_prompt.replace(f"{{{key}}}", ", ".join(value))
                elif isinstance(value, dict):
                    formatted_prompt = formatted_prompt.replace(f"{{{key}}}", json.dumps(value))
            
            # Invoke the LLM
            response = await self.llm.ainvoke(formatted_prompt)

            llm_result = response.content.strip()
            llm_result = re.sub(r'```json|```', '', llm_result).strip()
            try:
                ai_response = json.loads(llm_result)
            except json.JSONDecodeError:
                print(f"Error parsing JSON response: {llm_result}")
                ai_response = llm_result
                
            return {
                "output": ai_response,
                "model": self.llm_config.model_name,
                "provider": self.llm_config.provider,
            }
        except Exception as e:
            print(f"Error processing node {self.id}: {e}")
            raise e
