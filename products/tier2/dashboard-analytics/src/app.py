"""
Dashboard Analítico Jurídico Principal
Gera KPIs, relatórios e visualizações
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from fastapi import FastAPI, Query, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Adiciona paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "tier1" / "shared"))

from shared.middleware.security import configure_cors_seguro, add_security_middleware
from shared.middleware.rate_limit import rate_limit_dependency
from shared.middleware.cache import init_cache, cached_response
from shared.utils.logger import setup_logger

from src.config import Config
from src.services.aggregator import DataAggregator
from src.services.kpi_calculator import KPICalculator
from src.services.report_generator import ReportGenerator
from src.services.visualization import VisualizationEngine

# Setup
logger = setup_logger("dashboard_analytics", "dashboard_analytics.log")
app = FastAPI(title="Genesys Analytics Dashboard", version="1.0.0")

# Configure security
configure_cors_seguro(
    app,
    allowed_origins=[
        "https://genesys.com.br",
        "https://analytics.genesys.com.br",
        "http://localhost:3000"
    ]
)
add_security_middleware(app)

# Initialize cache
init_cache(Config.REDIS_URL)

# Initialize services
aggregator = DataAggregator()
kpi_calculator = KPICalculator()
report_generator = ReportGenerator()
visualizer = VisualizationEngine()


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "service": "Genesys Analytics Dashboard",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy"}


@app.get("/api/kpis")
@cached_response(ttl=60)  # Cache por 1 minuto
async def get_kpis(
    time_window: str = Query("today", description="Time window: today, 7d, 30d, 90d, 365d"),
    request: Request = None,
    _ = Depends(rate_limit_dependency())
):
    """
    Retorna KPIs em tempo real
    """
    try:
        kpis = kpi_calculator.calculate_all(time_window)
        return JSONResponse(content=kpis)
    
    except Exception as e:
        logger.error(f"Error calculating KPIs: {e}")
        return JSONResponse(
            content={"error": "Error calculating KPIs"},
            status_code=500
        )


@app.get("/api/kpis/{kpi_name}")
@cached_response(ttl=60)
async def get_kpi(
    kpi_name: str,
    time_window: str = Query("today"),
    request: Request = None
):
    """Retorna KPI específico"""
    
    try:
        kpi_value = kpi_calculator.calculate_single(kpi_name, time_window)
        return JSONResponse(content={kpi_name: kpi_value})
    
    except Exception as e:
        logger.error(f"Error calculating KPI {kpi_name}: {e}")
        return JSONResponse(
            content={"error": f"Error calculating KPI: {kpi_name}"},
            status_code=500
        )


@app.get("/api/charts")
@cached_response(ttl=120)  # Cache por 2 minutos
async def get_charts_data(
    chart_type: str = Query(..., description="Chart type: process_status, revenue_trend, deadline_alerts"),
    time_window: str = Query("30d"),
    request: Request = None,
    _ = Depends(rate_limit_dependency())
):
    """Retorna dados para visualização"""
    
    try:
        chart_data = visualizer.generate_chart(chart_type, time_window)
        return JSONResponse(content=chart_data)
    
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        return JSONResponse(
            content={"error": f"Error generating chart: {chart_type}"},
            status_code=500
        )


@app.get("/api/reports")
@cached_response(ttl=300)  # Cache por 5 minutos
async def list_reports(request: Request = None):
    """Lista relatórios disponíveis"""
    
    try:
        reports = report_generator.list_reports()
        return JSONResponse(content={"reports": reports})
    
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        return JSONResponse(
            content={"error": "Error listing reports"},
            status_code=500
        )


@app.post("/api/reports/generate")
async def generate_report(
    report_type: str,
    time_window: str = Query("30d"),
    request: Request = None,
    _ = Depends(rate_limit_dependency(max_requests=10, window_seconds=60))
):
    """Gera relatório"""
    
    try:
        report = report_generator.generate(report_type, time_window)
        return JSONResponse(content=report)
    
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return JSONResponse(
            content={"error": f"Error generating report: {report_type}"},
            status_code=500
        )


@app.get("/api/alerts")
async def get_alerts(request: Request = None):
    """Retorna alertas ativos"""
    
    try:
        alerts = aggregator.get_active_alerts()
        return JSONResponse(content={"alerts": alerts})
    
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return JSONResponse(
            content={"error": "Error getting alerts"},
            status_code=500
        )


@app.get("/api/analytics/summary")
@cached_response(ttl=180)
async def get_analytics_summary(
    request: Request = None,
    _ = Depends(rate_limit_dependency())
):
    """Retorna resumo de analytics"""
    
    try:
        summary = aggregator.get_summary()
        return JSONResponse(content=summary)
    
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return JSONResponse(
            content={"error": "Error getting analytics summary"},
            status_code=500
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)

