'use client'

import { FaRocket, FaPlay, FaBrain, FaFileAlt, FaDatabase, FaNetworkWired } from 'react-icons/fa'

export default function Hero() {
  return (
    <section id="home" className="min-h-screen neural-network-bg relative overflow-hidden pt-20">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500/20 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '4s' }}></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Main Hero Section */}
        <div className="text-center py-20">
          <h1 className="text-5xl md:text-7xl font-bold font-playfair mb-8">
            <span className="gradient-text">Tecnologia por Trás da</span>
            <br />
            <span className="text-white">Genesys</span>
          </h1>

          <p className="text-xl md:text-2xl text-slate-300 max-w-4xl mx-auto leading-relaxed mb-12">
            A mais avançada tecnologia de IA aplicada ao contexto jurídico brasileiro
          </p>

          {/* Call to Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-20">
            <a href="/#products" className="btn-primary flex items-center space-x-3 group">
              <FaRocket className="group-hover:animate-bounce" />
              <span>Descobrir Soluções</span>
            </a>

            <button
              onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de ver uma demonstração das soluções da Genesys Tecnologia.', '_blank')}
              className="btn-secondary flex items-center space-x-3 group"
            >
              <FaPlay className="group-hover:scale-110 transition-transform" />
              <span>Ver Demo</span>
            </button>
          </div>
        </div>

        {/* Professional Features Section */}
        <div className="grid lg:grid-cols-2 gap-12 items-center mb-20">
          {/* Left Column - Feature Cards */}
          <div className="space-y-8">
            <div className="professional-feature-card group">
              <div className="feature-icon bg-gradient-to-r from-blue-500 to-cyan-500">
                <FaBrain className="text-2xl text-white" />
              </div>
              <div className="feature-content">
                <h3 className="text-2xl font-bold text-white mb-3">Machine Learning Avançado</h3>
                <p className="text-slate-300 leading-relaxed">
                  Algoritmos de deep learning treinados especificamente com dados jurídicos brasileiros,
                  capazes de compreender nuances legais e contextos processuais complexos.
                </p>
              </div>
            </div>

            <div className="professional-feature-card group">
              <div className="feature-icon bg-gradient-to-r from-orange-500 to-red-500">
                <FaFileAlt className="text-2xl text-white" />
              </div>
              <div className="feature-content">
                <h3 className="text-2xl font-bold text-white mb-3">Processamento de Linguagem Natural</h3>
                <p className="text-slate-300 leading-relaxed">
                  NLP especializado em português jurídico para interpretação precisa de textos legais,
                  extração de informações relevantes e análise semântica avançada.
                </p>
              </div>
            </div>

            <div className="professional-feature-card group">
              <div className="feature-icon bg-gradient-to-r from-green-500 to-emerald-500">
                <FaDatabase className="text-2xl text-white" />
              </div>
              <div className="feature-content">
                <h3 className="text-2xl font-bold text-white mb-3">Big Data Jurídico</h3>
                <p className="text-slate-300 leading-relaxed">
                  Processamento de milhões de documentos jurídicos, decisões judiciais e legislações
                  para identificar padrões e gerar insights estratégicos.
                </p>
              </div>
            </div>
          </div>

          {/* Right Column - Main Feature Card */}
          <div className="relative">
            <div className="main-feature-card">
              <div className="feature-icon-large bg-gradient-to-r from-purple-500 to-blue-500">
                <FaNetworkWired className="text-4xl text-white" />
              </div>

              <h3 className="text-3xl font-bold text-white mb-4">Rede Neural Jurídica</h3>

              <p className="text-slate-200 text-lg leading-relaxed mb-8">
                Nossa IA utiliza uma arquitetura de rede neural especializada, treinada com mais de
                10 milhões de documentos jurídicos para oferecer análises precisas e contextualizadas.
              </p>

              <div className="grid grid-cols-2 gap-6">
                <div className="stat-card">
                  <div className="stat-number">99.2%</div>
                  <div className="stat-label">Precisão</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">10M+</div>
                  <div className="stat-label">Documentos</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white/50 rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>
  )
}
