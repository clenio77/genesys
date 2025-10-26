'use client'

import { FaChartLine, FaChartPie, FaChartBar, FaDatabase, FaBrain, FaArrowLeft, FaClock, FaUsers, FaTrophy, FaLightbulb } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import Link from 'next/link'
import SEOHead from '@/components/SEOHead'

export default function AnalyticsJuridicoPage() {
  const metricas = [
    {
      categoria: 'Performance Processual',
      icon: FaTrophy,
      cor: 'from-amber-500 to-orange-500',
      indicadores: [
        'Taxa de sucesso por tipo de ação',
        'Tempo médio de tramitação',
        'Valor médio de condenações',
        'Taxa de recursos procedentes'
      ]
    },
    {
      categoria: 'Produtividade da Equipe',
      icon: FaUsers,
      cor: 'from-blue-500 to-cyan-500',
      indicadores: [
        'Processos por advogado',
        'Tempo médio de resposta',
        'Taxa de cumprimento de prazos',
        'Distribuição de carga de trabalho'
      ]
    },
    {
      categoria: 'Análise Financeira',
      icon: FaChartLine,
      cor: 'from-emerald-500 to-teal-500',
      indicadores: [
        'Custos por processo',
        'ROI de ações judiciais',
        'Provisões vs. Condenações',
        'Previsão de despesas'
      ]
    },
    {
      categoria: 'Inteligência Estratégica',
      icon: FaLightbulb,
      cor: 'from-purple-500 to-pink-500',
      indicadores: [
        'Padrões de decisões',
        'Perfil de magistrados',
        'Tendências jurisprudenciais',
        'Oportunidades de teses'
      ]
    }
  ]

  const dashboards = [
    {
      nome: 'Visão Executiva',
      descricao: 'KPIs principais para tomada de decisão',
      widgets: ['Taxa de Sucesso', 'Custos Totais', 'Processos Ativos', 'Tendências']
    },
    {
      nome: 'Operacional',
      descricao: 'Métricas de produtividade e prazos',
      widgets: ['Prazos Críticos', 'Distribuição de Processos', 'Performance Individual', 'Alertas']
    },
    {
      nome: 'Estratégico',
      descricao: 'Análises preditivas e insights',
      widgets: ['Previsões', 'Análise de Riscos', 'Oportunidades', 'Benchmarking']
    }
  ]

  const tecnologias = [
    {
      nome: 'Business Intelligence',
      descricao: 'Dashboards interativos e relatórios customizados',
      aplicacao: 'Visualização de dados em tempo real'
    },
    {
      nome: 'Machine Learning',
      descricao: 'Modelos preditivos para análise de tendências',
      aplicacao: 'Previsão de resultados e custos'
    },
    {
      nome: 'Data Mining',
      descricao: 'Extração de padrões e insights ocultos',
      aplicacao: 'Descoberta de correlações e oportunidades'
    },
    {
      nome: 'Big Data',
      descricao: 'Processamento de grandes volumes de dados',
      aplicacao: 'Análise histórica e comparativa'
    }
  ]

  return (
    <>
      <SEOHead 
        title="Analytics Jurídico com IA | Genesys Tecnologia"
        description="Dashboards inteligentes e análise preditiva para gestão jurídica. Business Intelligence, Machine Learning e Big Data aplicados ao Direito."
        keywords="analytics jurídico, business intelligence direito, dashboards jurídicos, análise preditiva advocacia"
        canonical="https://genesys-tecnologia.com.br/tecnologias/analytics-juridico"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

        {/* Hero Section */}
        <section className="pt-32 pb-20 px-4 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-600/10 to-teal-600/10" />
          
          <div className="max-w-7xl mx-auto relative z-10">
            <Link 
              href="/#services"
              className="inline-flex items-center gap-2 text-cyan-400 hover:text-cyan-300 mb-8 transition-colors"
            >
              <FaArrowLeft />
              Voltar para Serviços
            </Link>

            <div className="text-center mb-16">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl mb-6">
                <FaChartLine className="text-4xl text-white" />
              </div>
              <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
                Analytics <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400">Jurídico</span>
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Transforme dados jurídicos em insights estratégicos. 
                Dashboards interativos, análise preditiva e inteligência de negócios para decisões mais assertivas.
              </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <FaChartLine className="text-4xl text-emerald-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-2">
                  Real-time
                </div>
                <p className="text-gray-400 text-sm">Atualização</p>
              </div>
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <FaDatabase className="text-4xl text-cyan-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-2">
                  100+
                </div>
                <p className="text-gray-400 text-sm">Métricas</p>
              </div>
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <FaBrain className="text-4xl text-purple-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-2">
                  IA
                </div>
                <p className="text-gray-400 text-sm">Preditiva</p>
              </div>
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <FaClock className="text-4xl text-amber-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-2">
                  24/7
                </div>
                <p className="text-gray-400 text-sm">Monitoramento</p>
              </div>
            </div>
          </div>
        </section>

        {/* Categorias de Métricas */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Categorias de Métricas
              </h2>
              <p className="text-xl text-gray-400">
                Análise completa de todos os aspectos do seu departamento jurídico
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {metricas.map((metrica, index) => {
                const Icon = metrica.icon
                return (
                  <div
                    key={index}
                    className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-emerald-500/50 transition-all group"
                  >
                    <div className="flex items-center gap-4 mb-6">
                      <div className={`w-16 h-16 bg-gradient-to-br ${metrica.cor} rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform`}>
                        <Icon className="text-3xl text-white" />
                      </div>
                      <h3 className="text-2xl font-bold text-white">
                        {metrica.categoria}
                      </h3>
                    </div>

                    <ul className="space-y-3">
                      {metrica.indicadores.map((indicador, idx) => (
                        <li key={idx} className="flex items-start gap-3">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full mt-2 flex-shrink-0" />
                          <span className="text-gray-300">{indicador}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* Dashboards */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Dashboards Inteligentes
              </h2>
              <p className="text-xl text-gray-400">
                Visualizações personalizadas para cada necessidade
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {dashboards.map((dashboard, index) => (
                <div
                  key={index}
                  className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all"
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-2xl font-bold text-white">
                      {dashboard.nome}
                    </h3>
                    <FaChartBar className="text-3xl text-cyan-400" />
                  </div>
                  
                  <p className="text-gray-300 mb-6">
                    {dashboard.descricao}
                  </p>

                  <div className="space-y-2">
                    <p className="text-sm text-cyan-400 font-medium mb-3">Widgets inclusos:</p>
                    {dashboard.widgets.map((widget, idx) => (
                      <div key={idx} className="bg-slate-900/50 rounded-lg p-3 border border-slate-600">
                        <p className="text-gray-300 text-sm">{widget}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Exemplo Visual de Dashboard */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Exemplo de Dashboard
              </h2>
              <p className="text-xl text-gray-400">
                Visualização em tempo real dos seus dados
              </p>
            </div>

            <div className="bg-slate-800/50 backdrop-blur-sm rounded-3xl p-8 border border-slate-700">
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {/* KPI Cards */}
                <div className="bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/50 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <FaTrophy className="text-3xl text-emerald-400" />
                    <span className="text-emerald-400 text-sm font-medium">↑ 12%</span>
                  </div>
                  <div className="text-4xl font-bold text-white mb-2">87%</div>
                  <p className="text-gray-400 text-sm">Taxa de Sucesso</p>
                </div>

                <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/50 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <FaChartLine className="text-3xl text-blue-400" />
                    <span className="text-blue-400 text-sm font-medium">↑ 8%</span>
                  </div>
                  <div className="text-4xl font-bold text-white mb-2">1.2K</div>
                  <p className="text-gray-400 text-sm">Processos Ativos</p>
                </div>

                <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/50 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <FaClock className="text-3xl text-purple-400" />
                    <span className="text-purple-400 text-sm font-medium">↓ 15%</span>
                  </div>
                  <div className="text-4xl font-bold text-white mb-2">8.5</div>
                  <p className="text-gray-400 text-sm">Meses Médios</p>
                </div>

                <div className="bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/50 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <FaChartPie className="text-3xl text-amber-400" />
                    <span className="text-amber-400 text-sm font-medium">↓ 5%</span>
                  </div>
                  <div className="text-4xl font-bold text-white mb-2">R$ 2.8M</div>
                  <p className="text-gray-400 text-sm">Custos Totais</p>
                </div>
              </div>

              {/* Gráfico Simulado */}
              <div className="bg-slate-900/50 rounded-2xl p-8 border border-slate-600">
                <h4 className="text-xl font-bold text-white mb-6">Tendência de Processos (12 meses)</h4>
                <div className="flex items-end justify-between gap-2 h-48">
                  {[65, 72, 68, 85, 78, 92, 88, 95, 90, 98, 94, 100].map((height, idx) => (
                    <div key={idx} className="flex-1 flex flex-col items-center gap-2">
                      <div 
                        className="w-full bg-gradient-to-t from-emerald-500 to-teal-500 rounded-t-lg transition-all hover:from-emerald-400 hover:to-teal-400"
                        style={{ height: `${height}%` }}
                      />
                      <span className="text-xs text-gray-500">{idx + 1}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Tecnologias */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Stack Tecnológico
              </h2>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {tecnologias.map((tech, index) => (
                <div
                  key={index}
                  className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-emerald-500/50 transition-all"
                >
                  <h3 className="text-2xl font-bold text-white mb-3">
                    {tech.nome}
                  </h3>
                  <p className="text-gray-300 mb-4">
                    {tech.descricao}
                  </p>
                  <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-600">
                    <p className="text-sm text-emerald-400 font-medium">Aplicação:</p>
                    <p className="text-gray-400 text-sm">{tech.aplicacao}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Benefícios */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Benefícios do Analytics Jurídico
              </h2>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700">
                <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400 mb-4">
                  60%
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">
                  Redução de Custos
                </h3>
                <p className="text-gray-300">
                  Otimização de recursos e identificação de desperdícios
                </p>
              </div>

              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700">
                <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400 mb-4">
                  85%
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">
                  Decisões Data-Driven
                </h3>
                <p className="text-gray-300">
                  Estratégias baseadas em dados concretos
                </p>
              </div>

              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700">
                <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-4">
                  3x
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">
                  Mais Produtividade
                </h3>
                <p className="text-gray-300">
                  Automação de relatórios e análises
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Transforme Dados em Decisões Estratégicas
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Implemente Analytics Jurídico e tenha visibilidade total do seu departamento
            </p>
            <button
              onClick={() => window.open(`https://wa.me/5534998264603?text=${encodeURIComponent('Olá! Gostaria de saber mais sobre Analytics Jurídico.')}`, '_blank')}
              className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-2xl hover:shadow-emerald-500/50 transition-all"
            >
              Agendar Demonstração
            </button>
          </div>
        </section>

        <Footer />
      </div>
    </>
  )
}

