'use client'

import Link from 'next/link'
import { FaBrain, FaFileAlt, FaChartLine, FaRobot, FaShieldAlt, FaDatabase, FaCheck, FaArrowRight, FaUsers, FaClock, FaAward } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

export default function ServicosPage() {
  const servicos = [
    {
      id: 'consultoria-ia',
      nome: 'Consultoria em IA Jurídica',
      tagline: 'Transformação Digital Personalizada',
      descricao: 'Consultoria especializada para implementar IA na sua prática jurídica com estratégia personalizada',
      icon: FaBrain,
      gradient: 'from-purple-600 to-indigo-600',
      features: [
        'Diagnóstico completo do escritório',
        'Plano de implementação personalizado',
        'Treinamento da equipe',
        'Suporte contínuo',
        'ROI garantido',
        'Acompanhamento mensal'
      ],
      beneficios: [
        'Redução de 70% em tarefas repetitivas',
        'Aumento de 3x na produtividade',
        'ROI em até 6 meses'
      ],
      investimento: 'A partir de R$ 5.000/mês',
      duracao: '3-6 meses'
    },
    {
      id: 'analise-juridica',
      nome: 'Análise Jurídica Inteligente',
      tagline: 'IA para Revisão de Contratos',
      descricao: 'Serviço de análise automática de contratos e documentos com IA avançada',
      icon: FaFileAlt,
      gradient: 'from-blue-600 to-cyan-600',
      features: [
        'Revisão automática de contratos',
        'Identificação de cláusulas críticas',
        'Análise de riscos',
        'Sugestões de melhorias',
        'Comparação com modelos',
        'Relatórios executivos'
      ],
      beneficios: [
        'Análise em 5 minutos vs 2 horas',
        '98.5% de precisão',
        'Economia de R$ 50K/ano'
      ],
      investimento: 'A partir de R$ 2.500/mês',
      duracao: 'Sob demanda'
    },
    {
      id: 'pesquisa-jurisprudencia',
      nome: 'Pesquisa de Jurisprudência',
      tagline: 'Busca Inteligente de Precedentes',
      descricao: 'Encontre precedentes relevantes com IA semântica e análise contextual avançada',
      icon: FaChartLine,
      gradient: 'from-green-600 to-emerald-600',
      features: [
        'Busca semântica avançada',
        'Análise de precedentes',
        'Resumos automáticos',
        'Citações relevantes',
        'Filtros inteligentes',
        'Exportação formatada'
      ],
      beneficios: [
        'Pesquisa 10x mais rápida',
        '97.8% de relevância',
        'Acesso a 50M+ decisões'
      ],
      investimento: 'A partir de R$ 1.500/mês',
      duracao: 'Ilimitado'
    },
    {
      id: 'automacao-processos',
      nome: 'Automação de Processos',
      tagline: 'Automatize Tarefas Repetitivas',
      descricao: 'Automatize documentos, fluxos de trabalho e notificações com IA',
      icon: FaRobot,
      gradient: 'from-amber-600 to-orange-600',
      features: [
        'Geração automática de documentos',
        'Fluxos de trabalho inteligentes',
        'Integração com sistemas',
        'Notificações automáticas',
        'Agendamento inteligente',
        'Templates personalizáveis'
      ],
      beneficios: [
        'Economia de 15h/semana',
        '99.5% de precisão',
        'ROI em 3 meses'
      ],
      investimento: 'A partir de R$ 3.000/mês',
      duracao: 'Contínuo'
    },
    {
      id: 'compliance-lgpd',
      nome: 'Compliance e LGPD',
      tagline: 'Monitoramento Inteligente',
      descricao: 'Sistema de compliance automatizado com IA para LGPD e regulamentações',
      icon: FaShieldAlt,
      gradient: 'from-rose-600 to-red-600',
      features: [
        'Monitoramento 24/7',
        'Alertas inteligentes',
        'Auditoria automática',
        'Relatórios de conformidade',
        'Gestão de riscos',
        'Criptografia avançada'
      ],
      beneficios: [
        '100% de conformidade',
        'Alertas em tempo real',
        'Redução de 80% em riscos'
      ],
      investimento: 'A partir de R$ 4.000/mês',
      duracao: 'Contínuo'
    },
    {
      id: 'gestao-conhecimento',
      nome: 'Gestão de Conhecimento',
      tagline: 'Base de Conhecimento Inteligente',
      descricao: 'Centralize e organize todo conhecimento jurídico com busca inteligente',
      icon: FaDatabase,
      gradient: 'from-indigo-600 to-blue-600',
      features: [
        'Base de conhecimento centralizada',
        'Busca inteligente',
        'Versionamento de documentos',
        'Colaboração em equipe',
        'Acesso controlado',
        'Backup automático'
      ],
      beneficios: [
        'Acesso instantâneo ao conhecimento',
        'Redução de 90% em buscas',
        'Colaboração eficiente'
      ],
      investimento: 'A partir de R$ 2.000/mês',
      duracao: 'Ilimitado'
    }
  ]

  return (
    <>
      <SEOHead
        title="Serviços - Genesys Tecnologia | Consultoria em IA Jurídica"
        description="Serviços especializados em Inteligência Artificial para o setor jurídico: Consultoria, Análise Jurídica, Pesquisa de Jurisprudência, Automação e Compliance."
        keywords="consultoria ia jurídica, análise jurídica inteligente, pesquisa jurisprudência, automação processos, compliance lgpd"
        canonical="https://genesys-tecnologia.com.br/servicos"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">
            Nossos Serviços
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-8">
            Soluções completas de IA para transformar sua prática jurídica
          </p>
          
          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto mt-12">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <FaUsers className="text-4xl text-blue-400 mx-auto mb-2" />
              <div className="text-3xl font-bold text-white">500+</div>
              <div className="text-sm text-gray-400">Clientes Ativos</div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <FaClock className="text-4xl text-cyan-400 mx-auto mb-2" />
              <div className="text-3xl font-bold text-white">10x</div>
              <div className="text-sm text-gray-400">Mais Rápido</div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <FaAward className="text-4xl text-purple-400 mx-auto mb-2" />
              <div className="text-3xl font-bold text-white">99%</div>
              <div className="text-sm text-gray-400">Satisfação</div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <FaShieldAlt className="text-4xl text-green-400 mx-auto mb-2" />
              <div className="text-3xl font-bold text-white">100%</div>
              <div className="text-sm text-gray-400">LGPD Compliant</div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {servicos.map((servico) => {
              const Icon = servico.icon
              return (
                <div
                  key={servico.id}
                  className="group bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20"
                >
                  {/* Icon & Title */}
                  <div className="flex items-center gap-4 mb-6">
                    <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${servico.gradient} flex items-center justify-center text-white text-2xl`}>
                      <Icon />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">{servico.nome}</h3>
                      <p className="text-cyan-400 text-sm">{servico.tagline}</p>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-gray-300 mb-6 text-sm">{servico.descricao}</p>

                  {/* Features */}
                  <div className="space-y-2 mb-6">
                    {servico.features.slice(0, 4).map((feature, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-gray-300">
                        <FaCheck className="text-green-400 text-xs flex-shrink-0" />
                        <span className="text-sm">{feature}</span>
                      </div>
                    ))}
                  </div>

                  {/* Benefícios */}
                  <div className="bg-slate-900/50 rounded-lg p-4 mb-6">
                    <h4 className="text-sm font-bold text-white mb-3">Benefícios:</h4>
                    {servico.beneficios.map((beneficio, idx) => (
                      <div key={idx} className="flex items-start gap-2 mb-2">
                        <FaCheck className="text-green-400 text-xs mt-1 flex-shrink-0" />
                        <span className="text-xs text-gray-300">{beneficio}</span>
                      </div>
                    ))}
                  </div>

                  {/* Pricing & Duration */}
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                      <div className="text-xs text-gray-400 mb-1">Investimento</div>
                      <div className="text-sm font-bold text-white">{servico.investimento}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-400 mb-1">Duração</div>
                      <div className="text-sm font-bold text-white">{servico.duracao}</div>
                    </div>
                  </div>

                  {/* CTA */}
                  <Link
                    href={`/servicos/${servico.id}`}
                    className={`block w-full bg-gradient-to-r ${servico.gradient} text-white px-6 py-3 rounded-lg font-semibold text-center hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 group-hover:scale-105 text-sm`}
                  >
                    <span className="flex items-center justify-center gap-2">
                      Saiba Mais
                      <FaArrowRight className="group-hover:translate-x-1 transition-transform" />
                    </span>
                  </Link>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl p-12">
          <h2 className="text-4xl font-bold text-white mb-4">
            Pronto para começar?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Agende uma consulta gratuita e descubra como podemos ajudar
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="#contact"
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
            >
              Agendar Consulta Gratuita
            </Link>
            <Link
              href="#contact"
              className="bg-blue-800 text-white px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
            >
              Falar com Especialista
            </Link>
          </div>
        </div>
      </section>

      <Footer />
      </div>
    </>
  )
}

