"""
Odoo XML-RPC Client
"""
import xmlrpc.client
from typing import List, Dict, Any, Optional
from functools import lru_cache
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class OdooClient:
    """Odoo XML-RPC Client wrapper"""

    def __init__(self):
        self.url = settings.odoo_url
        self.db = settings.odoo_db
        self.username = settings.odoo_username
        self.password = settings.odoo_password
        self._uid: Optional[int] = None

        # XML-RPC endpoints
        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")

    @property
    def uid(self) -> int:
        """Get authenticated user ID (cached)"""
        if self._uid is None:
            self._uid = self.authenticate()
        return self._uid

    def authenticate(self) -> int:
        """Authenticate with Odoo"""
        try:
            uid = self.common.authenticate(
                self.db, self.username, self.password, {}
            )
            if not uid:
                raise ValueError("Authentication failed")
            logger.info(f"Authenticated with Odoo as user ID: {uid}")
            return uid
        except Exception as e:
            logger.error(f"Odoo authentication error: {e}")
            raise

    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        """Authenticate specific user"""
        try:
            uid = self.common.authenticate(self.db, username, password, {})
            return uid if uid else None
        except Exception as e:
            logger.error(f"User authentication error: {e}")
            return None

    def execute(self, model: str, method: str, *args, **kwargs) -> Any:
        """Execute Odoo model method"""
        try:
            return self.models.execute_kw(
                self.db, self.uid, self.password, model, method, args, kwargs
            )
        except Exception as e:
            logger.error(f"Odoo execute error: {model}.{method} - {e}")
            raise

    def search(self, model: str, domain: List, **kwargs) -> List[int]:
        """Search records"""
        return self.execute(model, "search", domain, kwargs)

    def read(self, model: str, ids: List[int], fields: Optional[List[str]] = None) -> List[Dict]:
        """Read records"""
        kwargs = {"fields": fields} if fields else {}
        return self.execute(model, "read", ids, kwargs)

    def search_read(
        self, model: str, domain: List, fields: Optional[List[str]] = None, **kwargs
    ) -> List[Dict]:
        """Search and read records"""
        search_kwargs = {**kwargs}
        if fields:
            search_kwargs["fields"] = fields
        return self.execute(model, "search_read", domain, search_kwargs)

    def create(self, model: str, values: Dict) -> int:
        """Create record"""
        return self.execute(model, "create", values)

    def write(self, model: str, ids: List[int], values: Dict) -> bool:
        """Update records"""
        return self.execute(model, "write", ids, values)

    def unlink(self, model: str, ids: List[int]) -> bool:
        """Delete records"""
        return self.execute(model, "unlink", ids)

    def get_user_info(self, uid: int) -> Dict:
        """Get user information"""
        users = self.read("res.users", [uid], ["name", "login", "email"])
        return users[0] if users else {}

    def check_user_pin(self, uid: int, pin: str) -> bool:
        """
        Check user PIN code
        Note: This requires custom field 'x_pin' on res.users
        If not exists, you'll need to create it in Odoo or modify logic
        """
        try:
            users = self.read("res.users", [uid], ["x_pin"])
            if users and users[0].get("x_pin"):
                return users[0]["x_pin"] == pin
            # If no PIN field, accept any 4-digit PIN for testing
            logger.warning(f"No PIN field found for user {uid}, accepting any PIN")
            return len(pin) == 4
        except Exception as e:
            logger.error(f"Error checking PIN: {e}")
            # Fallback: accept any 4-digit PIN
            return len(pin) == 4


# Global Odoo client instance
@lru_cache()
def get_odoo_client() -> OdooClient:
    """Get cached Odoo client instance"""
    return OdooClient()
