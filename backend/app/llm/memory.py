import threading
from typing import Optional


class ConversationManager:
    """In-memory multi-turn conversation memory keyed by session_id."""

    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns
        self._sessions: dict[str, list[dict[str, str]]] = {}
        self._lock = threading.Lock()

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a single message (user or assistant) to session history."""
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = []
            self._sessions[session_id].append({
                "role": role,
                "content": content
            })
            # Prune older messages if exceeding window
            max_messages = self.max_turns * 2
            if len(self._sessions[session_id]) > max_messages:
                self._sessions[session_id] = self._sessions[session_id][-max_messages:]

    def get_history(self, session_id: str) -> list[dict[str, str]]:
        """Return list of message turns for a session."""
        with self._lock:
            return list(self._sessions.get(session_id, []))

    def format_history_for_prompt(self, session_id: Optional[str]) -> str:
        """Format prior turns for inclusion in LLM prompt."""
        if not session_id:
            return ""

        history = self.get_history(session_id)
        if not history:
            return ""

        lines = ["\n====================\nCONVERSATION HISTORY\n===================="]
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{role}: {msg['content']}")

        return "\n".join(lines)

    def clear_session(self, session_id: str) -> bool:
        """Delete session history."""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False


conversation_manager = ConversationManager(max_turns=6)
