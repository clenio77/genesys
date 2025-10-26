'use client'

import { FaShieldAlt, FaCheck, FaLock, FaBell, FaChartBar, FaArrowRight, FaEye } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'

export default function ComplianceIAPage() {
  const features = [
    {
      icon: FaEye,
      title: 'Monitoramento 24/7',
      description: 'Vigilância contínua de conformidade com LGPD e outras regulamentações',
      gradient: 'from-cyan-600 to-blue-600'
    },
    {
      icon: FaBell,
      title: 'Alertas Inteligentes',
      description: 'Notificações automáticas sobre riscos e não conformidades detectadas',
      gradient: 'from-blue-600 to-purple-600'
    },
    {
      icon: FaChartBar,
      title: 'Auditoria Automática',
      description: 'Relatórios completos de conformidade gerados automaticamente',
      gradient: 'from-purple-600 to-pink-600'
    },
    {
      icon: FaLock,
      title: 'Segurança Avançada',
      description: 'Criptografia de ponta e proteção de dados sensíveis',
      gradient: 'from-green-600 to-emerald-600'
    }
  ]

  const benefits = [
    'Monitoramento contínuo 24/7',
    'Alertas inteligentes de riscos',
    'Auditoria automática de conformidade',
    'Relatórios detalhados LGPD',
    'Gestão de riscos em tempo real',
    'Criptografia avançada de dados',
    'Backup automático e seguro',
    'Dashboard de conformidade'
  ]

  const regulations = [
    {
      name: 'LGPD',
      full: 'Lei Geral de Proteção de Dados',
      icon: '🇧🇷',
      coverage: '100%'
    },
    {
      name: 'GDPR',
      full: 'General Data Protection Regulation',
      icon: '🇪🇺',
      coverage: '100%'
    },
    {
      name: 'ISO 27001',
      full: 'Segurança da Informação',
      icon: '🔒',
      coverage: '100%'
    },
    {
      name: 'SOC 2',
      full: 'Service Organization Control',
      icon: '✅',
      coverage: '100%'
    }
  ]

  const complianceAreas = [
    {
      title: 'Proteção de Dados',
      description: 'Monitoramento de tratamento de dados pessoais e sensíveis',
      icon: '🛡️',
      items: ['Mapeamento de dados', 'Controle de acesso', 'Anonimização']
    },
    {
      title: 'Gestão de Riscos',
      description: 'Identificação e mitigação de riscos de conformidade',
      icon: '⚠️',
      items: ['Análise de riscos', 'Planos de ação', 'Monitoramento']
    },
    {
      title: 'Auditoria e Relatórios',
      description: 'Documentação completa para auditorias e fiscalizações',
      icon: '📋',
      items: ['Relatórios LGPD', 'Logs de acesso', 'Evidências']
    },
    {
      title: 'Treinamento',
      description: 'Capacitação da equipe em conformidade e segurança',
      icon: '🎓',
      items: ['Cursos online', 'Certificações', 'Atualizações']
    }
  ]

  return (
    <>
      <SEOHead
        title="Compliance IA - Genesys Tecnologia"
        description="Sistema de compliance automatizado com IA para LGPD, GDPR e outras regulamentações. Monitoramento 24/7 e auditoria automática."
        keywords="compliance ia, lgpd, gdpr, auditoria automática, gestão de riscos, proteção de dados"
        canonical="https://genesys-tecnologia.com.br/produtos/compliance-ia"
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
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-cyan-500/10 border border-cyan-500/30 rounded-full mb-6">
                  <FaShieldAlt className="text-cyan-400" />
                  <span className="text-cyan-300 text-sm font-medium">Compliance Inteligente</span>
                </div>

                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-cyan-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  Compliance IA
                </h1>

                <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                  Sistema completo de compliance automatizado com IA. 
                  Monitoramento 24/7, alertas inteligentes e conformidade garantida com LGPD e outras regulamentações.
                </p>

                <div className="grid grid-cols-3 gap-4 mb-8">
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-cyan-400">100%</div>
                    <div className="text-xs text-gray-400 mt-1">Precisão</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-blue-400">24/7</div>
                    <div className="text-xs text-gray-400 mt-1">Monitoramento</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                    <div className="text-3xl font-bold text-purple-400">R$30K</div>
                    <div className="text-xs text-gray-400 mt-1">Economia/mês</div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-4">
                  <button
                    onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de conhecer a solução de Compliance IA.', '_blank')}
                    className="px-8 py-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-lg font-semibold hover:shadow-xl hover:shadow-cyan-500/50 transition-all hover:scale-105 flex items-center gap-2"
                  >
                    Solicitar Demonstração
                    <FaArrowRight />
                  </button>
                  <button
                    onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre preços do Compliance IA.', '_blank')}
                    className="px-8 py-4 bg-slate-800 text-white rounded-lg font-semibold border border-slate-700 hover:border-cyan-500/50 transition-all hover:scale-105"
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
                <div className="bg-gradient-to-br from-cyan-600/20 to-blue-600/20 rounded-3xl p-8 border border-cyan-500/30 backdrop-blur-sm">
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
                Compliance automatizado e inteligente
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
                  className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 hover:border-cyan-500/50 transition-all hover:shadow-xl hover:shadow-cyan-500/20"
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

        {/* Regulations Section */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                Regulamentações Cobertas
              </h2>
              <p className="text-xl text-gray-400">
                Conformidade com as principais normas e regulamentações
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {regulations.map((regulation, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-blue-500/50 transition-all text-center"
                >
                  <div className="text-5xl mb-4">{regulation.icon}</div>
                  <h3 className="text-xl font-bold text-white mb-2">{regulation.name}</h3>
                  <p className="text-sm text-gray-400 mb-4">{regulation.full}</p>
                  <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-2">
                    <span className="text-green-400 font-semibold">{regulation.coverage} Cobertura</span>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Compliance Areas Section */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                Áreas de Compliance
              </h2>
              <p className="text-xl text-gray-400">
                Cobertura completa de todas as áreas críticas
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {complianceAreas.map((area, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-slate-800/50 rounded-xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all"
                >
                  <div className="flex items-start gap-4 mb-4">
                    <div className="text-4xl">{area.icon}</div>
                    <div>
                      <h3 className="text-2xl font-bold text-white mb-2">{area.title}</h3>
                      <p className="text-gray-400">{area.description}</p>
                    </div>
                  </div>
                  <ul className="space-y-2">
                    {area.items.map((item, i) => (
                      <li key={i} className="flex items-center gap-2 text-gray-300">
                        <FaCheck className="text-cyan-400 text-sm flex-shrink-0" />
                        <span className="text-sm">{item}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-gradient-to-r from-cyan-600 to-blue-600 rounded-3xl p-12 text-center">
              <h2 className="text-4xl font-bold text-white mb-4">
                Pronto para garantir 100% de conformidade?
              </h2>
              <p className="text-xl text-cyan-100 mb-8">
                Agende uma demonstração gratuita e veja o sistema em ação
              </p>
              <button
                onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de agendar uma demonstração do Compliance IA.', '_blank')}
                className="bg-white text-cyan-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105 inline-flex items-center gap-2"
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

