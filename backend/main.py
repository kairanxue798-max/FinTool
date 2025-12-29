from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
from typing import Dict, List, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from services.financial_statements import FinancialStatementGenerator
from services.ai_agent import AIAgent
from services.kpi_calculator import KPICalculator
from services.fx_rate_service import FXRateService
from services.kpi_calculator import KPICalculator
from services.fx_rate_service import FXRateService

load_dotenv()

app = FastAPI(title="Financial Statement Generator API", version="1.0.0")

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
statement_generator = FinancialStatementGenerator()
ai_agent = AIAgent()
kpi_calculator = KPICalculator()
fx_service = FXRateService()
kpi_calculator = KPICalculator()
fx_service = FXRateService()


class FinancialData(BaseModel):
    data: Dict


class VarianceAnalysisRequest(BaseModel):
    current_period: Dict
    previous_period: Dict
    period_name: str


class KPIAnalysisRequest(BaseModel):
    financial_data: Dict
    kpi_targets: Dict


class ChatRequest(BaseModel):
    message: str
    financial_data: Optional[Dict] = None
    transactions: Optional[List[Dict]] = None
    conversation_history: Optional[List[Dict]] = None
    entity: Optional[str] = None


class EntityRequest(BaseModel):
    transactions: List[Dict]
    entity: Optional[str] = None


class KPICalculationRequest(BaseModel):
    transactions: List[Dict]
    entity: Optional[str] = None
    as_of_date: Optional[str] = None
    period_days: Optional[int] = 30


class FXRateRequest(BaseModel):
    base_currency: str = "USD"
    date: Optional[str] = None


class FXConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    date: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Financial Statement Generator API"}


@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload and parse CSV file containing financial transactions
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate required columns
        required_columns = ['date', 'account', 'amount', 'type']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Process and return parsed data
        transactions = df.to_dict('records')
        
        return JSONResponse({
            "success": True,
            "message": "CSV uploaded successfully",
            "transactions": transactions,
            "row_count": len(transactions)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-statements")
async def generate_statements(data: FinancialData):
    """
    Generate Balance Sheet, Profit & Loss, and Cash Flow statements
    """
    try:
        transactions = data.data.get('transactions', [])
        
        if not transactions:
            raise HTTPException(status_code=400, detail="No transactions provided")
        
        # Generate all financial statements
        balance_sheet = statement_generator.generate_balance_sheet(transactions)
        profit_loss = statement_generator.generate_profit_loss(transactions)
        cash_flow = statement_generator.generate_cash_flow(transactions)
        
        return JSONResponse({
            "success": True,
            "balance_sheet": balance_sheet,
            "profit_loss": profit_loss,
            "cash_flow": cash_flow
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ai/variance-analysis")
async def variance_analysis(request: VarianceAnalysisRequest):
    """
    AI-powered variance analysis comparing current vs previous period
    """
    try:
        analysis = await ai_agent.analyze_variance(
            current_period=request.current_period,
            previous_period=request.previous_period,
            period_name=request.period_name
        )
        
        return JSONResponse({
            "success": True,
            "analysis": analysis
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ai/kpi-analysis")
async def kpi_analysis(request: KPIAnalysisRequest):
    """
    AI-powered KPI achievement analysis
    """
    try:
        analysis = await ai_agent.analyze_kpi_achievement(
            financial_data=request.financial_data,
            kpi_targets=request.kpi_targets
        )
        
        return JSONResponse({
            "success": True,
            "analysis": analysis
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ai/chat")
async def ai_chat(request: ChatRequest):
    """
    Conversational AI agent for financial analysis - handles any financial-related questions
    """
    try:
        response = await ai_agent.chat(
            message=request.message,
            financial_data=request.financial_data,
            transactions=request.transactions,
            conversation_history=request.conversation_history,
            entity=request.entity
        )
        
        return JSONResponse({
            "success": True,
            "response": response.get("response", ""),
            "data": response
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/entities")
async def get_entities(data: FinancialData):
    """
    Extract unique entities/subsidiaries from transactions
    """
    try:
        transactions = data.data.get('transactions', [])
        if not transactions:
            return JSONResponse({"entities": []})
        
        entities = set()
        for transaction in transactions:
            entity = transaction.get('entity') or transaction.get('subsidiary') or transaction.get('company')
            if entity:
                entities.add(entity)
        
        return JSONResponse({
            "success": True,
            "entities": sorted(list(entities))
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/kpi/ar-aging")
async def calculate_ar_aging(request: KPICalculationRequest):
    """
    Calculate Accounts Receivable Aging Report
    """
    try:
        result = kpi_calculator.calculate_ar_aging(
            transactions=request.transactions,
            as_of_date=request.as_of_date
        )
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/kpi/dso")
async def calculate_dso(request: KPICalculationRequest):
    """
    Calculate Days Sales Outstanding (DSO)
    """
    try:
        result = kpi_calculator.calculate_dso(
            transactions=request.transactions,
            period_days=request.period_days or 30
        )
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/kpi/revenue-ytd")
async def calculate_revenue_ytd(request: EntityRequest):
    """
    Calculate Year-to-Date Revenue
    """
    try:
        result = kpi_calculator.calculate_revenue_ytd(
            transactions=request.transactions,
            entity=request.entity
        )
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/kpi/revenue-variance")
async def calculate_revenue_variance(request: EntityRequest):
    """
    Calculate revenue variance vs previous month
    """
    try:
        result = kpi_calculator.calculate_revenue_variance(
            transactions=request.transactions,
            entity=request.entity
        )
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/kpi/trailing-3m")
async def calculate_trailing_3m(request: EntityRequest):
    """
    Calculate trailing 3 months rolling revenue
    """
    try:
        result = kpi_calculator.calculate_trailing_3m_revenue(
            transactions=request.transactions,
            entity=request.entity
        )
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/kpi/top-n")
async def get_top_n_revenue(request: EntityRequest):
    """
    Get TOP N revenue transactions
    """
    try:
        n = 10  # Default
        entity = request.entity if isinstance(request.entity, str) else None
        
        result = kpi_calculator.find_top_n_revenue(
            transactions=request.transactions,
            n=n,
            entity=entity
        )
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/kpi/unusual-transactions")
async def find_unusual_transactions(request: EntityRequest):
    """
    Find unusual transactions (e.g., weekend postings)
    """
    try:
        result = kpi_calculator.find_unusual_transactions(
            transactions=request.transactions,
            entity=request.entity
        )
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fx/rates")
async def get_fx_rates(base_currency: str = "USD", date: Optional[str] = None):
    """
    Get foreign exchange rates (current or historical)
    """
    try:
        if date:
            result = fx_service.get_historical_rates(date, base_currency)
        else:
            result = fx_service.get_current_rates(base_currency)
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fx/ato-rates")
async def get_ato_fx_rates(year: str, month: str):
    """
    Get FX rates from Australian Tax Office (ATO) website
    """
    try:
        result = fx_service.get_ato_rates(year, month)
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fx/convert")
async def convert_currency(request: FXConvertRequest):
    """
    Convert currency amount
    """
    try:
        result = fx_service.convert_currency(
            amount=request.amount,
            from_currency=request.from_currency,
            to_currency=request.to_currency,
            date=request.date
        )
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

