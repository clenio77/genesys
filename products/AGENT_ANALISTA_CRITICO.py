"""
🧠 AGENTE ANALISTA CRÍTICO - METHOD-BMAD
Fiscal da aplicação - Revisa arquitetura e implementação
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Issue:
    """Representa um problema encontrado"""
    tipo: str  # 'arquitetura', 'segurança', 'performance', 'código'
    severidade: str  # 'critica', 'alta', 'media', 'baixa'
    descricao: str
    local: str
    sugestao: str


class AnalistaCritico:
    """
    Agente analista crítico que revisa a aplicação
    
    Funciona como um "fiscal" que:
    - Analisa arquitetura (BACKEND, MODELO, API, DATA)
    - Revisa código em busca de issues
    - Valida boas práticas
    - Sugere melhorias
    """
    
    def __init__(self):
        self.issues: List[Issue] = []
        self.score = 0
        self.max_score = 100
    
    def analisar_arquitetura(self, produto: Dict) -> List[Issue]:
        """
        Analisa a arquitetura do produto usando METHOD-BMAD
        
        Args:
            produto: Dict com estrutura do produto
        
        Returns:
            Lista de issues encontradas
        """
        issues = []
        
        # Verificar BACKEND
        if not self._validar_backend(produto.get('backend', {})):
            issues.append(Issue(
                tipo='arquitetura',
                severidade='alta',
                descricao='Backend não está bem estruturado ou está faltando',
                local='Backend (B)',
                sugestao='Estruture o backend com camadas claras: controllers, services, repositories'
            ))
        
        # Verificar MODELO/MICROSERVICES
        if not self._validar_modelo(produto.get('modelo', {})):
            issues.append(Issue(
                tipo='arquitetura',
                severidade='media',
                descricao='Modelo/Microservices não está bem definido',
                local='Modelo (M)',
                sugestao='Defina microserviços claramente com responsabilidades únicas'
            ))
        
        # Verificar API/APLICATIVO
        if not self._validar_api(produto.get('api', {})):
            issues.append(Issue(
                tipo='arquitetura',
                severidade='alta',
                descricao='API não está completa ou bem documentada',
                local='API/Aplicativo (A)',
                sugestao='Documente todos os endpoints com OpenAPI/Swagger'
            ))
        
        # Verificar DATA/DOCUMENTO
        if not self._validar_data(produto.get('data', {})):
            issues.append(Issue(
                tipo='arquitetura',
                severidade='critica',
                descricao='Estrutura de dados não está bem definida',
                local='Data/Documento (D)',
                sugestao='Defina schema completo do banco de dados com migrations'
            ))
        
        self.issues.extend(issues)
        return issues
    
    def analisar_codigo(self, codigo: str) -> List[Issue]:
        """
        Analisa código em busca de problemas
        
        Args:
            codigo: String com o código a analisar
        
        Returns:
            Lista de issues encontradas
        """
        issues = []
        
        # Verificar imports
        if 'import *' in codigo:
            issues.append(Issue(
                tipo='código',
                severidade='media',
                descricao='Uso de import * é anti-pattern',
                local='Imports',
                sugestao='Use imports explícitos: from module import specific_function'
            ))
        
        # Verificar segurança
        if 'eval(' in codigo or 'exec(' in codigo:
            issues.append(Issue(
                tipo='segurança',
                severidade='critica',
                descricao='Uso de eval/exec é vulnerabilidade crítica',
                local='Código',
                sugestao='Nunca use eval ou exec com dados do usuário'
            ))
        
        # Verificar SQL injection
        if '+' in codigo and 'SQL' in codigo:
            issues.append(Issue(
                tipo='segurança',
                severidade='critica',
                descricao='Possível SQL injection com concatenação',
                local='Queries',
                sugestao='Use prepared statements ou ORM'
            ))
        
        # Verificar duplicação de código
        lines = codigo.split('\n')
        if len(set(lines)) < len(lines) * 0.7:
            issues.append(Issue(
                tipo='código',
                severidade='baixa',
                descricao='Alta duplicação de código detectada',
                local='Código geral',
                sugestao='Refatore para remover duplicação (DRY principle)'
            ))
        
        self.issues.extend(issues)
        return issues
    
    def analisar_seguranca(self, aplicacao: Dict) -> List[Issue]:
        """Analisa aspectos de segurança"""
        issues = []
        
        # Verificar autenticação
        if not aplicacao.get('autenticacao'):
            issues.append(Issue(
                tipo='segurança',
                severidade='critica',
                descricao='Sistema sem autenticação',
                local='Autenticação',
                sugestao='Implemente JWT ou OAuth2'
            ))
        
        # Verificar rate limiting
        if not aplicacao.get('rate_limiting'):
            issues.append(Issue(
                tipo='segurança',
                severidade='alta',
                descricao='Sem rate limiting - vulnerável a DDoS',
                local='API',
                sugestao='Implemente rate limiting (ex: Redis)'
            ))
        
        # Verificar CORS
        if aplicacao.get('cors') == '*':
            issues.append(Issue(
                tipo='segurança',
                severidade='media',
                descricao='CORS muito permissivo',
                local='Configuração',
                sugestao='Configure CORS específico para domínios permitidos'
            ))
        
        # Verificar encriptação
        if not aplicacao.get('https_obrigatorio'):
            issues.append(Issue(
                tipo='segurança',
                severidade='alta',
                descricao='HTTPS não obrigatório',
                local='Configuração',
                sugestao='Force HTTPS em produção'
            ))
        
        self.issues.extend(issues)
        return issues
    
    def analisar_performance(self, aplicacao: Dict) -> List[Issue]:
        """Analisa aspectos de performance"""
        issues = []
        
        # Verificar cache
        if not aplicacao.get('cache'):
            issues.append(Issue(
                tipo='performance',
                severidade='alta',
                descricao='Sistema sem cache',
                local='Performance',
                sugestao='Implemente Redis ou cache em memória'
            ))
        
        # Verificar queries N+1
        if aplicacao.get('possivel_n_plus_1'):
            issues.append(Issue(
                tipo='performance',
                severidade='alta',
                descricao='Possível problema de queries N+1',
                local='Database',
                sugestao='Use eager loading ou joins'
            ))
        
        # Verificar paginação
        if not aplicacao.get('paginacao'):
            issues.append(Issue(
                tipo='performance',
                severidade='media',
                descricao='Listas sem paginação',
                local='API',
                sugestao='Implemente paginação em todas as listagens'
            ))
        
        self.issues.extend(issues)
        return issues
    
    def gerar_relatorio(self) -> Dict:
        """
        Gera relatório completo da análise
        
        Returns:
            Dict com o relatório
        """
        # Calcular score
        self._calcular_score()
        
        # Agrupar issues por tipo
        issues_por_tipo = self._agrupar_issues()
        
        # Agrupar issues por severidade
        issues_por_severidade = self._agrupar_issues_por_severidade()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'score_total': self.score,
            'score_maximo': self.max_score,
            'percentual_aprovacao': round((self.score / self.max_score) * 100, 2),
            'total_issues': len(self.issues),
            'issues_por_tipo': issues_por_tipo,
            'issues_por_severidade': issues_por_severidade,
            'issues_criticas': self._filtrar_issues_por_severidade('critica'),
            'issues_altas': self._filtrar_issues_por_severidade('alta'),
            'recomendacoes': self._gerar_recomendacoes(),
            'aprovacao': self.score >= 80,
            'message': self._gerar_mensagem()
        }
    
    def _validar_backend(self, backend: Dict) -> bool:
        """Valida estrutura do backend"""
        return bool(
            backend.get('stack') and
            backend.get('responsabilidades') and
            len(backend.get('microservicos', [])) > 0
        )
    
    def _validar_modelo(self, modelo: Dict) -> bool:
        """Valida estrutura de modelo/microserviços"""
        return bool(
            modelo.get('microservicos') and
            len(modelo.get('microservicos', [])) > 0 and
            modelo.get('comunicacao')
        )
    
    def _validar_api(self, api: Dict) -> bool:
        """Valida estrutura da API"""
        return bool(
            api.get('endpoints') and
            len(api.get('endpoints', [])) > 0 and
            api.get('documentacao')
        )
    
    def _validar_data(self, data: Dict) -> bool:
        """Valida estrutura de dados"""
        return bool(
            data.get('database') and
            len(data.get('tabelas', [])) > 0
        )
    
    def _calcular_score(self):
        """Calcula score baseado nos issues"""
        penalizacoes = {
            'critica': 15,
            'alta': 10,
            'media': 5,
            'baixa': 2
        }
        
        score = self.max_score
        for issue in self.issues:
            score -= penalizacoes.get(issue.severidade, 0)
        
        self.score = max(0, score)
    
    def _agrupar_issues(self) -> Dict:
        """Agrupa issues por tipo"""
        grupos = {}
        for issue in self.issues:
            if issue.tipo not in grupos:
                grupos[issue.tipo] = []
            grupos[issue.tipo].append({
                'severidade': issue.severidade,
                'descricao': issue.descricao,
                'local': issue.local,
                'sugestao': issue.sugestao
            })
        return grupos
    
    def _agrupar_issues_por_severidade(self) -> Dict:
        """Agrupa issues por severidade"""
        grupos = {}
        for issue in self.issues:
            if issue.severidade not in grupos:
                grupos[issue.severidade] = []
            grupos[issue.severidade].append({
                'tipo': issue.tipo,
                'descricao': issue.descricao,
                'local': issue.local
            })
        return grupos
    
    def _filtrar_issues_por_severidade(self, severidade: str) -> List[Issue]:
        """Filtra issues por severidade"""
        return [issue for issue in self.issues if issue.severidade == severidade]
    
    def _gerar_recomendacoes(self) -> List[str]:
        """Gera recomendações baseadas nos issues"""
        recomendacoes = []
        
        # Issues críticas
        criticas = self._filtrar_issues_por_severidade('critica')
        if criticas:
            recomendacoes.append(f"🚨 URGENTE: Corrigir {len(criticas)} issue(s) crítica(s) antes do deploy")
        
        # Issues de arquitetura
        arquitetura_issues = [i for i in self.issues if i.tipo == 'arquitetura']
        if arquitetura_issues:
            recomendacoes.append("🏗️ Revisar arquitetura para melhorar escalabilidade")
        
        # Issues de segurança
        seguranca_issues = [i for i in self.issues if i.tipo == 'segurança']
        if seguranca_issues:
            recomendacoes.append("🔒 Implementar melhorias de segurança")
        
        # Issues de performance
        performance_issues = [i for i in self.issues if i.tipo == 'performance']
        if performance_issues:
            recomendacoes.append("⚡ Otimizar performance")
        
        if not recomendacoes:
            recomendacoes.append("✅ Código está em boa qualidade! Aprovado para deploy.")
        
        return recomendacoes
    
    def _gerar_mensagem(self) -> str:
        """Gera mensagem final de aprovação/rejeição"""
        if self.score >= 80:
            return "✅ APROVADO - Código está em boa qualidade para produção"
        elif self.score >= 60:
            return "⚠️ APROVADO COM RESERVAS - Corrigir issues críticas antes do deploy"
        else:
            return "❌ REPROVADO - Corrigir todos os issues antes de prosseguir"


# Exemplo de uso
if __name__ == "__main__":
    # Criar analista
    analista = AnalistaCritico()
    
    # Exemplo de análise de produto
    produto_exemplo = {
        'backend': {
            'stack': 'Python + FastAPI',
            'responsabilidades': ['processar mensagens', 'integrar LLM'],
            'microservicos': ['telegram-handler', 'rag-system']
        },
        'modelo': {
            'microservicos': ['handler', 'rag'],
            'comunicacao': 'HTTP'
        },
        'api': {
            'endpoints': ['/webhook', '/health'],
            'documentacao': True
        },
        'data': {
            'database': 'PostgreSQL',
            'tabelas': ['users', 'chats']
        }
    }
    
    # Analisar
    analista.analisar_arquitetura(produto_exemplo)
    analista.analisar_seguranca({
        'autenticacao': True,
        'rate_limiting': False,
        'cors': '*'
    })
    
    # Gerar relatório
    relatorio = analista.gerar_relatorio()
    print(relatorio)

