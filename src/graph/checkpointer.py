"""
LangGraph Checkpointing - Enables resume capability for long research runs.
Saves intermediate agent states to disk for fault tolerance.
"""
import os
import json
import pickle
from datetime import datetime
from typing import Optional, Any
from langgraph.checkpoint.memory import MemorySaver
from src.config.settings import settings
from src.utils.logger import app_logger


class DiskCheckpointer:
    """
    Disk-based checkpointer that persists agent states to files.
    Allows resuming interrupted research pipelines.
    
    For production: replace with PostgreSQL or Redis checkpointer.
    """

    def __init__(self, checkpoint_dir: str = None):
        self.checkpoint_dir = checkpoint_dir or settings.checkpoints_dir
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        app_logger.info(f"DiskCheckpointer initialized at: {self.checkpoint_dir}")

    def save(self, thread_id: str, state: dict, step: str) -> str:
        """
        Save agent state checkpoint to disk.
        
        Args:
            thread_id: Unique pipeline run ID
            state: Current agent state dict
            step: Current agent/step name
            
        Returns:
            Path to saved checkpoint file
        """
        checkpoint_data = {
            "thread_id": thread_id,
            "step": step,
            "timestamp": datetime.utcnow().isoformat(),
            "state": state,
        }

        filename = f"{thread_id}_{step}.json"
        filepath = os.path.join(self.checkpoint_dir, filename)

        try:
            # Save JSON (excluding non-serializable objects)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(
                    checkpoint_data,
                    f,
                    indent=2,
                    default=str,  # Handle non-serializable types
                    ensure_ascii=False,
                )
            app_logger.debug(f"💾 Checkpoint saved: {filename}")
            return filepath

        except Exception as e:
            app_logger.warning(f"Failed to save checkpoint {filename}: {e}")
            return ""

    def load(self, thread_id: str, step: str) -> Optional[dict]:
        """
        Load a checkpoint from disk.
        
        Args:
            thread_id: Pipeline run ID
            step: Step to restore
            
        Returns:
            State dict or None if not found
        """
        filename = f"{thread_id}_{step}.json"
        filepath = os.path.join(self.checkpoint_dir, filename)

        if not os.path.exists(filepath):
            app_logger.debug(f"No checkpoint found: {filename}")
            return None

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            app_logger.info(f"📂 Checkpoint loaded: {filename}")
            return data.get("state")

        except Exception as e:
            app_logger.warning(f"Failed to load checkpoint {filename}: {e}")
            return None

    def list_checkpoints(self, thread_id: str) -> list:
        """List all checkpoints for a given thread."""
        checkpoints = []
        for filename in os.listdir(self.checkpoint_dir):
            if filename.startswith(thread_id):
                filepath = os.path.join(self.checkpoint_dir, filename)
                stat = os.stat(filepath)
                checkpoints.append({
                    "filename": filename,
                    "step": filename.replace(f"{thread_id}_", "").replace(".json", ""),
                    "size_bytes": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })

        return sorted(checkpoints, key=lambda x: x["modified"])

    def delete_checkpoints(self, thread_id: str) -> int:
        """Delete all checkpoints for a thread. Returns count deleted."""
        count = 0
        for filename in os.listdir(self.checkpoint_dir):
            if filename.startswith(thread_id):
                os.remove(os.path.join(self.checkpoint_dir, filename))
                count += 1
        app_logger.info(f"🗑️ Deleted {count} checkpoints for thread: {thread_id}")
        return count

    def cleanup_old_checkpoints(self, max_age_hours: int = 24) -> int:
        """Remove checkpoints older than max_age_hours. Returns count deleted."""
        import time
        cutoff = time.time() - (max_age_hours * 3600)
        count = 0

        for filename in os.listdir(self.checkpoint_dir):
            filepath = os.path.join(self.checkpoint_dir, filename)
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
                count += 1

        if count > 0:
            app_logger.info(f"🧹 Cleaned up {count} old checkpoints")
        return count


def get_memory_checkpointer() -> MemorySaver:
    """
    Get LangGraph's built-in in-memory checkpointer.
    Fast but loses state on restart.
    Use for development and single-run scenarios.
    """
    return MemorySaver()


# Default checkpointer instances
disk_checkpointer = DiskCheckpointer()
memory_checkpointer = get_memory_checkpointer()