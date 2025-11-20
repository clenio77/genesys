"""
Extrator de Processos de Tribunais usando Playwright
Baseado na infraestrutura do Kermartin
"""

import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, List
import re

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.utils.logger import bot_telegram_logger as logger

try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright não instalado. Execute: pip install playwright && playwright install")


class TribunalExtractor:
    """Extrai dados de processos diretamente dos sites dos tribunais usando Playwright"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
        
    async def iniciar_browser(self):
        """Inicia o browser Playwright"""
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright não está instalado")
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ]
        )
        logger.info("✅ Browser Playwright iniciado")
    
    async def fechar_browser(self):
        """Fecha o browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Browser fechado")
    
    async def extrair_processo_tjmg(self, numero_processo: str) -> Optional[Dict]:
        """
        Extrai dados de processo diretamente do site do TJMG
        
        Args:
            numero_processo: Número CNJ do processo
            
        Returns:
            Dict com dados do processo ou None
        """
        if not self.browser:
            await self.iniciar_browser()
        
        try:
            page = await self.browser.new_page()
            
            # URL de consulta pública do TJMG
            url = "https://www8.tjmg.jus.br/consultas/consulta.do"
            
            logger.info(f"🌐 Acessando TJMG: {numero_processo}")
            
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(2)
            
            # Preencher número do processo
            # NOTA: Os seletores precisam ser verificados no site real
            try:
                # Tentar diferentes seletores possíveis
                seletores_numero = [
                    '#numeroProcesso',
                    '#numero',
                    'input[name="numeroProcesso"]',
                    'input[type="text"]'
                ]
                
                preenchido = False
                for seletor in seletores_numero:
                    try:
                        await page.fill(seletor, numero_processo)
                        preenchido = True
                        logger.debug(f"Preenchido com seletor: {seletor}")
                        break
                    except:
                        continue
                
                if not preenchido:
                    logger.warning("Não foi possível encontrar campo do processo")
                    await page.close()
                    return None
                
                # Clicar no botão de consultar
                await page.click('button[type="submit"], #btnConsultar, input[type="submit"]')
                
                # Aguardar resultados (ajustar timeout conforme necessário)
                await page.wait_for_selector('.resultado, .processo, .dados-processo', timeout=15000)
                await asyncio.sleep(3)  # Aguardar carregamento completo
                
                # Extrair dados usando JavaScript
                dados = await page.evaluate("""
                    () => {
                        const resultado = {
                            numero: '',
                            classe: '',
                            assunto: '',
                            partes: [],
                            movimentacoes: [],
                            status: ''
                        };
                        
                        // Tentar extrair número
                        const numeroEl = document.querySelector('.numero-processo, .numero, [data-field="numero"]');
                        if (numeroEl) resultado.numero = numeroEl.innerText.trim();
                        
                        // Tentar extrair classe
                        const classeEl = document.querySelector('.classe, .tipo-processo, [data-field="classe"]');
                        if (classeEl) resultado.classe = classeEl.innerText.trim();
                        
                        // Tentar extrair partes
                        const partesEls = document.querySelectorAll('.parte, .participante, [data-field="parte"]');
                        partesEls.forEach(el => {
                            resultado.partes.push(el.innerText.trim());
                        });
                        
                        // Tentar extrair movimentações
                        const movEls = document.querySelectorAll('.movimentacao, .historico-item, [data-field="movimentacao"]');
                        movEls.forEach(el => {
                            const dataEl = el.querySelector('.data, .data-movimentacao');
                            const tipoEl = el.querySelector('.tipo, .tipo-movimentacao');
                            const descEl = el.querySelector('.descricao, .texto-movimentacao');
                            
                            resultado.movimentacoes.push({
                                data: dataEl ? dataEl.innerText.trim() : '',
                                tipo: tipoEl ? tipoEl.innerText.trim() : '',
                                descricao: descEl ? descEl.innerText.trim() : ''
                            });
                        });
                        
                        return resultado;
                    }
                """)
                
                await page.close()
                
                if dados.get('numero'):
                    logger.info(f"✅ Processo extraído: {dados['numero']}")
                    dados['fonte'] = 'TJMG (Playwright)'
                    dados['data_consulta'] = datetime.now().isoformat()
                    return dados
                else:
                    logger.warning("Dados do processo não encontrados")
                    return None
                
            except Exception as e:
                logger.error(f"Erro ao extrair dados: {e}")
                await page.close()
                return None
                
        except Exception as e:
            logger.error(f"Erro ao acessar TJMG: {e}")
            return None
    
    async def extrair_processo_geral(self, numero_processo: str, tribunal_alias: str) -> Optional[Dict]:
        """
        Extrai processo usando URL genérica baseada no tribunal
        
        Args:
            numero_processo: Número CNJ
            tribunal_alias: Alias do tribunal (tjmg, tjsp, etc.)
            
        Returns:
            Dict com dados ou None
        """
        # Mapear alias para URLs
        urls_tribunais = {
            'tjmg': 'https://www8.tjmg.jus.br/consultas/consulta.do',
            'tjsp': 'https://esaj.tjsp.jus.br/cpopg/search.do',
            'trf1': 'https://pje.trf1.jus.br/consultaprocessual/consultarProcesso',
            # Adicionar mais conforme necessário
        }
        
        url = urls_tribunais.get(tribunal_alias.lower())
        if not url:
            logger.warning(f"URL não encontrada para tribunal: {tribunal_alias}")
            return None
        
        if tribunal_alias.lower() == 'tjmg':
            return await self.extrair_processo_tjmg(numero_processo)
        else:
            logger.info(f"Extrator para {tribunal_alias} ainda não implementado")
            return None
    
    async def __aenter__(self):
        """Context manager entry"""
        if not self.browser:
            await self.iniciar_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.fechar_browser()


# Instância global (usar com context manager ou iniciar manualmente)
tribunal_extractor = TribunalExtractor()

