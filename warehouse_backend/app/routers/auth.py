"""
Authentication endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
import logging

from app.models.auth import (
    LoginRequest, LoginResponse, VerifyPinRequest,
    VerifyPinResponse, UserInfo, TokenData
)
from app.services.odoo_client import get_odoo_client, OdooClient
from app.dependencies.auth import create_access_token, get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    odoo: OdooClient = Depends(get_odoo_client)
):
    """
    Login with username and password
    Returns JWT access token
    """
    try:
        # Authenticate with Odoo
        uid = odoo.authenticate_user(request.username, request.password)

        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="НЕКОРЕКТНИЙ ЛОГІН АБО ПАРОЛЬ"
            )

        # Get user info
        user_info = odoo.get_user_info(uid)

        # Create access token
        token_data = {
            "user_id": uid,
            "username": request.username,
            "odoo_uid": uid
        }
        access_token = create_access_token(token_data)

        logger.info(f"User {request.username} logged in successfully")

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=uid,
            username=request.username,
            name=user_info.get("name", request.username)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post("/verify-pin", response_model=VerifyPinResponse)
async def verify_pin(
    request: VerifyPinRequest,
    current_user: TokenData = Depends(get_current_active_user),
    odoo: OdooClient = Depends(get_odoo_client)
):
    """
    Verify user PIN code
    Requires authentication token
    """
    try:
        # Check PIN in Odoo
        is_valid = odoo.check_user_pin(current_user.odoo_uid, request.pin)

        if not is_valid:
            return VerifyPinResponse(
                success=False,
                message="ПІН КОД НЕ ВІРНИЙ"
            )

        logger.info(f"PIN verified for user {current_user.username}")

        return VerifyPinResponse(
            success=True,
            message="PIN verified successfully"
        )

    except Exception as e:
        logger.error(f"PIN verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error verifying PIN"
        )


@router.post("/logout")
async def logout(current_user: TokenData = Depends(get_current_active_user)):
    """
    Logout user
    Note: JWT tokens are stateless, so this is just for logging purposes
    Client should discard the token
    """
    logger.info(f"User {current_user.username} logged out")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_active_user),
    odoo: OdooClient = Depends(get_odoo_client)
):
    """
    Get current user information
    """
    try:
        user_info = odoo.get_user_info(current_user.odoo_uid)

        return UserInfo(
            id=current_user.user_id,
            username=current_user.username,
            name=user_info.get("name", current_user.username),
            email=user_info.get("email")
        )

    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user information"
        )
