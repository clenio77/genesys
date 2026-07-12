'use client'

import { FaFileContract, FaCheck, FaShieldAlt, FaClock, FaChartLine, FaRobot, FaArrowRight } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import LegacyProdutoBanner from '@/components/LegacyProdutoBanner'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'

export default function AnaliseContratosPage() {
  const features = [
    {
      icon: FaRobot,
      title: 'Revisão Automática',
      description: 'IA analisa contratos em minutos, identificando cláusulas críticas e pontos de atenção',
      gradient: 'from-blue-600 to-cyan-600'
    },
    {
      icon: FaShieldAlt,
      title: 'Identificação de Riscos',
      description: 'Detecta automaticamente cláusulas abusivas, riscos jurídicos e pontos de vulnerabilidade',
      gradient: 'from-purple-600 to-pink-600'
    },
    {
      icon: FaChartLine,
      title: 'Análise Comparativa',
      description: 'Compare contratos com modelos padrão e identifique desvios e oportunidades',
      gradient: 'from-green-600 to-emerald-600'
    },
    {
      icon: FaClock,
      title: 'Economia de Tempo',
      description: 'Reduza 80% do tempo gasto em revisão manual de contratos',
      gradient: 'from-orange-600 to-red-600'
    }
  ]

  const benefits = [
    'Revisão completa em menos de 5 minutos',
    'Identificação de cláusulas críticas',
    'Sugestões de melhorias automáticas',
    'Comparação com modelos de mercado',
    'Relatórios detalhados em PDF',
    'Histórico de versões',
    'Alertas de conformidade LGPD',
    'Integração com sistemas existentes'
  ]

  const useCases = [
    {
      title: 'Contratos Comerciais',
      description: 'Análise de contratos de compra e venda, prestação de serviços e parcerias',
      icon: '📄'
    },
    {
      title: 'Contratos Trabalhistas',
      description: 'Revisão de contratos de trabalho, acordos e termos de rescisão',
      icon: '👔'
    },
    {
      title: 'Contratos Imobiliários',
      description: 'Análise de contratos de locação, compra e venda de imóveis',
      icon: '🏢'
    },
    {
      title: 'Termos de Uso',
      description: 'Revisão de termos de uso, políticas de privacidade e LGPD',
      icon: '📱'
    }
  ]

  return (
    <>
      <SEOHead
        title="Análise de Contratos IA - Genesys Tecnologia"
        description="Análise inteligente de contratos com IA. Revisão automática, identificação de riscos e sugestões de melhorias em minutos."
        keywords="análise de contratos, IA jurídica, revisão de contratos, análise automática, contratos inteligentes"
        canonical="https://genesys-tecnologia.com.br/produtos/analise-contratos"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

        <LegacyProdutoBanner
          titulo="Capacidade do Kermartin IA"
          descricao="Análise de contratos faz parte do Kermartin — a Genesys configura módulos e fluxos na implantação."
          linkServico="/produtos/kermartin-ia"
          labelServico="Conhecer o Kermartin"
        />

        {/* Hero Section */}
        <section className="pt-32 pb-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-full mb-6">
                  <FaFileContract className="text-blue-400" />
                  <span className="text-blue-300 text-sm font-medium">Análise Inteligente de Contratos</span>
                </div>

                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-400 bg-clip-text text-transparent">
                  Análise de Contratos com IA
                </h1>

                <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                  Revolucione a revisão de contratos com Inteligência Artificial. 
                  Análise completa em minutos, identificação automática de riscos e sugestões precisas.
                </p>

                <div className="grid grid-cols-3 gap-4 mb-8">
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-blue-400">98.5%</div>
                    <div className="text-xs text-gray-400 mt-1">Precisão</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-cyan-400">5min</div>
                    <div className="text-xs text-gray-400 mt-1">Por Contrato</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-purple-400">80%</div>
                    <div className="text-xs text-gray-400 mt-1">Economia</div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-4">
                  <button
                    onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de conhecer a solução de Análise de Contratos IA.', '_blank')}
                    className="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-semibold hover:shadow-xl hover:shadow-blue-500/50 transition-all hover:scale-105 flex items-center gap-2"
                  >
                    Solicitar Demonstração
                    <FaArrowRight />
                  </button>
                  <button
                    onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre preços da Análise de Contratos.', '_blank')}
                    className="px-8 py-4 bg-slate-800 text-white rounded-lg font-semibold border border-slate-700 hover:border-blue-500/50 transition-all hover:scale-105"
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
                <div className="bg-gradient-to-br from-blue-600/20 to-cyan-600/20 rounded-3xl p-8 border border-blue-500/30 backdrop-blur-sm">
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
                Tecnologia de ponta para análise jurídica
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
                  className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 hover:border-blue-500/50 transition-all hover:shadow-xl hover:shadow-blue-500/20"
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

        {/* Use Cases Section */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                Casos de Uso
              </h2>
              <p className="text-xl text-gray-400">
                Aplicável a diversos tipos de contratos
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {useCases.map((useCase, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-cyan-500/50 transition-all text-center"
                >
                  <div className="text-5xl mb-4">{useCase.icon}</div>
                  <h3 className="text-lg font-bold text-white mb-2">{useCase.title}</h3>
                  <p className="text-sm text-gray-400">{useCase.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl p-12 text-center">
              <h2 className="text-4xl font-bold text-white mb-4">
                Pronto para revolucionar sua análise de contratos?
              </h2>
              <p className="text-xl text-blue-100 mb-8">
                Agende uma demonstração gratuita e veja a IA em ação
              </p>
              <button
                onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de agendar uma demonstração da Análise de Contratos IA.', '_blank')}
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105 inline-flex items-center gap-2"
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

