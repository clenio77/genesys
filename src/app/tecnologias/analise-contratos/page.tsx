'use client'

import { FaFileContract, FaRobot, FaCheckCircle, FaExclamationTriangle, FaLightbulb, FaClock, FaChartLine, FaArrowLeft } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import Link from 'next/link'
import SEOHead from '@/components/SEOHead'

export default function AnaliseContratosPage() {
  const etapasProcesso = [
    {
      numero: 1,
      titulo: 'Upload do Contrato',
      descricao: 'O usuário faz upload do documento em PDF, DOCX ou TXT',
      icon: FaFileContract,
      cor: 'from-blue-500 to-cyan-500'
    },
    {
      numero: 2,
      titulo: 'Processamento NLP',
      descricao: 'IA processa o texto usando Natural Language Processing',
      icon: FaRobot,
      cor: 'from-purple-500 to-pink-500'
    },
    {
      numero: 3,
      titulo: 'Identificação de Cláusulas',
      descricao: 'Sistema identifica e classifica todas as cláusulas contratuais',
      icon: FaCheckCircle,
      cor: 'from-emerald-500 to-teal-500'
    },
    {
      numero: 4,
      titulo: 'Análise de Riscos',
      descricao: 'IA detecta cláusulas problemáticas e riscos jurídicos',
      icon: FaExclamationTriangle,
      cor: 'from-amber-500 to-orange-500'
    },
    {
      numero: 5,
      titulo: 'Sugestões Inteligentes',
      descricao: 'Sistema gera recomendações de melhorias e ajustes',
      icon: FaLightbulb,
      cor: 'from-yellow-500 to-amber-500'
    },
    {
      numero: 6,
      titulo: 'Relatório Final',
      descricao: 'Geração de relatório completo com análise detalhada',
      icon: FaChartLine,
      cor: 'from-indigo-500 to-purple-500'
    }
  ]

  const tecnologias = [
    {
      nome: 'Natural Language Processing (NLP)',
      descricao: 'Processamento de linguagem natural para entender o contexto jurídico',
      aplicacao: 'Extração de entidades, análise sintática e semântica'
    },
    {
      nome: 'Machine Learning',
      descricao: 'Algoritmos que aprendem com milhares de contratos analisados',
      aplicacao: 'Classificação de cláusulas e detecção de padrões'
    },
    {
      nome: 'Deep Learning',
      descricao: 'Redes neurais profundas para análise contextual avançada',
      aplicacao: 'Compreensão de nuances e interpretação jurídica'
    },
    {
      nome: 'OCR Inteligente',
      descricao: 'Reconhecimento óptico de caracteres com IA',
      aplicacao: 'Digitalização e extração de texto de documentos escaneados'
    }
  ]

  const beneficios = [
    {
      titulo: 'Redução de 90% no Tempo',
      descricao: 'Análise que levaria horas é feita em minutos',
      icon: FaClock,
      stat: '90%'
    },
    {
      titulo: 'Precisão de 98%',
      descricao: 'Taxa de acurácia na identificação de cláusulas críticas',
      icon: FaCheckCircle,
      stat: '98%'
    },
    {
      titulo: 'Detecção de Riscos',
      descricao: 'Identifica automaticamente cláusulas problemáticas',
      icon: FaExclamationTriangle,
      stat: '100%'
    }
  ]

  return (
    <>
      <SEOHead 
        title="Análise Inteligente de Contratos com IA | Genesys Tecnologia"
        description="Entenda como funciona a análise inteligente de contratos com Inteligência Artificial. Tecnologia NLP, Machine Learning e Deep Learning aplicada ao Direito."
        keywords="análise de contratos ia, nlp jurídico, machine learning contratos, automação jurídica"
        canonical="https://genesys-tecnologia.com.br/tecnologias/analise-contratos"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

        {/* Hero Section */}
        <section className="pt-32 pb-20 px-4 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10" />
          
          <div className="max-w-7xl mx-auto relative z-10">
            <Link 
              href="/#services"
              className="inline-flex items-center gap-2 text-cyan-400 hover:text-cyan-300 mb-8 transition-colors"
            >
              <FaArrowLeft />
              Voltar para Serviços
            </Link>

            <div className="text-center mb-16">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl mb-6">
                <FaFileContract className="text-4xl text-white" />
              </div>
              <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
                Análise Inteligente de <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">Contratos</span>
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Descubra como a Inteligência Artificial revoluciona a análise de contratos, 
                identificando riscos, cláusulas críticas e sugerindo melhorias em minutos.
              </p>
            </div>
          </div>
        </section>

        {/* Como Funciona */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Como Funciona o Processo
              </h2>
              <p className="text-xl text-gray-400">
                Entenda cada etapa da análise inteligente de contratos
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {etapasProcesso.map((etapa) => {
                const Icon = etapa.icon
                return (
                  <div
                    key={etapa.numero}
                    className="relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all group"
                  >
                    <div className="absolute -top-4 -left-4 w-12 h-12 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-lg">
                      {etapa.numero}
                    </div>
                    
                    <div className={`inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br ${etapa.cor} rounded-xl mb-6 group-hover:scale-110 transition-transform`}>
                      <Icon className="text-3xl text-white" />
                    </div>

                    <h3 className="text-2xl font-bold text-white mb-3">
                      {etapa.titulo}
                    </h3>
                    <p className="text-gray-300">
                      {etapa.descricao}
                    </p>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* Fluxograma Visual */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Fluxo de Análise
              </h2>
              <p className="text-xl text-gray-400">
                Visualize o caminho que seu contrato percorre
              </p>
            </div>

            <div className="bg-slate-800/50 backdrop-blur-sm rounded-3xl p-8 border border-slate-700">
              <div className="flex flex-col md:flex-row items-center justify-between gap-8">
                <div className="flex-1 text-center">
                  <div className="w-24 h-24 mx-auto bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mb-4">
                    <FaFileContract className="text-4xl text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">Documento</h3>
                  <p className="text-gray-400 text-sm">Upload do contrato</p>
                </div>

                <div className="text-cyan-400 text-4xl hidden md:block">→</div>

                <div className="flex-1 text-center">
                  <div className="w-24 h-24 mx-auto bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-4">
                    <FaRobot className="text-4xl text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">IA Processa</h3>
                  <p className="text-gray-400 text-sm">NLP + ML</p>
                </div>

                <div className="text-cyan-400 text-4xl hidden md:block">→</div>

                <div className="flex-1 text-center">
                  <div className="w-24 h-24 mx-auto bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center mb-4">
                    <FaCheckCircle className="text-4xl text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">Análise</h3>
                  <p className="text-gray-400 text-sm">Identificação</p>
                </div>

                <div className="text-cyan-400 text-4xl hidden md:block">→</div>

                <div className="flex-1 text-center">
                  <div className="w-24 h-24 mx-auto bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl flex items-center justify-center mb-4">
                    <FaChartLine className="text-4xl text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">Relatório</h3>
                  <p className="text-gray-400 text-sm">Insights + Riscos</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Tecnologias Utilizadas */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Tecnologias Utilizadas
              </h2>
              <p className="text-xl text-gray-400">
                Stack de IA de última geração
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {tecnologias.map((tech, index) => (
                <div
                  key={index}
                  className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-purple-500/50 transition-all"
                >
                  <h3 className="text-2xl font-bold text-white mb-3">
                    {tech.nome}
                  </h3>
                  <p className="text-gray-300 mb-4">
                    {tech.descricao}
                  </p>
                  <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-600">
                    <p className="text-sm text-cyan-400 font-medium">Aplicação:</p>
                    <p className="text-gray-400 text-sm">{tech.aplicacao}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Benefícios */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Benefícios Comprovados
              </h2>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {beneficios.map((beneficio, index) => {
                const Icon = beneficio.icon
                return (
                  <div
                    key={index}
                    className="text-center bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700"
                  >
                    <Icon className="text-6xl text-cyan-400 mx-auto mb-4" />
                    <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400 mb-4">
                      {beneficio.stat}
                    </div>
                    <h3 className="text-2xl font-bold text-white mb-3">
                      {beneficio.titulo}
                    </h3>
                    <p className="text-gray-300">
                      {beneficio.descricao}
                    </p>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Pronto para Revolucionar sua Análise de Contratos?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Experimente nossa tecnologia e veja a diferença
            </p>
            <button
              onClick={() => window.open(`https://wa.me/5534998264603?text=${encodeURIComponent('Olá! Gostaria de saber mais sobre a Análise Inteligente de Contratos.')}`, '_blank')}
              className="bg-gradient-to-r from-cyan-500 to-blue-500 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-2xl hover:shadow-cyan-500/50 transition-all"
            >
              Falar com Especialista
            </button>
          </div>
        </section>

        <Footer />
      </div>
    </>
  )
}

