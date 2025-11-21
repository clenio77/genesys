'use client'

import { FaRobot, FaCheck, FaFileAlt, FaBell, FaChartLine, FaArrowRight, FaCog } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'

export default function AutomacaoProcessosPage() {
  const features = [
    {
      icon: FaFileAlt,
      title: 'Geração de Documentos',
      description: 'Crie petições, contratos e documentos automaticamente com templates inteligentes',
      gradient: 'from-orange-600 to-red-600'
    },
    {
      icon: FaCog,
      title: 'Fluxos Inteligentes',
      description: 'Automatize processos repetitivos e ganhe produtividade com workflows personalizados',
      gradient: 'from-blue-600 to-cyan-600'
    },
    {
      icon: FaBell,
      title: 'Notificações Automáticas',
      description: 'Receba alertas inteligentes sobre prazos, atualizações e eventos importantes',
      gradient: 'from-purple-600 to-pink-600'
    },
    {
      icon: FaChartLine,
      title: 'Análise de Produtividade',
      description: 'Monitore métricas e otimize processos com dashboards em tempo real',
      gradient: 'from-green-600 to-emerald-600'
    }
  ]

  const benefits = [
    'Geração automática de documentos',
    'Fluxos de trabalho personalizáveis',
    'Integração com sistemas existentes',
    'Notificações e alertas inteligentes',
    'Agendamento automático de tarefas',
    'Templates personalizáveis',
    'Gestão de prazos automatizada',
    'Relatórios de produtividade'
  ]

  const automations = [
    {
      title: 'Petições Automáticas',
      description: 'Gere petições completas com base em templates e dados do processo',
      icon: '📝',
      time: '5min → 30seg'
    },
    {
      title: 'Gestão de Prazos',
      description: 'Controle automático de prazos com alertas e notificações',
      icon: '⏰',
      time: '100% automático'
    },
    {
      title: 'Acompanhamento Processual',
      description: 'Monitore processos automaticamente e receba atualizações',
      icon: '📊',
      time: '24/7'
    },
    {
      title: 'Distribuição de Tarefas',
      description: 'Atribua tarefas automaticamente com base em regras inteligentes',
      icon: '👥',
      time: 'Instantâneo'
    }
  ]

  const stats = [
    { value: '+300%', label: 'Produtividade', icon: '📈' },
    { value: '100%', label: 'Automação', icon: '🤖' },
    { value: '-95%', label: 'Erros', icon: '✅' },
    { value: '15h/sem', label: 'Economia', icon: '⏱️' }
  ]

  return (
    <>
      <SEOHead
        title="Automação de Processos - Genesys Tecnologia"
        description="Automatize tarefas jurídicas repetitivas com IA. Geração de documentos, gestão de prazos e workflows inteligentes."
        keywords="automação jurídica, workflow jurídico, automação de processos, IA jurídica, gestão de prazos"
        canonical="https://genesys-tecnologia.com.br/produtos/automacao-processos"
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
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500/10 border border-orange-500/30 rounded-full mb-6">
                  <FaRobot className="text-orange-400" />
                  <span className="text-orange-300 text-sm font-medium">Automação Inteligente</span>
                </div>

                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-orange-400 via-red-400 to-orange-400 bg-clip-text text-transparent">
                  Automação de Processos
                </h1>

                <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                  Automatize tarefas repetitivas e ganhe até 300% de produtividade. 
                  Gestão de prazos, petições automáticas e workflows inteligentes.
                </p>

                <div className="grid grid-cols-2 gap-4 mb-8">
                  {stats.map((stat, idx) => (
                    <div key={idx} className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                      <div className="text-2xl mb-1">{stat.icon}</div>
                      <div className="text-2xl font-bold text-orange-400">{stat.value}</div>
                      <div className="text-xs text-gray-400 mt-1">{stat.label}</div>
                    </div>
                  ))}
                </div>

                <div className="flex flex-wrap gap-4">
                  <button
                    onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de conhecer a solução de Automação de Processos.', '_blank')}
                    className="px-8 py-4 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-lg font-semibold hover:shadow-xl hover:shadow-orange-500/50 transition-all hover:scale-105 flex items-center gap-2"
                  >
                    Solicitar Demonstração
                    <FaArrowRight />
                  </button>
                  <button
                    onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre preços da Automação de Processos.', '_blank')}
                    className="px-8 py-4 bg-slate-800 text-white rounded-lg font-semibold border border-slate-700 hover:border-orange-500/50 transition-all hover:scale-105"
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
                <div className="bg-gradient-to-br from-orange-600/20 to-red-600/20 rounded-3xl p-8 border border-orange-500/30 backdrop-blur-sm">
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
                Automatize e otimize seus processos jurídicos
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
                  className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 hover:border-orange-500/50 transition-all hover:shadow-xl hover:shadow-orange-500/20"
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

        {/* Automations Section */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                Automações Disponíveis
              </h2>
              <p className="text-xl text-gray-400">
                Processos que você pode automatizar hoje
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {automations.map((automation, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-red-500/50 transition-all"
                >
                  <div className="text-5xl mb-4 text-center">{automation.icon}</div>
                  <h3 className="text-lg font-bold text-white mb-2 text-center">{automation.title}</h3>
                  <p className="text-sm text-gray-400 mb-4 text-center">{automation.description}</p>
                  <div className="bg-orange-500/10 border border-orange-500/30 rounded-lg p-2 text-center">
                    <span className="text-orange-400 font-semibold text-sm">{automation.time}</span>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-gradient-to-r from-orange-600 to-red-600 rounded-3xl p-12 text-center">
              <h2 className="text-4xl font-bold text-white mb-4">
                Pronto para ganhar 300% de produtividade?
              </h2>
              <p className="text-xl text-orange-100 mb-8">
                Agende uma demonstração gratuita e veja a automação em ação
              </p>
              <button
                onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de agendar uma demonstração da Automação de Processos.', '_blank')}
                className="bg-white text-orange-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105 inline-flex items-center gap-2"
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

