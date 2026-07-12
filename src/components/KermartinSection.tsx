'use client'

import Image from 'next/image'
import { FaCheck, FaBrain, FaSearch, FaRobot, FaChartLine } from 'react-icons/fa'

export default function KermartinSection() {
  return (
    <section id="products" className="py-20 bg-gradient-to-b from-genesys-dark to-genesys-navy">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold font-playfair mb-6">
            <span className="gradient-text">Nossos Produtos</span>
          </h2>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Plataforma jurídica com IA — análise por blocos, pesquisa com fontes, perfis estratégicos e automação assistida
          </p>
        </div>
        
        {/* Kermartin IA Main Card */}
        <div className="bg-gradient-to-r from-blue-900 to-purple-900 rounded-2xl p-8 mb-16 hover-lift">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="flex items-center mb-6">
                <div className="w-16 h-16 rounded-xl mr-4 relative overflow-hidden cyber-glow kermartin-container" style={{ minHeight: '64px' }}>
                  <Image
                    src="/images/kermartin-logo.png"
                    alt="Kermartin IA Logo"
                    fill
                    sizes="(max-width: 768px) 50vw, 25vw"
                    className="object-contain rounded-xl hover:scale-110 transition-transform duration-300 kermartin-logo"
                    style={{
                      background: 'transparent !important',
                      border: 'none !important',
                      outline: 'none !important',
                      boxShadow: 'none !important',
                      backgroundColor: 'transparent !important'
                    }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-600/10 rounded-xl"></div>
                  <div className="absolute -inset-1 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 opacity-20 blur-sm"></div>
                </div>
                <div>
                  <h3 className="text-3xl font-bold gradient-text font-playfair">Kermartin IA</h3>
                  <p className="text-slate-100 text-lg">Plataforma Jurídica com IA</p>
                </div>
              </div>
              
              <p className="text-slate-100 text-lg leading-relaxed mb-6">
                O Kermartin IA é uma plataforma de análise jurídica com arquitetura BMAD. Ele organiza documentos e casos em blocos de raciocínio para apoiar análise penal, civil, trânsito, tributária, auditoria pública e criação de perfis estratégicos.
              </p>
              
              <div className="space-y-3 mb-8">
                <div className="flex items-center space-x-3">
                  <FaCheck className="text-green-400 text-lg" />
                  <span className="text-slate-100">Análise por blocos e subetapas</span>
                </div>
                <div className="flex items-center space-x-3">
                  <FaCheck className="text-green-400 text-lg" />
                  <span className="text-slate-100">Módulos penal, civil, trânsito e tributário</span>
                </div>
                <div className="flex items-center space-x-3">
                  <FaCheck className="text-green-400 text-lg" />
                  <span className="text-slate-100">Auditoria pública, licitações e score de risco</span>
                </div>
                <div className="flex items-center space-x-3">
                  <FaCheck className="text-green-400 text-lg" />
                  <span className="text-slate-100">Anonimização, guardrails e documentação LGPD</span>
                </div>
              </div>
              
              <button className="btn-primary">
                Conhecer a Plataforma
              </button>
            </div>
            
            <div className="relative">
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
                <div className="text-center">
                  <div className="w-32 h-32 mx-auto mb-4 relative cyber-glow kermartin-container">
                    <Image
                      src="/images/kermartin-logo.png"
                      alt="Kermartin IA Logo"
                      fill
                      sizes="(max-width: 768px) 50vw, 25vw"
                      className="object-contain rounded-full hover:scale-110 transition-transform duration-300 kermartin-logo"
                      style={{
                        background: 'transparent !important',
                        border: 'none !important',
                        outline: 'none !important',
                        boxShadow: 'none !important',
                        backgroundColor: 'transparent !important'
                      }}
                    />
                  </div>
                  
                  <h4 className="text-2xl font-bold gradient-text font-playfair mb-2">Kermartin IA</h4>
                  <p className="text-genesys-cream mb-6">Plataforma Jurídica com IA</p>
                  
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className="bg-white/10 rounded-lg p-4">
                      <div className="text-2xl font-bold gradient-text">6+</div>
                      <div className="text-sm text-genesys-slate">Blocos de Análise</div>
                    </div>
                    <div className="bg-white/10 rounded-lg p-4">
                      <div className="text-2xl font-bold gradient-text">5</div>
                      <div className="text-sm text-genesys-slate">Áreas Jurídicas</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="feature-card text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <FaBrain className="text-2xl text-white" />
            </div>
            <h3 className="text-xl font-semibold mb-3 font-playfair">Orquestração BMAD</h3>
            <p className="text-genesys-slate text-sm">
              Orquestração por blocos, persona jurídica e instruções especializadas por área.
            </p>
          </div>
          
          <div className="feature-card text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <FaSearch className="text-2xl text-white" />
            </div>
            <h3 className="text-xl font-semibold mb-3 font-playfair">Pesquisa e Fontes</h3>
            <p className="text-genesys-slate text-sm">
              RAG integrado: bases privadas, precedentes e guardrails de citação — configurados na implantação Genesys.
            </p>
          </div>
          
          <div className="feature-card text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <FaRobot className="text-2xl text-white" />
            </div>
            <h3 className="text-xl font-semibold mb-3 font-playfair">Documentos e Fluxos</h3>
            <p className="text-genesys-slate text-sm">
              Upload, triagem, análise e estruturas de peças em fluxos jurídicos repetíveis.
            </p>
          </div>
          
          <div className="feature-card text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-orange-500 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <FaChartLine className="text-2xl text-white" />
            </div>
            <h3 className="text-xl font-semibold mb-3 font-playfair">Auditoria e Risco</h3>
            <p className="text-genesys-slate text-sm">
              Licitações, irregularidades, padrões, evidências e painéis executivos.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
