from utils.logger import log

class AgentNode:
    """
    Mimics Google ADK's Agent API.
    """

    def __init__(self, name: str, role: str, handler):
        """
        Args:
            name (str): Agent name (e.g., 'ParserAgent')
            role (str): Short description of the agent’s job
            handler (callable): Function that performs the agent’s logic
        """
        self.name = name
        self.role = role
        self.handler = handler

    def send(self, message: dict):
        """
        Simulate sending a message to the agent and returning a response.
        """
        log(self.name, f"Received message → {self._truncate(message)}", "info")

        try:
            # response = self.handler(**message) if isinstance(message, dict) else self.handler(message)
            response = self.handler(message)
            log(self.name, "Processed successfully.", "success")
        except Exception as e:
            response = {"error": str(e)}
            log(self.name, f"Error: {e}", "error")

        log(self.name, f"Sending response → {self._truncate(response)}", "info")
        return response

    def _truncate(self, data, max_len=250):
        """Shorten long messages for clean console logs."""
        text = str(data)
        return text[:max_len] + ("..." if len(text) > max_len else "")