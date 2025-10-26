'use client'

import { FaSearch, FaCheck, FaBrain, FaDatabase, FaChartLine, FaFileAlt, FaArrowRight } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'

export default function PesquisaJuridicaPage() {
  const features = [
    {
      icon: FaBrain,
      title: 'Busca Semântica',
      description: 'IA compreende o contexto e significado da sua pesquisa, não apenas palavras-chave',
      gradient: 'from-green-600 to-emerald-600'
    },
    {
      icon: FaDatabase,
      title: '90M+ Decisões',
      description: 'Acesso a mais de 90 milhões de decisões judiciais de todos os tribunais brasileiros',
      gradient: 'from-blue-600 to-cyan-600'
    },
    {
      icon: FaChartLine,
      title: 'Análise de Precedentes',
      description: 'Identifica padrões e tendências em decisões similares automaticamente',
      gradient: 'from-purple-600 to-pink-600'
    },
    {
      icon: FaFileAlt,
      title: 'Resumos Automáticos',
      description: 'IA gera resumos executivos das decisões mais relevantes',
      gradient: 'from-orange-600 to-red-600'
    }
  ]

  const benefits = [
    'Busca semântica avançada com IA',
    'Acesso a 90M+ decisões judiciais',
    'Filtros inteligentes por tribunal, data, tema',
    'Resumos automáticos de jurisprudência',
    'Citações e referências relevantes',
    'Exportação em diversos formatos',
    'Histórico de pesquisas',
    'Alertas de novas decisões'
  ]

  const tribunals = [
    { name: 'STF', full: 'Supremo Tribunal Federal', icon: '⚖️' },
    { name: 'STJ', full: 'Superior Tribunal de Justiça', icon: '⚖️' },
    { name: 'TST', full: 'Tribunal Superior do Trabalho', icon: '👔' },
    { name: 'TRFs', full: 'Tribunais Regionais Federais', icon: '🏛️' },
    { name: 'TJs', full: 'Tribunais de Justiça Estaduais', icon: '🏛️' },
    { name: 'TRTs', full: 'Tribunais Regionais do Trabalho', icon: '👔' }
  ]

  return (
    <>
      <SEOHead
        title="Pesquisa Jurídica IA - Genesys Tecnologia"
        description="Pesquisa jurisprudencial inteligente com IA. Busca semântica em 90M+ decisões, resumos automáticos e análise de precedentes."
        keywords="pesquisa jurídica, jurisprudência, busca semântica, IA jurídica, precedentes, decisões judiciais"
        canonical="https://genesys-tecnologia.com.br/produtos/pesquisa-juridica"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

        {/* Hero Section */}
        <section className="pt-32 pb-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-500/10 border border-green-500/30 rounded-full mb-6">
                  <FaSearch className="text-green-400" />
                  <span className="text-green-300 text-sm font-medium">Pesquisa Jurídica Inteligente</span>
                </div>

                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-green-400 via-emerald-400 to-green-400 bg-clip-text text-transparent">
                  Pesquisa Jurídica com IA
                </h1>

                <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                  Encontre jurisprudências relevantes em segundos com busca semântica avançada. 
                  Acesso a mais de 90 milhões de decisões judiciais com análise inteligente.
                </p>

                <div className="grid grid-cols-3 gap-4 mb-8">
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-green-400">90M+</div>
                    <div className="text-xs text-gray-400 mt-1">Decisões</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-emerald-400">2min</div>
                    <div className="text-xs text-gray-400 mt-1">Por Pesquisa</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-teal-400">97.8%</div>
                    <div className="text-xs text-gray-400 mt-1">Precisão</div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-4">
                  <button
                    onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de conhecer a solução de Pesquisa Jurídica IA.', '_blank')}
                    className="px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg font-semibold hover:shadow-xl hover:shadow-green-500/50 transition-all hover:scale-105 flex items-center gap-2"
                  >
                    Solicitar Demonstração
                    <FaArrowRight />
                  </button>
                  <button
                    onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre preços da Pesquisa Jurídica.', '_blank')}
                    className="px-8 py-4 bg-slate-800 text-white rounded-lg font-semibold border border-slate-700 hover:border-green-500/50 transition-all hover:scale-105"
                  >
                    Ver Preços
                  </button>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="relative"
              >
                <div className="bg-gradient-to-br from-green-600/20 to-emerald-600/20 rounded-3xl p-8 border border-green-500/30 backdrop-blur-sm">
                  <div className="space-y-4">
                    {benefits.slice(0, 6).map((benefit, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 + idx * 0.1 }}
                        className="flex items-center gap-3 text-gray-200"
                      >
                        <FaCheck className="text-green-400 flex-shrink-0" />
                        <span>{benefit}</span>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                Recursos Principais
              </h2>
              <p className="text-xl text-gray-400">
                Tecnologia de ponta para pesquisa jurídica
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 hover:border-green-500/50 transition-all hover:shadow-xl hover:shadow-green-500/20"
                >
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4`}>
                    <feature.icon className="text-2xl text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                  <p className="text-gray-400">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Tribunals Section */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                Tribunais Cobertos
              </h2>
              <p className="text-xl text-gray-400">
                Acesso completo a todos os tribunais brasileiros
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {tribunals.map((tribunal, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-emerald-500/50 transition-all"
                >
                  <div className="flex items-center gap-4">
                    <div className="text-4xl">{tribunal.icon}</div>
                    <div>
                      <h3 className="text-xl font-bold text-white">{tribunal.name}</h3>
                      <p className="text-sm text-gray-400">{tribunal.full}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-3xl p-12 text-center">
              <h2 className="text-4xl font-bold text-white mb-4">
                Pronto para acelerar suas pesquisas jurídicas?
              </h2>
              <p className="text-xl text-green-100 mb-8">
                Agende uma demonstração gratuita e veja a IA em ação
              </p>
              <button
                onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de agendar uma demonstração da Pesquisa Jurídica IA.', '_blank')}
                className="bg-white text-green-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105 inline-flex items-center gap-2"
              >
                Agendar Demonstração Gratuita
                <FaArrowRight />
              </button>
            </div>
          </div>
        </section>

        <Footer />
      </div>
    </>
  )
}

