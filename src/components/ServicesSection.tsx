'use client'

import { motion } from 'framer-motion'
import ServiceCard from './ServiceCard'
import { FaBrain, FaFileAlt, FaChartLine, FaRobot, FaShieldAlt, FaDatabase } from 'react-icons/fa'

export default function ServicesSection() {
  const services = [
    {
      title: 'Análise Inteligente de Contratos',
      description: 'IA avançada para revisão automática de contratos, identificação de cláusulas críticas e sugestões de melhorias.',
      icon: FaFileAlt,
      gradient: 'from-blue-600 to-cyan-600',
      badge: 'Popular',
      features: [
        'Revisão automática em minutos',
        'Identificação de riscos',
        'Sugestões de melhorias',
        'Comparação com modelos',
        'Relatórios detalhados',
      ],
    },
    {
      title: 'Pesquisa Jurisprudencial IA',
      description: 'Busca inteligente em milhões de decisões judiciais com análise de padrões e predição de resultados.',
      icon: FaBrain,
      gradient: 'from-purple-600 to-pink-600',
      features: [
        'Busca semântica avançada',
        'Análise de tendências',
        'Predição de resultados',
        'Jurisprudência relevante',
        'Resumos automáticos',
      ],
    },
    {
      title: 'Analytics Jurídico',
      description: 'Dashboards interativos com métricas em tempo real para tomada de decisões estratégicas.',
      icon: FaChartLine,
      gradient: 'from-emerald-600 to-teal-600',
      badge: 'Novo',
      features: [
        'Métricas em tempo real',
        'Visualizações interativas',
        'Relatórios customizados',
        'Previsões baseadas em IA',
        'Exportação de dados',
      ],
    },
    {
      title: 'Automação de Processos',
      description: 'Automatize tarefas repetitivas e ganhe tempo para focar no que realmente importa.',
      icon: FaRobot,
      gradient: 'from-amber-600 to-orange-600',
      features: [
        'Geração automática de documentos',
        'Fluxos de trabalho inteligentes',
        'Integração com sistemas',
        'Notificações automáticas',
        'Agendamento inteligente',
      ],
    },
    {
      title: 'Compliance e Segurança',
      description: 'Garanta conformidade com LGPD e outras regulamentações com monitoramento contínuo.',
      icon: FaShieldAlt,
      gradient: 'from-rose-600 to-red-600',
      features: [
        'Monitoramento LGPD',
        'Auditoria automática',
        'Alertas de conformidade',
        'Criptografia avançada',
        'Backup automático',
      ],
    },
    {
      title: 'Gestão de Conhecimento',
      description: 'Centralize e organize todo conhecimento jurídico da sua empresa com busca inteligente.',
      icon: FaDatabase,
      gradient: 'from-indigo-600 to-blue-600',
      features: [
        'Base de conhecimento centralizada',
        'Busca inteligente',
        'Versionamento de documentos',
        'Colaboração em equipe',
        'Acesso controlado',
      ],
    },
  ]

  return (
    <section id="solutions" className="py-24 bg-gradient-to-b from-slate-800 to-slate-900 relative overflow-hidden">
      {/* Background Decoration */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
          backgroundSize: '40px 40px',
        }} />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <span className="inline-block px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-full text-blue-400 text-sm font-medium mb-4">
            Nossas Soluções
          </span>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Tecnologia que
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent"> Transforma</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Soluções completas de IA para revolucionar sua prática jurídica
          </p>
        </motion.div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <ServiceCard
              key={service.title}
              {...service}
              delay={index * 0.1}
            />
          ))}
        </div>

        {/* CTA Section */}
        <motion.div
          className="mt-16 text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <p className="text-gray-400 mb-6">
            Não encontrou o que procura? Temos soluções personalizadas para suas necessidades.
          </p>
          <motion.button
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-semibold text-lg shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 transition-all"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre os serviços da Genesys Tecnologia.', '_blank')}
          >
            Fale com um Especialista
          </motion.button>
        </motion.div>
      </div>
    </section>
  )
}

