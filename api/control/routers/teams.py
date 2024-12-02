from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from typing import Annotated
from http import HTTPStatus

from api.control.database.database import get_session
from api.control.schemas.utils_schemas import Message
from api.control.settings.settings import Settings


import msal
import requests
import logging
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = Settings()

SCOPE = [
    "User.Read",
    "Chat.Read",
    "Chat.ReadWrite",
    "Chat.ReadBasic",
    "ChatMessage.Send",
    "TeamsActivity.Read"
]

tenauthority = settings.AUTHORITY + settings.TENANT_ID

msal_app = msal.ConfidentialClientApplication(
    client_id = settings.CLIENT_ID,
    client_credential = settings.CLIENT_SECRET,
    authority = tenauthority,
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{tenauthority}/oauth2/v2.0/authorize",
    tokenUrl=f"{tenauthority}/oauth2/v2.0/token"
)

router = APIRouter(prefix='/mc', tags=['mc'])

T_Session = Annotated[Session, Depends(get_session)]

@router.get("/login")
def login():

    auth_by_account = msal_app.acquire_token_by_username_password(
        scopes=SCOPE,
        username=settings.USER_MC,
        password=settings.USER_PASSWORD_MC
    )

    return {"message": "Autenticação bem-sucedida.", "access_token": auth_by_account}

@router.get("/callback")
def callback(session: T_Session, code: str):
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=settings.REDIRECT_URI
    )

    if "access_token" in result:
        session_token = result["access_token"]
        return {"message": "Autenticação bem-sucedida.", "access_token": session_token}
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Falha na autenticação: {result.get('error_description', 'Erro desconhecido')}"
        )

@router.get("/me")
def get_user_info(request: Request):
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token de acesso ausente"
        )
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao acessar a API: {response.json()}"
        )


@router.get("/list-chats")
def list_chats(request: Request):
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token de acesso ausente ou malformado."
        )

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    response = requests.get(
        "https://graph.microsoft.com/v1.0/me/chats",
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        error_detail = response.json()
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao listar chats: {error_detail}"
        )

@router.get("/list-teams")
def list_teams(request: Request):
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token de acesso ausente"
        )

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me/joinedTeams",
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao listar equipes: {response.json()}"
        )

@router.get("/list-channels")
def list_channels(request: Request, team_id: str):
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token de acesso ausente"
        )

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels",
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao listar canais: {response.json()}"
        )

from pydantic import BaseModel

class ReceiveMessageRequest(BaseModel):
    chat_id: str

@router.get("/receive-messages")
def receive_messages(request: Request, data: ReceiveMessageRequest):
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token de acesso ausente ou malformado."
        )

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"https://graph.microsoft.com/v1.0/chats/{data.chat_id}/messages",
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        return HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao receber mensagens: {response.json()}"
        )

class SendMessageRequest(BaseModel):
    chat_id: str
    message: str

@router.post("/send-message")
def send_message(request: Request, data: SendMessageRequest):
    """
    Envia uma mensagem para um chat no Microsoft Teams.

    Args:
        request (Request): O objeto de requisição contendo o token de autenticação.
        data (SendMessageRequest): Dados contendo o ID do chat e a mensagem a ser enviada.

    Returns:
        dict: Confirmação do envio da mensagem ou erro.
    """
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token de acesso ausente ou malformado."
        )

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "body": {
            "content": data.message
        }
    }

    response = requests.post(
        f"https://graph.microsoft.com/v1.0/chats/{data.chat_id}/messages",
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        return {"message": "Mensagem enviada com sucesso."}
    else:
        error_detail = response.json()
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao enviar a mensagem: {error_detail}"
        )

@router.post("/create-subscription")
async def create_subscription(request: Request):
    GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/subscriptions"
    access_token = request.headers.get("Authorization")
    if not access_token or not access_token.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token de acesso ausente ou malformado."
        )

    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    chat_id = 'CHAT ID'

    payload = {
        "changeType": "created,updated",
        "notificationUrl": "http://localhost:8000/mc/webhook",
        "resource": f"/chats/{chat_id}/messages",
        "expirationDateTime": "2024-09-11T00:00:00Z",
        "clientState": "secretClientState"
    }
    response = requests.post(GRAPH_API_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 201:
        logger.info("Assinatura de webhook criada com sucesso.")
        return JSONResponse(content={"status": "Subscription created", "subscriptionId": response.json().get("id")})
    else:
        logger.error("Erro ao criar assinatura de webhook: %s", response.json())
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro ao criar assinatura de webhook"
        )

class WbSendMessageRequest(BaseModel):
    webhook: str
    chat_id: str


@router.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        logger.info("Recebido webhook: %s", payload)
        print(payload)
        
        if "message" in payload and "body" in payload["message"]:
            message_body = payload["message"]["body"]["content"]
            if message_body == "Ativar Boas Vindas":
                chat_id = payload["conversation"]["id"]
                token = request.headers.get("Authorization")
                send_welcome_message(token, chat_id)
                
        return JSONResponse(content={"status": "success"})
    
    except Exception as e:
        logger.error("Erro ao processar o webhook: %s", str(e))
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro ao processar o webhook"
        )

def send_welcome_message(token: str, chat_id: str):
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token de acesso ausente ou malformado."
        )

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "body": {
            "content": "Iniciando Automação Boas Vindas..."
        }
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 201:
        logger.info("Mensagem de boas-vindas enviada com sucesso.")
    else:
        logger.error("Erro ao enviar mensagem de boas-vindas: %s", response.json())