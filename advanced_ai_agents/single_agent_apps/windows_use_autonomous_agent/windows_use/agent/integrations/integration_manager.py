"""
🌐 PHASE 8: ECOSYSTEM INTEGRATION
Integration with email, cloud storage, calendar, messaging, and more
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from pathlib import Path

class EmailIntegration:
    """
    Email integration supporting:
    - Send emails with attachments
    - Read emails (IMAP)
    - Search emails
    - Manage drafts
    """
    
    def __init__(self, email: str, password: str, smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587, imap_server: str = "imap.gmail.com"):
        self.email = email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
    
    def send_email(self, to: str, subject: str, body: str,
                   cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None,
                   attachments: Optional[List[str]] = None,
                   html: bool = False) -> Dict:
        """
        Send email
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients
            attachments: List of file paths to attach
            html: Whether body is HTML
        """
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Attach body
            msg.attach(MIMEText(body, 'html' if html else 'plain'))
            
            # Attach files
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                
                recipients = [to]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                
                server.sendmail(self.email, recipients, msg.as_string())
            
            return {
                "status": "success",
                "message": f"Email sent to {to}",
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def send_bulk_email(self, recipients: List[str], subject: str, body: str,
                       personalize: bool = False) -> Dict:
        """
        Send email to multiple recipients
        
        Args:
            recipients: List of email addresses
            subject: Email subject
            body: Email body (can use {name} placeholder)
            personalize: Whether to personalize each email
        """
        
        sent = []
        failed = []
        
        for recipient in recipients:
            try:
                # Personalize if enabled
                if personalize and '{name}' in body:
                    name = recipient.split('@')[0].title()
                    personalized_body = body.replace('{name}', name)
                else:
                    personalized_body = body
                
                result = self.send_email(recipient, subject, personalized_body)
                
                if result["status"] == "success":
                    sent.append(recipient)
                else:
                    failed.append({"email": recipient, "error": result["message"]})
            
            except Exception as e:
                failed.append({"email": recipient, "error": str(e)})
        
        return {
            "status": "success" if sent else "error",
            "sent_count": len(sent),
            "failed_count": len(failed),
            "sent": sent,
            "failed": failed
        }


class CloudStorageIntegration:
    """
    Cloud storage integration (OneDrive/Google Drive)
    Note: For production, use official APIs with OAuth
    """
    
    def __init__(self, provider: str = "onedrive"):
        self.provider = provider
        self.local_sync_path = self._get_sync_path()
    
    def _get_sync_path(self) -> Optional[Path]:
        """Get local sync folder path"""
        if self.provider == "onedrive":
            # Common OneDrive path
            onedrive_path = Path(os.path.expanduser("~")) / "OneDrive"
            if onedrive_path.exists():
                return onedrive_path
        
        elif self.provider == "googledrive":
            # Google Drive path (if installed)
            gdrive_path = Path(os.path.expanduser("~")) / "Google Drive"
            if gdrive_path.exists():
                return gdrive_path
        
        return None
    
    def upload_file(self, local_path: str, cloud_path: Optional[str] = None) -> Dict:
        """
        Upload file to cloud storage
        (Simplified version using local sync folder)
        """
        
        if not self.local_sync_path:
            return {
                "status": "error",
                "message": f"{self.provider} sync folder not found"
            }
        
        try:
            src = Path(local_path)
            
            if not src.exists():
                return {
                    "status": "error",
                    "message": "Source file not found"
                }
            
            # Determine destination
            if cloud_path:
                dst = self.local_sync_path / cloud_path
            else:
                dst = self.local_sync_path / src.name
            
            # Ensure parent directory exists
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file to sync folder (will auto-upload)
            import shutil
            shutil.copy2(src, dst)
            
            return {
                "status": "success",
                "message": f"File uploaded to {self.provider}",
                "cloud_path": str(dst.relative_to(self.local_sync_path))
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def download_file(self, cloud_path: str, local_path: str) -> Dict:
        """Download file from cloud storage"""
        
        if not self.local_sync_path:
            return {
                "status": "error",
                "message": f"{self.provider} sync folder not found"
            }
        
        try:
            src = self.local_sync_path / cloud_path
            
            if not src.exists():
                return {
                    "status": "error",
                    "message": "Cloud file not found"
                }
            
            dst = Path(local_path)
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copy2(src, dst)
            
            return {
                "status": "success",
                "message": f"File downloaded from {self.provider}",
                "local_path": local_path
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def list_files(self, cloud_path: str = "") -> Dict:
        """List files in cloud storage directory"""
        
        if not self.local_sync_path:
            return {
                "status": "error",
                "message": f"{self.provider} sync folder not found"
            }
        
        try:
            target = self.local_sync_path / cloud_path if cloud_path else self.local_sync_path
            
            if not target.exists():
                return {
                    "status": "error",
                    "message": "Directory not found"
                }
            
            files = []
            for item in target.iterdir():
                files.append({
                    "name": item.name,
                    "type": "folder" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
            
            return {
                "status": "success",
                "path": cloud_path or "/",
                "files": files
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def create_share_link(self, cloud_path: str) -> Dict:
        """
        Create shareable link (placeholder - needs real API)
        """
        return {
            "status": "info",
            "message": "Share link creation requires API integration",
            "suggestion": "Use OneDrive/Google Drive web interface to create share links"
        }


class WebhookIntegration:
    """
    Webhook integration for external services
    """
    
    def __init__(self):
        self.webhooks = {}
    
    def register_webhook(self, name: str, url: str, method: str = "POST") -> Dict:
        """Register a webhook"""
        self.webhooks[name] = {
            "url": url,
            "method": method,
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "message": f"Webhook '{name}' registered"
        }
    
    def send_webhook(self, name: str, data: Dict) -> Dict:
        """Send data to webhook"""
        
        if name not in self.webhooks:
            return {
                "status": "error",
                "message": "Webhook not found"
            }
        
        webhook = self.webhooks[name]
        
        try:
            import requests
            
            response = requests.request(
                method=webhook["method"],
                url=webhook["url"],
                json=data
            )
            
            return {
                "status": "success",
                "message": "Webhook triggered",
                "response_code": response.status_code
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


class IntegrationManager:
    """
    Central integration manager for all ecosystem connections
    """
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.expanduser("~"),
                "Documents",
                "PowerAgent",
                "Integrations"
            )
        
        self.config_path = Path(config_path)
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_path / "integrations.json"
        self.config = self._load_config()
        
        # Initialize integrations
        self.email = None
        self.cloud_storage = None
        self.webhooks = WebhookIntegration()
    
    def _load_config(self) -> Dict:
        """Load integration configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "email": {},
            "cloud_storage": {},
            "webhooks": {},
            "calendar": {},
            "messaging": {}
        }
    
    def _save_config(self):
        """Save integration configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_email(self, email: str, password: str, 
                   smtp_server: str = "smtp.gmail.com") -> Dict:
        """Setup email integration"""
        
        try:
            self.email = EmailIntegration(email, password, smtp_server)
            
            self.config["email"] = {
                "email": email,
                "smtp_server": smtp_server,
                "enabled": True,
                "configured_at": datetime.now().isoformat()
            }
            self._save_config()
            
            return {
                "status": "success",
                "message": "Email integration configured"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def setup_cloud_storage(self, provider: str = "onedrive") -> Dict:
        """Setup cloud storage integration"""
        
        try:
            self.cloud_storage = CloudStorageIntegration(provider)
            
            self.config["cloud_storage"] = {
                "provider": provider,
                "enabled": True,
                "configured_at": datetime.now().isoformat()
            }
            self._save_config()
            
            return {
                "status": "success",
                "message": f"{provider} integration configured"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_integration_status(self) -> Dict:
        """Get status of all integrations"""
        
        return {
            "email": {
                "enabled": bool(self.email),
                "configured": bool(self.config.get("email"))
            },
            "cloud_storage": {
                "enabled": bool(self.cloud_storage),
                "configured": bool(self.config.get("cloud_storage")),
                "provider": self.config.get("cloud_storage", {}).get("provider")
            },
            "webhooks": {
                "enabled": True,
                "registered_count": len(self.webhooks.webhooks)
            }
        }
    
    def execute_integration_command(self, integration: str, 
                                   command: str, params: Dict) -> Dict:
        """
        Execute command on specific integration
        
        Examples:
        - integration: "email", command: "send", params: {...}
        - integration: "cloud", command: "upload", params: {...}
        """
        
        if integration == "email":
            if not self.email:
                return {
                    "status": "error",
                    "message": "Email integration not configured"
                }
            
            if command == "send":
                return self.email.send_email(**params)
            elif command == "send_bulk":
                return self.email.send_bulk_email(**params)
        
        elif integration == "cloud":
            if not self.cloud_storage:
                return {
                    "status": "error",
                    "message": "Cloud storage integration not configured"
                }
            
            if command == "upload":
                return self.cloud_storage.upload_file(**params)
            elif command == "download":
                return self.cloud_storage.download_file(**params)
            elif command == "list":
                return self.cloud_storage.list_files(**params)
        
        elif integration == "webhook":
            if command == "register":
                return self.webhooks.register_webhook(**params)
            elif command == "send":
                return self.webhooks.send_webhook(**params)
        
        return {
            "status": "error",
            "message": "Unknown integration or command"
        }
