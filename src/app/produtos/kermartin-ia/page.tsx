'use client'

import Image from 'next/image'
import Link from 'next/link'
import { FaBrain, FaCheck, FaRocket, FaChartLine, FaUsers, FaArrowRight, FaPlay, FaDownload } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

export default function KermartinIAPage() {
  const modulos = [
    {
      nome: 'Análise de Jurisprudência',
      descricao: 'IA avançada para análise semântica de decisões judiciais',
      icon: FaChartLine,
      features: ['Busca semântica', 'Análise de padrões', 'Resumos automáticos', 'Citações relevantes']
    },
    {
      nome: 'Consultas Inteligentes',
      descricao: 'Faça perguntas em linguagem natural e receba respostas precisas',
      icon: FaBrain,
      features: ['NLP avançado', 'Contexto jurídico', 'Respostas fundamentadas', 'Múltiplas fontes']
    },
    {
      nome: 'Agente Klaus',
      descricao: 'Assistente virtual especializado em direito brasileiro',
      icon: FaUsers,
      features: ['Disponível 24/7', 'Aprendizado contínuo', 'Personalização', 'Integração completa']
    },
    {
      nome: 'Automação de Documentos',
      descricao: 'Geração automática de peças e documentos jurídicos',
      icon: FaRocket,
      features: ['Templates inteligentes', 'Preenchimento automático', 'Revisão de IA', 'Exportação múltipla']
    }
  ]

  const planos = [
    {
      nome: 'Starter',
      preco: 'R$ 497',
      periodo: '/mês',
      descricao: 'Ideal para advogados autônomos',
      features: [
        '1 usuário',
        '100 consultas/mês',
        'Análise de jurisprudência',
        'Suporte por email',
        'Atualizações incluídas'
      ],
      destaque: false
    },
    {
      nome: 'Professional',
      preco: 'R$ 1.497',
      periodo: '/mês',
      descricao: 'Para escritórios de médio porte',
      features: [
        'Até 5 usuários',
        '500 consultas/mês',
        'Todos os módulos',
        'Agente Klaus incluído',
        'Suporte prioritário',
        'Treinamento online',
        'API de integração'
      ],
      destaque: true
    },
    {
      nome: 'Enterprise',
      preco: 'Personalizado',
      periodo: '',
      descricao: 'Solução completa para grandes escritórios',
      features: [
        'Usuários ilimitados',
        'Consultas ilimitadas',
        'Customização completa',
        'Suporte dedicado 24/7',
        'Treinamento presencial',
        'SLA garantido',
        'Infraestrutura dedicada'
      ],
      destaque: false
    }
  ]

  const casos = [
    {
      cliente: 'Silva & Associados',
      resultado: '70% redução em tempo de análise',
      descricao: 'Escritório com 15 advogados reduziu drasticamente o tempo de análise de contratos'
    },
    {
      cliente: 'Mendes Advocacia',
      resultado: '3x aumento em produtividade',
      descricao: 'Advogado autônomo triplicou sua capacidade de atendimento'
    },
    {
      cliente: 'TechCorp Brasil',
      resultado: 'R$ 50K economia/mês',
      descricao: 'Departamento jurídico economizou significativamente em custos operacionais'
    }
  ]

  return (
    <>
      <SEOHead
        title="Kermartin IA - Assistente Jurídico Cibernético | Genesys Tecnologia"
        description="Kermartin IA: A plataforma mais completa de IA para análise jurídica do Brasil. Agente Klaus integrado, análise de jurisprudência e consultas inteligentes 24/7."
        keywords="kermartin ia, assistente jurídico ia, agente klaus, análise jurisprudência ia, consultas jurídicas inteligentes"
        canonical="https://genesys-tecnologia.com.br/produtos/kermartin-ia"
        ogImage="/images/kermartin-logo.png"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
            backgroundSize: '40px 40px',
          }} />
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-block bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full text-sm font-bold mb-6">
                🌟 Produto Mais Vendido
              </div>

              <div className="flex items-center gap-4 mb-6">
                <Image
                  src="/images/kermartin-logo.png"
                  alt="Kermartin IA"
                  width={80}
                  height={80}
                  className="object-contain"
                />
                <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
                  Kermartin IA
                </h1>
              </div>
              <p className="text-2xl text-cyan-400 mb-6 font-semibold">
                Assistente Jurídico Cibernético
              </p>
              <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                A plataforma mais completa de IA para análise jurídica do Brasil. 
                Com o agente Klaus integrado, você tem um assistente virtual especializado 
                trabalhando 24/7 para você.
              </p>

              <div className="flex flex-wrap gap-4 mb-8">
                <Link
                  href="#planos"
                  className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-lg font-bold hover:shadow-xl hover:shadow-purple-500/50 transition-all hover:scale-105 flex items-center gap-2"
                >
                  Começar Agora
                  <FaArrowRight />
                </Link>
                <button className="bg-slate-800 text-white px-8 py-4 rounded-lg font-bold hover:bg-slate-700 transition-all flex items-center gap-2">
                  <FaPlay />
                  Ver Demo
                </button>
              </div>

              <div className="grid grid-cols-3 gap-6">
                <div>
                  <div className="text-3xl font-bold text-purple-400">99.2%</div>
                  <div className="text-sm text-gray-400">Precisão</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-pink-400">10x</div>
                  <div className="text-sm text-gray-400">Mais Rápido</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-cyan-400">50K+</div>
                  <div className="text-sm text-gray-400">Casos Analisados</div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="relative aspect-square rounded-3xl overflow-hidden bg-gradient-to-br from-purple-600/20 to-pink-600/20 backdrop-blur-sm border border-purple-500/30 p-8">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 to-pink-600/10" />
                <div className="relative z-10 flex items-center justify-center h-full">
                  <Image
                    src="/images/kermartin-logo.png"
                    alt="Kermartin IA Logo"
                    width={400}
                    height={400}
                    className="object-contain drop-shadow-2xl"
                    priority
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Módulos Section */}
      <section className="py-20 px-4 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              12 Módulos Disponíveis
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Funcionalidades completas para transformar sua prática jurídica
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {modulos.map((modulo, index) => {
              const Icon = modulo.icon
              return (
                <div
                  key={index}
                  className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-purple-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/20"
                >
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl flex items-center justify-center text-white text-2xl flex-shrink-0">
                      <Icon />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-white mb-2">{modulo.nome}</h3>
                      <p className="text-gray-300">{modulo.descricao}</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    {modulo.features.map((feature, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-gray-300">
                        <FaCheck className="text-green-400 text-sm flex-shrink-0" />
                        <span className="text-sm">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Casos de Sucesso */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Casos de Sucesso
            </h2>
            <p className="text-xl text-gray-300">
              Resultados reais de clientes que transformaram sua prática
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {casos.map((caso, index) => (
              <div
                key={index}
                className="bg-gradient-to-br from-purple-600/10 to-pink-600/10 backdrop-blur-sm rounded-2xl p-8 border border-purple-500/30"
              >
                <div className="text-3xl font-bold text-purple-400 mb-4">{caso.resultado}</div>
                <div className="text-xl font-semibold text-white mb-2">{caso.cliente}</div>
                <p className="text-gray-300">{caso.descricao}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Planos e Preços */}
      <section id="planos" className="py-20 px-4 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Planos e Preços
            </h2>
            <p className="text-xl text-gray-300">
              Escolha o plano ideal para seu escritório
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {planos.map((plano, index) => (
              <div
                key={index}
                className={`relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border transition-all duration-300 hover:scale-105 ${
                  plano.destaque
                    ? 'border-purple-500 shadow-2xl shadow-purple-500/30'
                    : 'border-slate-700 hover:border-purple-500/50'
                }`}
              >
                {plano.destaque && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-2 rounded-full text-sm font-bold">
                    Mais Popular
                  </div>
                )}

                <h3 className="text-2xl font-bold text-white mb-2">{plano.nome}</h3>
                <p className="text-gray-400 mb-6">{plano.descricao}</p>

                <div className="mb-6">
                  <span className="text-5xl font-bold text-white">{plano.preco}</span>
                  <span className="text-gray-400">{plano.periodo}</span>
                </div>

                <ul className="space-y-3 mb-8">
                  {plano.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center gap-2 text-gray-300">
                      <FaCheck className="text-green-400 flex-shrink-0" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <Link
                  href="#contact"
                  className={`block w-full text-center px-6 py-4 rounded-lg font-bold transition-all ${
                    plano.destaque
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:shadow-xl hover:shadow-purple-500/50'
                      : 'bg-slate-700 text-white hover:bg-slate-600'
                  }`}
                >
                  Começar Agora
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl p-12">
          <h2 className="text-4xl font-bold text-white mb-4">
            Pronto para revolucionar sua prática jurídica?
          </h2>
          <p className="text-xl text-purple-100 mb-8">
            Comece hoje mesmo com 14 dias de teste grátis
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="#contact"
              className="bg-white text-purple-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
            >
              Iniciar Teste Grátis
            </Link>
            <button className="bg-purple-800 text-white px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105 flex items-center gap-2">
              <FaDownload />
              Baixar Brochure
            </button>
          </div>
        </div>
      </section>

      <Footer />
      </div>
    </>
  )
}

