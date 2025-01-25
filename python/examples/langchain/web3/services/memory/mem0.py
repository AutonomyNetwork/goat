from mem0 import MemoryClient
from datetime import datetime
from typing import Optional

class MemoryManager:
    def __init__(self, mem0_api_key: str):
        self.mem0_client = MemoryClient(api_key=mem0_api_key)
    
    async def add_user_memory(self, user_id: str, message: list,infer:bool, agent_id:str = None):
        try:
            print(message,"MESSAGE")
            response = self.mem0_client.add(
                messages=message,
                user_id=user_id,
                agent_id=agent_id,
                infer=infer,
                output_format="v1.1"  # Use enhanced output format
            )
            print("Memory added successfully:", response)
            
        except Exception as e:
            print(f"Error occurred while adding user memory: {e},")
            raise

    async def add_agent_memory(self, agent_id: str, message: list):
        try:
            response = self.mem0_client.add(
                messages=message,
                agent_id=agent_id,
                output_format="v1.1"  # Use enhanced output format
            )
            print("Memory added successfully:", response)
        except Exception as e:
            print(f"Error occurred while adding agent memory: {e}")
            raise
    async def search_recent_user_memory(self, user_id: str,agent_id:str = None):
        try:
            
            response = self.mem0_client.get_all(
                output_format="v1.1",
                user_id=user_id,
                agent_id=agent_id,
                page_size=10,
                page=1,
                fields=["id","input",'created_at']
            )
            # print(response,"FF")
            # print(response)
            if 'results' not in response:
                print("No memories found.")
                return []

            memories = response['results']['results']
            
            if not memories:
                print("No memories found.")
                return []
            
            formatted_memories = []

            # print(response,"R")


            for memory in memories:
                print(memory['created_at'])
                for input_msg in memory['input']:
                    formatted_memories.append({
                        'role':input_msg['role'],
                        'content':input_msg['content'],
                        "timestamp":memory['created_at']
                    })

            # Sort after formatting to maintain message order within conversations
            sorted_memories = sorted(
                formatted_memories,
                key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')),
                reverse=False  # Get most recent first
            )
            sorted_memories_after_removing_timestamp=[{k: v for k, v in d.items() if k != 'timestamp'} for d in sorted_memories]

            # print(f"Retrieved {len(sorted_memories)} memories")
            # print(sorted_memories,"SORT")
            return sorted_memories_after_removing_timestamp

        except Exception as e:
            raise Exception(f"Error occurred while searching recent user memory: {e}")
        
    async def search_user_memory(self,user_id:str,user_message:str,agent_id:str = None):
        try:
            user_memories =self.mem0_client.search(user_message,version="v1",limit=5,user_id=user_id,agent_id=agent_id)
            print(user_memories,"UUU")
            return user_memories
        except Exception as e:
            raise (f"Error occurered while searching user memory {e}")

    async def delete_create_agent_memory(self, user_id: str, agent_id: Optional[str] = None):
        try:
            self.mem0_client.delete_all(user_id=user_id, agent_id=agent_id)
            return {"success": True, "message": "Memory deleted successfully"}

        except Exception as e:
            # Handle the exception (logging or re-raising it)
            print(f"An error occurred: {e}")

            return {"success": False, "message": f"Error: {str(e)}"}





