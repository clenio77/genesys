'use client'

import Link from 'next/link'
import { FaBrain, FaFileContract, FaSearch, FaRobot, FaShieldAlt, FaArrowRight, FaCheck } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

export default function ProdutosPage() {
  const produtos = [
    {
      id: 'kermartin-ia',
      nome: 'Kermartin IA',
      tagline: 'Plataforma jurídica com IA',
      descricao: 'Produto central da Genesys: análise jurídica por blocos, upload de documentos, pesquisa, perfis estratégicos e módulos especializados por área.',
      icon: FaBrain,
      gradient: 'from-purple-600 to-pink-600',
      link: '/produtos/kermartin-ia',
      features: [
        'Blocos de análise penal e júri',
        'Módulos civil, trânsito e tributário',
        'Auditoria pública e licitações',
        'Análise de perfis estratégicos',
        'Anonimização e guardrails LGPD',
        'API e interface web Django/React'
      ],
      stats: {
        precisao: 'BMAD',
        tempo: '6+ blocos',
        economia: '5 áreas'
      },
      destaque: true
    },
    {
      id: 'implementacao-kermartin',
      nome: 'Implementação Kermartin',
      tagline: 'Serviço de onboarding e adoção',
      descricao: 'Diagnóstico, parametrização, treinamento e implantação do Kermartin no fluxo real do escritório ou departamento jurídico.',
      icon: FaRobot,
      gradient: 'from-blue-600 to-cyan-600',
      link: '/servicos',
      features: [
        'Mapeamento de casos de uso',
        'Configuração de módulos e permissões',
        'Treinamento da equipe',
        'Playbooks por área jurídica',
        'Métricas de adoção',
        'Suporte de implantação'
      ],
      stats: {
        precisao: 'Guiado',
        tempo: '30-90 dias',
        economia: 'Adoção'
      }
    },
    {
      id: 'automacao-documentos',
      nome: 'Automação de Documentos',
      tagline: 'Fluxos conectados ao Kermartin',
      descricao: 'Automação de upload, triagem, análise e geração assistida de estruturas de peças e relatórios jurídicos.',
      icon: FaFileContract,
      gradient: 'from-amber-600 to-orange-600',
      link: '/servicos/automacao-processos',
      features: [
        'Processamento de PDFs e textos',
        'Estruturação de peças civis',
        'Relatórios jurídicos em Markdown',
        'Templates customizados',
        'Integrações operacionais',
        'Rotinas de acompanhamento'
      ],
      stats: {
        precisao: 'Fluxo',
        tempo: 'Sob medida',
        economia: 'Horas'
      }
    },
    {
      id: 'governanca-lgpd',
      nome: 'Governança e LGPD',
      tagline: 'Segurança para IA jurídica',
      descricao: 'Camada de privacidade, validação, anonimização e documentação para uso responsável de IA em dados jurídicos sensíveis.',
      icon: FaShieldAlt,
      gradient: 'from-cyan-600 to-blue-600',
      link: '/servicos/compliance-lgpd',
      features: [
        'Anonimização antes do LLM',
        'Validação de entrada',
        'Controle de acesso',
        'RIPD e documentação de privacidade',
        'Logs e monitoramento',
        'Políticas de uso interno'
      ],
      stats: {
        precisao: 'LGPD',
        tempo: 'Contínuo',
        economia: 'Risco'
      }
    },
    {
      id: 'auditoria-publica',
      nome: 'Auditoria Pública IA',
      tagline: 'Licitações, contratos e evidências',
      descricao: 'Módulo Kermartin para analisar licitações, detectar irregularidades, montar evidências, score de risco e dashboard executivo.',
      icon: FaSearch,
      gradient: 'from-green-600 to-emerald-600',
      link: '/produtos/kermartin-ia',
      features: [
        'Análise de licitações',
        'Detecção de irregularidades',
        'Análise de padrões',
        'Score de risco',
        'Relatório de evidências',
        'Dashboard executivo'
      ],
      stats: {
        precisao: 'Score',
        tempo: 'BI',
        economia: 'Controle'
      }
    }
  ]

  return (
    <>
      <SEOHead
        title="Produtos - Genesys Tecnologia | Soluções de IA Jurídica"
        description="Kermartin IA é o produto central da Genesys. Conheça a plataforma e os serviços de implantação, operação, automação e governança."
        keywords="kermartin ia, implantação kermartin, plataforma ia jurídica, automação jurídica, compliance ia"
        canonical="https://genesys-tecnologia.com.br/produtos"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">
            Nossos Produtos
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-8">
            Kermartin como produto central, com serviços Genesys para implantação, automação e governança
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-400">
            <div className="flex items-center gap-2">
              <FaCheck className="text-green-400" />
              <span>Arquitetura BMAD</span>
            </div>
            <div className="flex items-center gap-2">
              <FaCheck className="text-green-400" />
              <span>Módulos por área</span>
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
            {produtos.map((produto) => {
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
                        href={produto.link}
                        className={`block w-full bg-gradient-to-r ${produto.gradient} text-white px-6 py-3 rounded-lg font-semibold text-center hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 group-hover:scale-105`}
                      >
                        <span className="flex items-center justify-center gap-2">
                          Conhecer oferta
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
            Pronto para implantar o Kermartin?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Agende uma demonstração e veja os módulos reais aplicados a documentos e casos do seu fluxo
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
    </>
  )
}

