from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from api.database import get_db
from api.services import ai_service

router = APIRouter(
    prefix="/ai",
    tags=["Inteligencia Artificial"]
)

class AIConfigRequest(BaseModel):
    provider: str
    api_key: Optional[str] = ""
    model: Optional[str] = ""
    base_url: Optional[str] = ""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    system_prompt: Optional[str] = None
    lang: Optional[str] = "es"

@router.get("/config")
def get_ai_config():
    """Obtiene la configuración actual y los proveedores disponibles"""
    curr_key = ai_service.AI_CONFIG.get("api_key", "")
    masked_key = f"{curr_key[:4]}...{curr_key[-4:]}" if len(curr_key) > 8 else ("****" if curr_key else "")

    return {
        "current": {
            "provider": ai_service.AI_CONFIG["provider"],
            "model": ai_service.AI_CONFIG["model"],
            "base_url": ai_service.AI_CONFIG["base_url"],
            "has_key": bool(curr_key),
            "masked_key": masked_key
        },
        "providers": ai_service.PROVIDERS_INFO
    }

@router.post("/config")
def update_ai_config(config: AIConfigRequest):
    """Actualiza el motor de Inteligencia Artificial (Local o Nube)"""
    if config.provider not in ai_service.PROVIDERS_INFO:
        raise HTTPException(status_code=400, detail=f"Proveedor no soportado: {config.provider}")

    ai_service.AI_CONFIG["provider"] = config.provider
    if config.api_key is not None:
        ai_service.AI_CONFIG["api_key"] = config.api_key.strip()
    
    # Si el usuario no especificó modelo, tomar el default del proveedor
    default_model = ai_service.PROVIDERS_INFO[config.provider].get("default_model", "")
    ai_service.AI_CONFIG["model"] = config.model.strip() if config.model else default_model

    # Si el usuario no especificó base_url, tomar la default
    default_url = ai_service.PROVIDERS_INFO[config.provider].get("default_url", "")
    ai_service.AI_CONFIG["base_url"] = config.base_url.strip() if config.base_url else default_url

    # Persistir configuración en disco
    ai_service.save_ai_config(ai_service.AI_CONFIG)

    return {
        "message": f"Configuración de IA actualizada a '{ai_service.PROVIDERS_INFO[config.provider]['name']}'",
        "provider": ai_service.AI_CONFIG["provider"],
        "model": ai_service.AI_CONFIG["model"]
    }

@router.get("/reporte")
async def get_ai_report(lang: str = "es", db: Session = Depends(get_db)):
    """Genera un reporte analítico de negocio con el modelo de IA seleccionado"""
    return await ai_service.generate_ai_report(db, lang=lang)

@router.post("/chat")
async def chat_with_assistant(req: ChatRequest, db: Session = Depends(get_db)):
    """Chat interactivo con el Asistente Virtual, inyectando contexto vivo de la base de datos"""
    summary = ai_service.get_db_summary(db)
    is_en = (req.lang or "es").lower() == "en"

    if is_en:
        system_context = f"""
You are the Virtual Assistant of SAD ERP, an analytical AI agent integrated into the enterprise platform.
Your role is to assist managers and staff by answering questions about inventory, sales, customers, and business strategy.

Real-time business database context:
- Total Revenue: ${summary['total_ingresos']:,.2f} USD ({summary['num_ventas']} transactions).
- Average Ticket per Sale: ${summary['ticket_promedio']:,.2f} USD.
- Total Products in Catalog: {summary['total_productos']}.
- Low Stock Alerts (< 5 units): {summary['productos_stock_critico']}.
- Out of Stock Items: {summary['productos_agotados']}.
- Best-selling Product: {summary['producto_estrella']}.
- Catalog Sample: {summary['catalogo_muestra']}.
- Recent Transactions: {summary['ultimas_ventas']}.

Response Guidelines:
1. Always respond professionally, concisely, and empathetically in English.
2. Ground all answers in the real numbers provided above when asked about figures.
3. If requested to draft emails or suggest commercial actions, be proactive, executive, and structured.
4. Use Markdown formatting (bolding, lists, bullet points) for maximum readability.
"""
    else:
        system_context = f"""
Eres el Asistente Virtual del ERP SAD, un agente analítico integrado en la plataforma.
Tu rol es asistir al administrador y empleados respondiendo dudas sobre inventario, ventas, clientes y estrategia comercial.

Contexto en tiempo real de la base de datos empresarial:
- Ingresos Totales: ${summary['total_ingresos']:,.2f} USD ({summary['num_ventas']} transacciones).
- Ticket promedio por venta: ${summary['ticket_promedio']:,.2f} USD.
- Total de productos: {summary['total_productos']}.
- Alertas de Stock Bajo (< 5 unidades): {summary['productos_stock_critico']}.
- Productos Agotados: {summary['productos_agotados']}.
- Producto más vendido: {summary['producto_estrella']}.
- Muestra de catálogo reciente: {summary['catalogo_muestra']}.
- Últimas ventas: {summary['ultimas_ventas']}.

Pautas de respuesta:
1. Responde de manera profesional, concisa y empática en español.
2. Si te preguntan sobre datos concretos (ventas, stock, ingresos), usa las cifras reales provistas arriba.
3. Si te piden redactar un correo o sugerir una acción comercial, sé proactivo y creativo con un tono ejecutivo.
4. Usa formato Markdown (negritas, listas, viñetas) para facilitar la lectura.
"""

    formatted_messages = [{"role": "system", "content": system_context}]
    for msg in req.messages:
        formatted_messages.append({"role": msg.role, "content": msg.content})

    ai_reply = await ai_service.call_llm(formatted_messages, lang=req.lang or "es")

    return {
        "reply": ai_reply,
        "provider": ai_service.AI_CONFIG["provider"],
        "model": ai_service.AI_CONFIG["model"]
    }
