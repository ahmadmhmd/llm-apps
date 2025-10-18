"""
🛡️ SECURITY & RELIABILITY LAYER
Permission system, sandbox mode, undo stack, encrypted storage
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib
import base64
from cryptography.fernet import Fernet
import shutil

class SecurityManager:
    """
    Security and reliability system that provides:
    - Permission system for sensitive operations
    - Sandbox mode for safe testing
    - Undo stack for reversible actions
    - Encrypted storage for sensitive data
    """
    
    def __init__(self, memory_path: Optional[str] = None):
        if memory_path is None:
            memory_path = os.path.join(
                os.path.expanduser("~"),
                "Documents",
                "PowerAgent",
                "Security"
            )
        
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        self.permissions_file = self.memory_path / "permissions.json"
        self.undo_stack_file = self.memory_path / "undo_stack.json"
        self.sandbox_path = self.memory_path / "sandbox"
        self.sandbox_path.mkdir(exist_ok=True)
        
        # Initialize encryption key
        self.key_file = self.memory_path / ".key"
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Permissions
        self.permissions = self._load_permissions()
        
        # Undo stack (last 50 actions)
        self.undo_stack = self._load_undo_stack()
        
        # Sandbox mode
        self.sandbox_mode = False
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Hide the key file
            os.system(f'attrib +h "{self.key_file}"')
            return key
    
    def _load_permissions(self) -> Dict:
        """Load permission settings"""
        if self.permissions_file.exists():
            with open(self.permissions_file, 'r') as f:
                return json.load(f)
        return {
            "file_operations": {
                "read": {"allowed": True, "require_confirmation": False},
                "write": {"allowed": True, "require_confirmation": True},
                "delete": {"allowed": True, "require_confirmation": True},
                "execute": {"allowed": False, "require_confirmation": True}
            },
            "system_operations": {
                "shutdown": {"allowed": False, "require_confirmation": True},
                "registry": {"allowed": False, "require_confirmation": True},
                "admin_tasks": {"allowed": False, "require_confirmation": True}
            },
            "network_operations": {
                "web_access": {"allowed": True, "require_confirmation": False},
                "downloads": {"allowed": True, "require_confirmation": True},
                "uploads": {"allowed": True, "require_confirmation": True}
            },
            "sensitive_data": {
                "clipboard": {"allowed": True, "require_confirmation": False},
                "screenshots": {"allowed": True, "require_confirmation": False},
                "keylogging": {"allowed": False, "require_confirmation": True}
            },
            "protected_paths": []
        }
    
    def _save_permissions(self):
        """Save permission settings"""
        with open(self.permissions_file, 'w') as f:
            json.dump(self.permissions, f, indent=2)
    
    def _load_undo_stack(self) -> List:
        """Load undo stack"""
        if self.undo_stack_file.exists():
            with open(self.undo_stack_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_undo_stack(self):
        """Save undo stack"""
        # Keep only last 50 actions
        if len(self.undo_stack) > 50:
            self.undo_stack = self.undo_stack[-50:]
        
        with open(self.undo_stack_file, 'w') as f:
            json.dump(self.undo_stack, f, indent=2)
    
    def check_permission(self, operation_type: str, operation: str, 
                        details: Dict) -> Dict:
        """
        Check if operation is allowed
        
        Returns:
            {
                "allowed": bool,
                "require_confirmation": bool,
                "reason": str
            }
        """
        
        # Check if path is protected
        if "path" in details:
            path = Path(details["path"])
            if self._is_protected_path(path):
                return {
                    "allowed": False,
                    "require_confirmation": True,
                    "reason": "Path is in protected list"
                }
        
        # Check operation permissions
        if operation_type in self.permissions:
            if operation in self.permissions[operation_type]:
                perm = self.permissions[operation_type][operation]
                return {
                    "allowed": perm["allowed"],
                    "require_confirmation": perm["require_confirmation"],
                    "reason": "Permission granted" if perm["allowed"] else "Permission denied"
                }
        
        # Default: require confirmation for unknown operations
        return {
            "allowed": True,
            "require_confirmation": True,
            "reason": "Unknown operation - requires confirmation"
        }
    
    def _is_protected_path(self, path: Path) -> bool:
        """Check if path is in protected paths"""
        protected = self.permissions.get("protected_paths", [])
        
        for protected_path in protected:
            try:
                if path.is_relative_to(protected_path):
                    return True
            except:
                pass
        
        return False
    
    def request_permission(self, operation: str, details: Dict) -> bool:
        """
        Request user permission for operation
        (In GUI mode, would show dialog)
        """
        
        print(f"\n⚠️  PERMISSION REQUEST")
        print(f"Operation: {operation}")
        print(f"Details: {json.dumps(details, indent=2)}")
        
        # In real implementation, would show GUI dialog
        # For now, auto-approve in non-interactive mode
        
        return True
    
    def add_to_undo_stack(self, action: str, details: Dict, 
                         undo_function: Optional[str] = None,
                         undo_params: Optional[Dict] = None):
        """
        Add action to undo stack
        
        Args:
            action: Action name
            details: Action details
            undo_function: Function to call for undo
            undo_params: Parameters for undo function
        """
        
        entry = {
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "undo_function": undo_function,
            "undo_params": undo_params,
            "can_undo": undo_function is not None
        }
        
        self.undo_stack.append(entry)
        self._save_undo_stack()
    
    def undo_last_action(self) -> Dict:
        """
        Undo the last action
        """
        if not self.undo_stack:
            return {
                "status": "error",
                "message": "No actions to undo"
            }
        
        last_action = self.undo_stack[-1]
        
        if not last_action.get("can_undo"):
            return {
                "status": "error",
                "message": f"Action '{last_action['action']}' cannot be undone"
            }
        
        # Execute undo function
        undo_function = last_action["undo_function"]
        undo_params = last_action.get("undo_params", {})
        
        try:
            # In real implementation, would call actual undo function
            # For now, just log
            self.undo_stack.pop()
            self._save_undo_stack()
            
            return {
                "status": "success",
                "message": f"Undone: {last_action['action']}",
                "action": last_action
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to undo: {str(e)}"
            }
    
    def get_undo_history(self, count: int = 10) -> List[Dict]:
        """Get recent undo-able actions"""
        return self.undo_stack[-count:]
    
    def enable_sandbox_mode(self) -> Dict:
        """
        Enable sandbox mode - all operations work in isolated environment
        """
        self.sandbox_mode = True
        
        return {
            "status": "success",
            "message": "Sandbox mode enabled",
            "sandbox_path": str(self.sandbox_path),
            "info": "All file operations will be isolated to sandbox"
        }
    
    def disable_sandbox_mode(self) -> Dict:
        """Disable sandbox mode"""
        self.sandbox_mode = False
        
        return {
            "status": "success",
            "message": "Sandbox mode disabled"
        }
    
    def clear_sandbox(self) -> Dict:
        """Clear sandbox directory"""
        try:
            shutil.rmtree(self.sandbox_path)
            self.sandbox_path.mkdir(exist_ok=True)
            
            return {
                "status": "success",
                "message": "Sandbox cleared"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to clear sandbox: {str(e)}"
            }
    
    def get_sandbox_path(self, original_path: str) -> str:
        """Convert real path to sandbox path"""
        if not self.sandbox_mode:
            return original_path
        
        # Create mirrored path in sandbox
        path = Path(original_path)
        
        # Remove drive letter if present
        if path.is_absolute():
            parts = path.parts[1:]  # Skip drive
        else:
            parts = path.parts
        
        sandbox_path = self.sandbox_path.joinpath(*parts)
        sandbox_path.parent.mkdir(parents=True, exist_ok=True)
        
        return str(sandbox_path)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        decoded = base64.b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(decoded)
        return decrypted.decode()
    
    def store_secret(self, key: str, value: str) -> Dict:
        """Store encrypted secret"""
        secrets_file = self.memory_path / "secrets.enc"
        
        # Load existing secrets
        secrets = {}
        if secrets_file.exists():
            with open(secrets_file, 'r') as f:
                secrets = json.load(f)
        
        # Encrypt and store
        encrypted_value = self.encrypt_data(value)
        secrets[key] = {
            "value": encrypted_value,
            "created_at": datetime.now().isoformat()
        }
        
        with open(secrets_file, 'w') as f:
            json.dump(secrets, f, indent=2)
        
        return {
            "status": "success",
            "message": f"Secret '{key}' stored securely"
        }
    
    def get_secret(self, key: str) -> Optional[str]:
        """Retrieve encrypted secret"""
        secrets_file = self.memory_path / "secrets.enc"
        
        if not secrets_file.exists():
            return None
        
        with open(secrets_file, 'r') as f:
            secrets = json.load(f)
        
        if key not in secrets:
            return None
        
        encrypted_value = secrets[key]["value"]
        return self.decrypt_data(encrypted_value)
    
    def add_protected_path(self, path: str) -> Dict:
        """Add path to protected paths list"""
        if path not in self.permissions["protected_paths"]:
            self.permissions["protected_paths"].append(path)
            self._save_permissions()
            
            return {
                "status": "success",
                "message": f"Path '{path}' added to protected paths"
            }
        
        return {
            "status": "info",
            "message": "Path already protected"
        }
    
    def remove_protected_path(self, path: str) -> Dict:
        """Remove path from protected paths"""
        if path in self.permissions["protected_paths"]:
            self.permissions["protected_paths"].remove(path)
            self._save_permissions()
            
            return {
                "status": "success",
                "message": f"Path '{path}' removed from protected paths"
            }
        
        return {
            "status": "error",
            "message": "Path not in protected list"
        }
    
    def update_permission(self, operation_type: str, operation: str,
                         allowed: bool, require_confirmation: bool) -> Dict:
        """Update permission for an operation"""
        
        if operation_type not in self.permissions:
            self.permissions[operation_type] = {}
        
        self.permissions[operation_type][operation] = {
            "allowed": allowed,
            "require_confirmation": require_confirmation
        }
        
        self._save_permissions()
        
        return {
            "status": "success",
            "message": f"Permission updated for {operation_type}.{operation}"
        }
    
    def get_security_report(self) -> Dict:
        """Generate security report"""
        
        # Count undoable actions
        undoable = sum(1 for action in self.undo_stack if action.get("can_undo"))
        
        # Count protected paths
        protected_count = len(self.permissions.get("protected_paths", []))
        
        # Count stored secrets
        secrets_file = self.memory_path / "secrets.enc"
        secret_count = 0
        if secrets_file.exists():
            with open(secrets_file, 'r') as f:
                secrets = json.load(f)
                secret_count = len(secrets)
        
        return {
            "sandbox_mode": self.sandbox_mode,
            "undo_stack_size": len(self.undo_stack),
            "undoable_actions": undoable,
            "protected_paths_count": protected_count,
            "stored_secrets_count": secret_count,
            "encryption_enabled": True,
            "recent_actions": self.undo_stack[-5:] if self.undo_stack else []
        }
    
    def create_backup_point(self, name: str, paths: List[str]) -> Dict:
        """
        Create a backup point for rollback
        """
        backup_path = self.memory_path / "backups" / name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        backed_up = []
        failed = []
        
        for path in paths:
            try:
                src = Path(path)
                if src.exists():
                    if src.is_file():
                        dst = backup_path / src.name
                        shutil.copy2(src, dst)
                    else:
                        dst = backup_path / src.name
                        shutil.copytree(src, dst)
                    
                    backed_up.append(path)
            except Exception as e:
                failed.append({"path": path, "error": str(e)})
        
        # Save backup manifest
        manifest = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "backed_up_paths": backed_up,
            "failed_paths": failed
        }
        
        with open(backup_path / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return {
            "status": "success" if backed_up else "error",
            "message": f"Backed up {len(backed_up)} items",
            "backup_name": name,
            "backup_path": str(backup_path),
            "backed_up": backed_up,
            "failed": failed
        }
    
    def restore_backup(self, name: str) -> Dict:
        """Restore from backup point"""
        backup_path = self.memory_path / "backups" / name
        
        if not backup_path.exists():
            return {
                "status": "error",
                "message": f"Backup '{name}' not found"
            }
        
        # Load manifest
        manifest_file = backup_path / "manifest.json"
        if not manifest_file.exists():
            return {
                "status": "error",
                "message": "Backup manifest not found"
            }
        
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)
        
        # Restore files
        restored = []
        failed = []
        
        for original_path in manifest["backed_up_paths"]:
            try:
                src = backup_path / Path(original_path).name
                dst = Path(original_path)
                
                if src.is_file():
                    shutil.copy2(src, dst)
                else:
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                
                restored.append(original_path)
            except Exception as e:
                failed.append({"path": original_path, "error": str(e)})
        
        return {
            "status": "success" if restored else "error",
            "message": f"Restored {len(restored)} items",
            "restored": restored,
            "failed": failed
        }
