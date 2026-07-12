'use client'

import Link from 'next/link'
import { FaBrain, FaHeadset, FaRobot, FaShieldAlt, FaPlug, FaCheck, FaArrowRight, FaUsers, FaClock, FaAward } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

type Servico = {
  id: string
  nome: string
  tagline: string
  descricao: string
  icon: typeof FaBrain
  gradient: string
  link: string
  features: string[]
  beneficios: string[]
  investimento: string
  duracao: string
  categoria: 'principal' | 'complementar'
}

export default function ServicosPage() {
  const servicos: Servico[] = [
    {
      id: 'implantacao-kermartin',
      nome: 'Implantação do Kermartin',
      tagline: 'Onboarding guiado no fluxo real',
      descricao: 'Implementamos o Kermartin no escritório ou departamento jurídico: módulos por área, permissões, bases documentais, treinamento e governança de uso.',
      icon: FaBrain,
      gradient: 'from-purple-600 to-indigo-600',
      link: '/produtos/kermartin-ia',
      categoria: 'principal',
      features: [
        'Diagnóstico do fluxo jurídico',
        'Configuração de módulos (penal, civil, trânsito, tributário)',
        'Base privada e conectores de pesquisa',
        'Treinamento prático da equipe',
        'Playbooks de prompts e revisão humana',
        'Métricas de adoção pós-go-live',
      ],
      beneficios: [
        'IA integrada à rotina do escritório',
        'Menor risco de uso inadequado',
        'Adoção acompanhada por especialistas Genesys',
      ],
      investimento: 'A partir de R$ 5.000/mês',
      duracao: '30–90 dias',
    },
    {
      id: 'operacao-kermartin',
      nome: 'Operação e Suporte do Kermartin',
      tagline: 'Continuidade e evolução assistida',
      descricao: 'Operamos e damos suporte contínuo ao Kermartin: monitoramento, ajustes de módulos, análises assistidas sob demanda e revisão humana antes da entrega.',
      icon: FaHeadset,
      gradient: 'from-blue-600 to-cyan-600',
      link: '/produtos/kermartin-ia',
      categoria: 'principal',
      features: [
        'Suporte técnico e operacional',
        'Análise penal por blocos e subetapas',
        'Deep scan civil e estratégia de execução',
        'Auditoria pública e licitações',
        'Relatórios estruturados em Markdown jurídico',
        'Revisão técnica antes da entrega',
      ],
      beneficios: [
        'Equipe não precisa operar tudo sozinha',
        'Resposta estruturada para casos complexos',
        'Evolução contínua dos fluxos configurados',
      ],
      investimento: 'Projeto ou assinatura mensal',
      duracao: 'Contínuo',
    },
    {
      id: 'automacao-processos',
      nome: 'Automação de Processos',
      tagline: 'Documentos e fluxos conectados',
      descricao: 'Automatizamos upload, triagem, geração assistida de peças, notificações e rotinas operacionais integradas ao Kermartin.',
      icon: FaRobot,
      gradient: 'from-amber-600 to-orange-600',
      link: '/servicos/automacao-processos',
      categoria: 'complementar',
      features: [
        'Geração assistida de documentos',
        'Fluxos de trabalho inteligentes',
        'Integração com sistemas internos',
        'Notificações automáticas',
        'Templates personalizáveis',
        'APIs e webhooks',
      ],
      beneficios: [
        'Menos trabalho manual repetitivo',
        'Fluxos padronizados por área',
        'Maior rastreabilidade operacional',
      ],
      investimento: 'A partir de R$ 3.000/mês',
      duracao: 'Contínuo',
    },
    {
      id: 'compliance-lgpd',
      nome: 'Governança, Compliance e LGPD',
      tagline: 'IA jurídica com controle de risco',
      descricao: 'Desenhamos políticas de uso, anonimização, validação de entrada, controle de acesso e documentação de privacidade para operação segura do Kermartin.',
      icon: FaShieldAlt,
      gradient: 'from-rose-600 to-red-600',
      link: '/servicos/compliance-lgpd',
      categoria: 'complementar',
      features: [
        'Anonimização antes do LLM',
        'Validação de dados sensíveis',
        'RIPD e políticas internas',
        'Controle de permissões por perfil',
        'Logs e auditoria',
        'Treinamento de uso responsável',
      ],
      beneficios: [
        'Redução de risco regulatório',
        'Uso consistente da IA pela equipe',
        'Documentação pronta para auditoria',
      ],
      investimento: 'A partir de R$ 4.000/mês',
      duracao: 'Contínuo',
    },
    {
      id: 'integracao-sistemas',
      nome: 'Integração com Sistemas',
      tagline: 'PJe, ERP, CRM e ferramentas internas',
      descricao: 'Conectamos o Kermartin a tribunais, sistemas de gestão, CRM, comunicação e bases documentais existentes do cliente.',
      icon: FaPlug,
      gradient: 'from-indigo-600 to-blue-600',
      link: '/integracoes',
      categoria: 'complementar',
      features: [
        'Integração com PJe, e-SAJ e Eproc',
        'WhatsApp, Slack e Google Workspace',
        'CRM e ERP corporativos',
        'APIs REST e webhooks',
        'Sincronização de documentos',
        'Mapeamento de fluxos existentes',
      ],
      beneficios: [
        'Kermartin no meio do fluxo atual',
        'Menos retrabalho de digitação',
        'Dados jurídicos centralizados',
      ],
      investimento: 'Sob proposta',
      duracao: 'Projeto ou contínuo',
    },
  ]

  const principais = servicos.filter((s) => s.categoria === 'principal')
  const complementares = servicos.filter((s) => s.categoria === 'complementar')

  const renderGrid = (items: Servico[]) => (
    <div className="grid md:grid-cols-2 gap-8">
      {items.map((servico) => {
        const Icon = servico.icon
        return (
          <div
            key={servico.id}
            className="group bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${servico.gradient} flex items-center justify-center text-white text-2xl`}>
                <Icon />
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">{servico.nome}</h3>
                <p className="text-cyan-400 text-sm">{servico.tagline}</p>
              </div>
            </div>

            <p className="text-gray-300 mb-6 text-sm">{servico.descricao}</p>

            <div className="space-y-2 mb-6">
              {servico.features.slice(0, 4).map((feature, idx) => (
                <div key={idx} className="flex items-center gap-2 text-gray-300">
                  <FaCheck className="text-green-400 text-xs flex-shrink-0" />
                  <span className="text-sm">{feature}</span>
                </div>
              ))}
            </div>

            <div className="bg-slate-900/50 rounded-lg p-4 mb-6">
              <h4 className="text-sm font-bold text-white mb-3">Benefícios:</h4>
              {servico.beneficios.map((beneficio, idx) => (
                <div key={idx} className="flex items-start gap-2 mb-2">
                  <FaCheck className="text-green-400 text-xs mt-1 flex-shrink-0" />
                  <span className="text-xs text-gray-300">{beneficio}</span>
                </div>
              ))}
            </div>

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

            <Link
              href={servico.link}
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
  )

  return (
    <>
      <SEOHead
        title="Serviços - Genesys Tecnologia | Implantação e Operação do Kermartin"
        description="Genesys implanta, opera e governa o Kermartin IA. Serviços principais de onboarding e suporte, complementados por automação, LGPD e integrações."
        keywords="implantação kermartin, operação kermartin ia, suporte ia jurídica, automação jurídica, governança lgpd, integração pje"
        canonical="https://genesys-tecnologia.com.br/servicos"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

        <section className="pt-32 pb-20 px-4">
          <div className="max-w-7xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Nossos Serviços
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-4">
              Genesys implanta e opera o Kermartin — plataforma jurídica com IA da nossa stack
            </p>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto mb-8">
              Pesquisa, bases privadas e análise por blocos são capacidades do produto Kermartin, não serviços avulsos.
              Nós configuramos, treinamos e mantêm tudo funcionando no seu fluxo.
            </p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto mt-12">
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <FaUsers className="text-4xl text-blue-400 mx-auto mb-2" />
                <div className="text-3xl font-bold text-white">5</div>
                <div className="text-sm text-gray-400">Áreas Jurídicas</div>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <FaClock className="text-4xl text-cyan-400 mx-auto mb-2" />
                <div className="text-3xl font-bold text-white">6+</div>
                <div className="text-sm text-gray-400">Blocos de Análise</div>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <FaAward className="text-4xl text-purple-400 mx-auto mb-2" />
                <div className="text-3xl font-bold text-white">BMAD</div>
                <div className="text-sm text-gray-400">Arquitetura</div>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <FaShieldAlt className="text-4xl text-green-400 mx-auto mb-2" />
                <div className="text-3xl font-bold text-white">100%</div>
                <div className="text-sm text-gray-400">LGPD Compliant</div>
              </div>
            </div>
          </div>
        </section>

        <section className="pb-12 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-10">
              <span className="inline-block px-4 py-2 bg-purple-500/10 border border-purple-500/30 rounded-full text-purple-300 text-sm font-medium mb-4">
                Serviços Principais
              </span>
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-3">
                Implantação e operação do Kermartin
              </h2>
              <p className="text-gray-400 max-w-2xl mx-auto">
                O núcleo do que a Genesys entrega: colocar o Kermartin para rodar e mantê-lo produtivo no dia a dia.
              </p>
            </div>
            {renderGrid(principais)}
          </div>
        </section>

        <section className="pb-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-10">
              <span className="inline-block px-4 py-2 bg-cyan-500/10 border border-cyan-500/30 rounded-full text-cyan-300 text-sm font-medium mb-4">
                Serviços Complementares
              </span>
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-3">
                Automação, governança e integração
              </h2>
              <p className="text-gray-400 max-w-2xl mx-auto">
                Camadas adicionais para conectar o Kermartin ao ecossistema do cliente com segurança e eficiência.
              </p>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {complementares.map((servico) => {
                const Icon = servico.icon
                return (
                  <div
                    key={servico.id}
                    className="group bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all duration-300"
                  >
                    <div className="flex items-center gap-4 mb-4">
                      <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${servico.gradient} flex items-center justify-center text-white text-xl`}>
                        <Icon />
                      </div>
                      <div>
                        <h3 className="text-lg font-bold text-white">{servico.nome}</h3>
                        <p className="text-cyan-400 text-xs">{servico.tagline}</p>
                      </div>
                    </div>
                    <p className="text-gray-300 mb-4 text-sm">{servico.descricao}</p>
                    <Link
                      href={servico.link}
                      className={`inline-flex items-center gap-2 text-sm font-semibold bg-gradient-to-r ${servico.gradient} bg-clip-text text-transparent hover:opacity-80`}
                    >
                      Ver detalhes <FaArrowRight className="text-cyan-400" />
                    </Link>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl p-12">
            <h2 className="text-4xl font-bold text-white mb-4">
              Pronto para implantar o Kermartin?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Agende uma conversa para mapear módulos, casos de uso e o plano de adoção da sua equipe
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                href="/produtos/kermartin-ia"
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
              >
                Conhecer o Kermartin
              </Link>
              <Link
                href="/#contact"
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
