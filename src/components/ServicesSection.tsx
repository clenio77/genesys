'use client'

import { motion } from 'framer-motion'
import ServiceCard from './ServiceCard'
import { FaBrain, FaHeadset, FaRobot, FaShieldAlt, FaPlug } from 'react-icons/fa'

export default function ServicesSection() {
  const services = [
    {
      title: 'Kermartin IA — Plataforma',
      description: 'Produto central: análise jurídica por blocos BMAD, upload de documentos, pesquisa com fontes, perfis estratégicos e módulos por área.',
      icon: FaBrain,
      gradient: 'from-blue-600 to-cyan-600',
      badge: 'Produto',
      link: '/produtos/kermartin-ia',
      features: [
        'Penal, civil, trânsito e tributário',
        'Auditoria pública e licitações',
        'RAG e base privada integrados',
        'Anonimização e guardrails LGPD',
        'Relatórios em Markdown jurídico',
      ],
    },
    {
      title: 'Implantação do Kermartin',
      description: 'Diagnóstico, parametrização de módulos, bases documentais, permissões e treinamento da equipe no uso seguro da plataforma.',
      icon: FaBrain,
      gradient: 'from-purple-600 to-pink-600',
      badge: 'Principal',
      link: '/servicos',
      features: [
        'Mapeamento de casos de uso',
        'Configuração por área jurídica',
        'Onboarding guiado (30–90 dias)',
        'Playbooks de prompts e revisão',
        'Métricas de adoção',
      ],
    },
    {
      title: 'Operação e Suporte',
      description: 'Suporte contínuo, análises assistidas sob demanda, ajustes de fluxo e revisão humana antes da entrega ao cliente interno.',
      icon: FaHeadset,
      gradient: 'from-indigo-600 to-blue-600',
      badge: 'Principal',
      link: '/servicos',
      features: [
        'Suporte técnico e operacional',
        'Análise penal, civil e tributária',
        'Licitações e score de risco',
        'Relatórios estruturados',
        'Evolução dos fluxos configurados',
      ],
    },
    {
      title: 'Automação de Processos',
      description: 'Upload, triagem, geração assistida de peças, notificações e integrações operacionais conectadas ao Kermartin.',
      icon: FaRobot,
      gradient: 'from-amber-600 to-orange-600',
      badge: 'Complementar',
      link: '/servicos/automacao-processos',
      features: [
        'Geração assistida de documentos',
        'Fluxos de trabalho inteligentes',
        'Templates por área jurídica',
        'APIs e webhooks',
        'Integração com sistemas internos',
      ],
    },
    {
      title: 'Governança, LGPD e Segurança',
      description: 'Anonimização, validação de entrada, controle de acesso e políticas de uso para reduzir risco na operação do Kermartin.',
      icon: FaShieldAlt,
      gradient: 'from-rose-600 to-red-600',
      badge: 'Complementar',
      link: '/servicos/compliance-lgpd',
      features: [
        'Anonimização antes do LLM',
        'Validação de dados sensíveis',
        'RIPD e documentação LGPD',
        'Perfis de acesso por usuário',
        'Logs e auditoria',
      ],
    },
    {
      title: 'Integração com Sistemas',
      description: 'Conexão do Kermartin a tribunais (PJe, e-SAJ), CRM, ERP, WhatsApp e ferramentas de produtividade do cliente.',
      icon: FaPlug,
      gradient: 'from-emerald-600 to-teal-600',
      badge: 'Complementar',
      link: '/integracoes',
      features: [
        'PJe, e-SAJ, Eproc',
        'WhatsApp e Google Workspace',
        'CRM e ERP corporativos',
        'APIs REST e webhooks',
        'Sincronização documental',
      ],
    },
  ]

  return (
    <section id="solutions" className="py-24 bg-gradient-to-b from-slate-800 to-slate-900 relative overflow-hidden">
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
          backgroundSize: '40px 40px',
        }} />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
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
            Kermartin no centro,
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent"> Genesys na implantação</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            A Genesys é a consultoria que implanta, opera e governa o Kermartin — plataforma jurídica com IA para análise, pesquisa e automação assistida
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <ServiceCard
              key={service.title}
              {...service}
              delay={index * 0.1}
            />
          ))}
        </div>

        <motion.div
          className="mt-16 text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <p className="text-gray-400 mb-6">
            Pesquisa jurisprudencial e gestão de conhecimento fazem parte do Kermartin — configuramos tudo na implantação.
          </p>
          <motion.button
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-semibold text-lg shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 transition-all"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre implantação e operação do Kermartin.', '_blank')}
          >
            Fale com um Especialista
          </motion.button>
        </motion.div>
      </div>
    </section>
  )
}
