'use client'

import { FaSearch, FaDatabase, FaBrain, FaFilter, FaChartBar, FaArrowLeft, FaRobot, FaCheckCircle, FaClock } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import Link from 'next/link'
import SEOHead from '@/components/SEOHead'

export default function PesquisaJurisprudencialPage() {
  const etapas = [
    {
      numero: 1,
      titulo: 'Consulta em Linguagem Natural',
      descricao: 'Digite sua dúvida jurídica como se estivesse conversando',
      icon: FaSearch,
      cor: 'from-blue-500 to-cyan-500',
      exemplo: '"Casos de rescisão indireta por assédio moral"'
    },
    {
      numero: 2,
      titulo: 'Processamento Semântico',
      descricao: 'IA entende o contexto e a intenção da busca',
      icon: FaBrain,
      cor: 'from-purple-500 to-pink-500',
      exemplo: 'Análise de sinônimos, contexto e área do direito'
    },
    {
      numero: 3,
      titulo: 'Busca Inteligente',
      descricao: 'Sistema vasculha milhões de decisões judiciais',
      icon: FaDatabase,
      cor: 'from-emerald-500 to-teal-500',
      exemplo: 'STF, STJ, TRTs, TJs e tribunais regionais'
    },
    {
      numero: 4,
      titulo: 'Filtragem Avançada',
      descricao: 'IA filtra e ranqueia por relevância',
      icon: FaFilter,
      cor: 'from-amber-500 to-orange-500',
      exemplo: 'Ordenação por similaridade e importância'
    },
    {
      numero: 5,
      titulo: 'Análise de Padrões',
      descricao: 'Identifica tendências e padrões decisórios',
      icon: FaChartBar,
      cor: 'from-indigo-500 to-purple-500',
      exemplo: 'Taxa de sucesso, argumentos vencedores'
    },
    {
      numero: 6,
      titulo: 'Resultados Estruturados',
      descricao: 'Apresentação organizada com insights',
      icon: FaCheckCircle,
      cor: 'from-green-500 to-emerald-500',
      exemplo: 'Resumos, citações e recomendações'
    }
  ]

  const fontes = [
    { nome: 'STF', total: '1.2M+', descricao: 'Supremo Tribunal Federal' },
    { nome: 'STJ', total: '8.5M+', descricao: 'Superior Tribunal de Justiça' },
    { nome: 'TRTs', total: '15M+', descricao: 'Tribunais Regionais do Trabalho' },
    { nome: 'TJs', total: '50M+', descricao: 'Tribunais de Justiça Estaduais' },
    { nome: 'TRFs', total: '12M+', descricao: 'Tribunais Regionais Federais' },
    { nome: 'TST', total: '3M+', descricao: 'Tribunal Superior do Trabalho' }
  ]

  const diferenciais = [
    {
      titulo: 'Busca Semântica',
      descricao: 'Entende o significado, não apenas palavras-chave',
      icon: FaBrain,
      detalhes: [
        'Compreensão contextual',
        'Sinônimos jurídicos',
        'Interpretação de intenção',
        'Análise de conceitos'
      ]
    },
    {
      titulo: 'Análise Preditiva',
      descricao: 'Prevê tendências e probabilidades de sucesso',
      icon: FaChartBar,
      detalhes: [
        'Taxa de sucesso histórica',
        'Tendências de julgamento',
        'Argumentos vencedores',
        'Perfil de magistrados'
      ]
    },
    {
      titulo: 'Velocidade Extrema',
      descricao: 'Resultados em segundos, não em horas',
      icon: FaClock,
      detalhes: [
        'Busca em tempo real',
        'Cache inteligente',
        'Indexação otimizada',
        'Processamento paralelo'
      ]
    }
  ]

  return (
    <>
      <SEOHead 
        title="Pesquisa Jurisprudencial com IA | Genesys Tecnologia"
        description="Entenda como funciona a pesquisa jurisprudencial inteligente. Busca semântica em milhões de decisões judiciais com IA e análise preditiva."
        keywords="pesquisa jurisprudencial ia, busca semântica jurídica, análise preditiva direito, jurisprudência inteligente"
        canonical="https://genesys-tecnologia.com.br/tecnologias/pesquisa-jurisprudencial"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

        {/* Hero Section */}
        <section className="pt-32 pb-20 px-4 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600/10 to-pink-600/10" />
          
          <div className="max-w-7xl mx-auto relative z-10">
            <Link 
              href="/#services"
              className="inline-flex items-center gap-2 text-cyan-400 hover:text-cyan-300 mb-8 transition-colors"
            >
              <FaArrowLeft />
              Voltar para Serviços
            </Link>

            <div className="text-center mb-16">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl mb-6">
                <FaSearch className="text-4xl text-white" />
              </div>
              <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
                Pesquisa Jurisprudencial <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">Inteligente</span>
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Busque em milhões de decisões judiciais usando linguagem natural. 
                IA que entende o contexto e encontra exatamente o que você precisa.
              </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">
                  90M+
                </div>
                <p className="text-gray-400 text-sm">Decisões Indexadas</p>
              </div>
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400 mb-2">
                  &lt;3s
                </div>
                <p className="text-gray-400 text-sm">Tempo de Resposta</p>
              </div>
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400 mb-2">
                  95%
                </div>
                <p className="text-gray-400 text-sm">Precisão</p>
              </div>
              <div className="text-center bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-orange-400 mb-2">
                  24/7
                </div>
                <p className="text-gray-400 text-sm">Disponibilidade</p>
              </div>
            </div>
          </div>
        </section>

        {/* Como Funciona */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Como Funciona a Busca Inteligente
              </h2>
              <p className="text-xl text-gray-400">
                Do seu questionamento aos resultados precisos
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {etapas.map((etapa) => {
                const Icon = etapa.icon
                return (
                  <div
                    key={etapa.numero}
                    className="relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-purple-500/50 transition-all group"
                  >
                    <div className="absolute -top-4 -left-4 w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-lg">
                      {etapa.numero}
                    </div>
                    
                    <div className={`inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br ${etapa.cor} rounded-xl mb-6 group-hover:scale-110 transition-transform`}>
                      <Icon className="text-3xl text-white" />
                    </div>

                    <h3 className="text-2xl font-bold text-white mb-3">
                      {etapa.titulo}
                    </h3>
                    <p className="text-gray-300 mb-4">
                      {etapa.descricao}
                    </p>
                    <div className="bg-slate-900/50 rounded-lg p-3 border border-slate-600">
                      <p className="text-xs text-cyan-400 font-medium mb-1">Exemplo:</p>
                      <p className="text-gray-400 text-sm italic">{etapa.exemplo}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* Fontes de Dados */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Fontes de Dados
              </h2>
              <p className="text-xl text-gray-400">
                Acesso aos principais tribunais do Brasil
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {fontes.map((fonte, index) => (
                <div
                  key={index}
                  className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all text-center group"
                >
                  <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400 mb-3">
                    {fonte.total}
                  </div>
                  <h3 className="text-3xl font-bold text-white mb-2">
                    {fonte.nome}
                  </h3>
                  <p className="text-gray-400">
                    {fonte.descricao}
                  </p>
                  <div className="mt-4 h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full group-hover:w-full w-0 transition-all duration-1000" />
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-12 text-center">
              <p className="text-gray-400 text-lg">
                <span className="text-cyan-400 font-bold text-3xl">90+ milhões</span> de decisões judiciais indexadas e atualizadas diariamente
              </p>
            </div>
          </div>
        </section>

        {/* Diferenciais */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Diferenciais da Nossa Tecnologia
              </h2>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {diferenciais.map((diff, index) => {
                const Icon = diff.icon
                return (
                  <div
                    key={index}
                    className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-purple-500/50 transition-all"
                  >
                    <Icon className="text-5xl text-purple-400 mb-6" />
                    <h3 className="text-2xl font-bold text-white mb-3">
                      {diff.titulo}
                    </h3>
                    <p className="text-gray-300 mb-6">
                      {diff.descricao}
                    </p>
                    <ul className="space-y-2">
                      {diff.detalhes.map((detalhe, idx) => (
                        <li key={idx} className="flex items-center gap-2 text-gray-400">
                          <FaCheckCircle className="text-cyan-400 flex-shrink-0" />
                          <span>{detalhe}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* Fluxograma */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Arquitetura do Sistema
              </h2>
            </div>

            <div className="bg-slate-800/50 backdrop-blur-sm rounded-3xl p-12 border border-slate-700">
              <div className="space-y-8">
                {/* Camada 1 */}
                <div className="text-center">
                  <div className="inline-block bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-8 py-4 rounded-xl font-bold text-lg">
                    Interface do Usuário
                  </div>
                </div>

                <div className="text-center text-cyan-400 text-3xl">↓</div>

                {/* Camada 2 */}
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/50 rounded-xl p-6 text-center">
                    <FaBrain className="text-4xl text-purple-400 mx-auto mb-3" />
                    <h4 className="text-white font-bold mb-2">NLP Engine</h4>
                    <p className="text-gray-400 text-sm">Processamento de linguagem</p>
                  </div>
                  <div className="bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/50 rounded-xl p-6 text-center">
                    <FaRobot className="text-4xl text-emerald-400 mx-auto mb-3" />
                    <h4 className="text-white font-bold mb-2">ML Models</h4>
                    <p className="text-gray-400 text-sm">Modelos de aprendizado</p>
                  </div>
                  <div className="bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/50 rounded-xl p-6 text-center">
                    <FaFilter className="text-4xl text-amber-400 mx-auto mb-3" />
                    <h4 className="text-white font-bold mb-2">Ranking System</h4>
                    <p className="text-gray-400 text-sm">Sistema de relevância</p>
                  </div>
                </div>

                <div className="text-center text-cyan-400 text-3xl">↓</div>

                {/* Camada 3 */}
                <div className="text-center">
                  <div className="inline-block bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-8 py-4 rounded-xl font-bold text-lg">
                    <FaDatabase className="inline mr-2" />
                    Base de Dados (90M+ decisões)
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Experimente a Pesquisa Jurisprudencial Inteligente
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Encontre precedentes relevantes em segundos
            </p>
            <button
              onClick={() => window.open(`https://wa.me/5534998264603?text=${encodeURIComponent('Olá! Gostaria de saber mais sobre a Pesquisa Jurisprudencial Inteligente.')}`, '_blank')}
              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-2xl hover:shadow-purple-500/50 transition-all"
            >
              Solicitar Demonstração
            </button>
          </div>
        </section>

        <Footer />
      </div>
    </>
  )
}

