'use client'

import Image from 'next/image'
import Link from 'next/link'
import { FaBrain, FaFileContract, FaSearch, FaRobot, FaShieldAlt, FaArrowRight, FaCheck } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'

export default function ProdutosPage() {
  const produtos = [
    {
      id: 'kermartin-ia',
      nome: 'Kermartin IA',
      tagline: 'Assistente Jurídico Cibernético',
      descricao: 'Plataforma completa de IA para análise jurídica com agente Klaus integrado',
      icon: FaBrain,
      gradient: 'from-purple-600 to-pink-600',
      features: [
        'Análise de Jurisprudência',
        'Consultas Inteligentes',
        'Agente Klaus Integrado',
        'Roadmap Completo',
        '12 Módulos Disponíveis',
        '50K+ Casos Analisados'
      ],
      stats: {
        precisao: '99.2%',
        tempo: '10x mais rápido',
        economia: 'R$ 50K/mês'
      },
      destaque: true
    },
    {
      id: 'analise-contratos',
      nome: 'Análise de Contratos IA',
      tagline: 'Revisão Inteligente de Contratos',
      descricao: 'IA avançada para revisão automática, identificação de riscos e sugestões de melhorias',
      icon: FaFileContract,
      gradient: 'from-blue-600 to-cyan-600',
      features: [
        'Revisão automática em minutos',
        'Identificação de cláusulas críticas',
        'Análise de riscos',
        'Sugestões de melhorias',
        'Comparação com modelos',
        'Relatórios detalhados'
      ],
      stats: {
        precisao: '98.5%',
        tempo: '5 min/contrato',
        economia: '80% tempo'
      }
    },
    {
      id: 'pesquisa-juridica',
      nome: 'Pesquisa Jurídica IA',
      tagline: 'Busca Inteligente de Jurisprudência',
      descricao: 'Encontre precedentes relevantes com IA semântica e análise contextual',
      icon: FaSearch,
      gradient: 'from-green-600 to-emerald-600',
      features: [
        'Busca semântica avançada',
        'Análise de precedentes',
        'Resumos automáticos',
        'Citações relevantes',
        'Filtros inteligentes',
        'Exportação formatada'
      ],
      stats: {
        precisao: '97.8%',
        tempo: '2 min/pesquisa',
        economia: '90% tempo'
      }
    },
    {
      id: 'automacao-processos',
      nome: 'Automação de Processos',
      tagline: 'Automatize Tarefas Repetitivas',
      descricao: 'Ganhe tempo automatizando documentos, fluxos e notificações',
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
      stats: {
        precisao: '99.5%',
        tempo: '15 min/dia economizado',
        economia: '70% tarefas'
      }
    },
    {
      id: 'compliance-ia',
      nome: 'Compliance IA',
      tagline: 'Monitoramento Inteligente',
      descricao: 'Sistema de compliance automatizado com IA para LGPD e regulamentações',
      icon: FaShieldAlt,
      gradient: 'from-cyan-600 to-blue-600',
      features: [
        'Monitoramento 24/7',
        'Alertas inteligentes',
        'Auditoria automática',
        'Relatórios de conformidade',
        'Gestão de riscos',
        'Criptografia avançada'
      ],
      stats: {
        precisao: '100%',
        tempo: 'Real-time',
        economia: 'R$ 30K/mês'
      }
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      <PremiumHeader />
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">
            Nossos Produtos
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-8">
            Soluções de IA que transformam a prática jurídica
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-400">
            <div className="flex items-center gap-2">
              <FaCheck className="text-green-400" />
              <span>99%+ Precisão</span>
            </div>
            <div className="flex items-center gap-2">
              <FaCheck className="text-green-400" />
              <span>10x Mais Rápido</span>
            </div>
            <div className="flex items-center gap-2">
              <FaCheck className="text-green-400" />
              <span>LGPD Compliant</span>
            </div>
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {produtos.map((produto, index) => {
              const Icon = produto.icon
              return (
                <div
                  key={produto.id}
                  className={`group relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20 ${
                    produto.destaque ? 'md:col-span-2 lg:col-span-3' : ''
                  }`}
                >
                  {produto.destaque && (
                    <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-2 rounded-full text-sm font-bold">
                      🌟 Produto Destaque
                    </div>
                  )}

                  <div className={produto.destaque ? 'grid lg:grid-cols-2 gap-8' : ''}>
                    <div>
                      {/* Icon & Title */}
                      <div className="flex items-center gap-4 mb-6">
                        <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${produto.gradient} flex items-center justify-center text-white text-2xl`}>
                          <Icon />
                        </div>
                        <div>
                          <h3 className="text-2xl font-bold text-white">{produto.nome}</h3>
                          <p className="text-cyan-400 text-sm">{produto.tagline}</p>
                        </div>
                      </div>

                      {/* Description */}
                      <p className="text-gray-300 mb-6">{produto.descricao}</p>

                      {/* Features */}
                      <div className="space-y-2 mb-6">
                        {produto.features.map((feature, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-gray-300">
                            <FaCheck className="text-green-400 text-sm flex-shrink-0" />
                            <span className="text-sm">{feature}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div>
                      {/* Stats */}
                      <div className="grid grid-cols-3 gap-4 mb-6">
                        <div className="bg-slate-900/50 rounded-lg p-4 text-center">
                          <div className={`text-2xl font-bold bg-gradient-to-r ${produto.gradient} bg-clip-text text-transparent`}>
                            {produto.stats.precisao}
                          </div>
                          <div className="text-xs text-gray-400 mt-1">Precisão</div>
                        </div>
                        <div className="bg-slate-900/50 rounded-lg p-4 text-center">
                          <div className={`text-2xl font-bold bg-gradient-to-r ${produto.gradient} bg-clip-text text-transparent`}>
                            {produto.stats.tempo}
                          </div>
                          <div className="text-xs text-gray-400 mt-1">Velocidade</div>
                        </div>
                        <div className="bg-slate-900/50 rounded-lg p-4 text-center">
                          <div className={`text-2xl font-bold bg-gradient-to-r ${produto.gradient} bg-clip-text text-transparent`}>
                            {produto.stats.economia}
                          </div>
                          <div className="text-xs text-gray-400 mt-1">Economia</div>
                        </div>
                      </div>

                      {/* CTA */}
                      <Link
                        href={`/produtos/${produto.id}`}
                        className={`block w-full bg-gradient-to-r ${produto.gradient} text-white px-6 py-3 rounded-lg font-semibold text-center hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 group-hover:scale-105`}
                      >
                        <span className="flex items-center justify-center gap-2">
                          Conhecer {produto.nome}
                          <FaArrowRight className="group-hover:translate-x-1 transition-transform" />
                        </span>
                      </Link>
                    </div>
                  </div>
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
            Pronto para transformar sua prática jurídica?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Agende uma demonstração gratuita e veja nossos produtos em ação
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de agendar uma demonstração dos produtos da Genesys Tecnologia.', '_blank')}
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
            >
              Agendar Demonstração
            </button>
            <button
              onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre os serviços da Genesys Tecnologia.', '_blank')}
              className="bg-blue-800 text-white px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
            >
              Falar com Especialista
            </button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}

