'use client'

import { useState, useEffect } from 'react'
import { FaChevronLeft, FaChevronRight, FaRobot, FaCog, FaBrain, FaChartLine, FaShieldAlt, FaRocket } from 'react-icons/fa'

export default function ProductCarousel() {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [isAutoPlaying, setIsAutoPlaying] = useState(true)

  const products = [
    {
      id: 1,
      title: 'Kermartin IA',
      subtitle: 'Assistente Jurídico Cibernético',
      description: 'Solução completa de IA especializada em Direito Penal, desenvolvida em parceria com o Dr. Jader Mattos. Análise inteligente de jurisprudência e consultas contextualizadas.',
      icon: <FaBrain className="text-4xl" />,
      gradient: 'from-blue-500 to-purple-600',
      features: ['Análise de Jurisprudência', 'Consultas Inteligentes', 'Agente Klaus', 'Roadmap Completo'],
      stats: { precision: '99.2%', cases: '50K+' },
      image: '/images/kermartin-logo.png'
    },
    {
      id: 2,
      title: 'Automações IA',
      subtitle: 'Processos Inteligentes',
      description: 'Automação completa de processos jurídicos com IA avançada. Reduza tempo de análise em 80% e aumente precisão com algoritmos especializados.',
      icon: <FaCog className="text-4xl" />,
      gradient: 'from-green-500 to-emerald-600',
      features: ['Análise Automática', 'Geração de Documentos', 'Workflow Inteligente', 'Integração Total'],
      stats: { efficiency: '80%', time: '5x' },
      image: '/images/automation-icon.png'
    },
    {
      id: 3,
      title: 'Bots Jurídicos',
      subtitle: 'Assistentes Virtuais',
      description: 'Chatbots especializados em direito com conhecimento jurídico profundo. Atendimento 24/7 com respostas precisas e contextualizadas.',
      icon: <FaRobot className="text-4xl" />,
      gradient: 'from-orange-500 to-red-600',
      features: ['Atendimento 24/7', 'Conhecimento Jurídico', 'Respostas Contextualizadas', 'Integração WhatsApp'],
      stats: { availability: '24/7', accuracy: '95%' },
      image: '/images/bot-icon.png'
    },
    {
      id: 4,
      title: 'Analytics Jurídico',
      subtitle: 'Insights Inteligentes',
      description: 'Plataforma de analytics com IA para análise de dados jurídicos. Identifique padrões, tendências e oportunidades estratégicas.',
      icon: <FaChartLine className="text-4xl" />,
      gradient: 'from-purple-500 to-pink-600',
      features: ['Análise Preditiva', 'Dashboards Interativos', 'Relatórios Automáticos', 'Insights Estratégicos'],
      stats: { insights: '1000+', patterns: '500+' },
      image: '/images/analytics-icon.png'
    },
    {
      id: 5,
      title: 'Compliance IA',
      subtitle: 'Monitoramento Inteligente',
      description: 'Sistema de compliance automatizado com IA. Monitore regulamentações, identifique riscos e mantenha conformidade em tempo real.',
      icon: <FaShieldAlt className="text-4xl" />,
      gradient: 'from-cyan-500 to-blue-600',
      features: ['Monitoramento 24/7', 'Alertas Inteligentes', 'Relatórios de Conformidade', 'Gestão de Riscos'],
      stats: { compliance: '100%', alerts: 'Real-time' },
      image: '/images/compliance-icon.png'
    }
  ]

  useEffect(() => {
    if (!isAutoPlaying) return

    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % products.length)
    }, 5000)

    return () => clearInterval(interval)
  }, [isAutoPlaying, products.length])

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % products.length)
    setIsAutoPlaying(false)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + products.length) % products.length)
    setIsAutoPlaying(false)
  }

  const goToSlide = (index: number) => {
    setCurrentSlide(index)
    setIsAutoPlaying(false)
  }

  return (
    <section className="py-20 bg-gradient-to-b from-slate-900 to-slate-800 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold font-playfair mb-6">
            <span className="gradient-text">Nossos Produtos</span>
          </h2>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Soluções inovadoras de IA que transformam a prática jurídica moderna
          </p>
        </div>

        {/* Carousel Container */}
        <div className="relative">
          {/* Main Carousel */}
          <div className="carousel-container">
            <div 
              className="carousel-track"
              style={{ transform: `translateX(-${currentSlide * 100}%)` }}
            >
              {products.map((product) => (
                <div key={product.id} className="carousel-slide">
                  <div className={`product-card bg-gradient-to-br ${product.gradient} p-8 rounded-3xl shadow-2xl`}>
                    <div className="grid lg:grid-cols-2 gap-12 items-center">
                      {/* Left Side - Content */}
                      <div className="text-white">
                        <div className="flex items-center mb-6">
                          <div className="w-20 h-20 bg-white/20 rounded-2xl flex items-center justify-center mr-6 backdrop-blur-sm">
                            {product.icon}
                          </div>
                          <div>
                            <h3 className="text-3xl font-bold font-playfair">{product.title}</h3>
                            <p className="text-xl text-white/80">{product.subtitle}</p>
                          </div>
                        </div>

                        <p className="text-lg leading-relaxed mb-8 text-white/90">
                          {product.description}
                        </p>

                        {/* Features */}
                        <div className="grid grid-cols-2 gap-3 mb-8">
                          {product.features.map((feature, idx) => (
                            <div key={idx} className="flex items-center space-x-2">
                              <div className="w-2 h-2 bg-white rounded-full"></div>
                              <span className="text-white/80 text-sm">{feature}</span>
                            </div>
                          ))}
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-2 gap-6">
                          {Object.entries(product.stats).map(([key, value], idx) => (
                            <div key={idx} className="bg-white/10 rounded-xl p-4 text-center backdrop-blur-sm">
                              <div className="text-2xl font-bold">{value}</div>
                              <div className="text-sm text-white/70 capitalize">{key}</div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Right Side - Visual */}
                      <div className="relative">
                        <div className="product-visual bg-white/10 rounded-2xl p-8 backdrop-blur-sm border border-white/20">
                          <div className="text-center">
                            <div className="w-32 h-32 mx-auto mb-6 bg-white/20 rounded-full flex items-center justify-center">
                              {product.icon}
                            </div>
                            <h4 className="text-2xl font-bold mb-2">{product.title}</h4>
                            <p className="text-white/80 mb-6">{product.subtitle}</p>
                            
                            <button className="carousel-cta-btn">
                              <FaRocket className="mr-2" />
                              Conhecer Produto
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Navigation Controls */}
          <button 
            onClick={prevSlide}
            className="carousel-nav-btn carousel-nav-left"
            aria-label="Slide anterior"
          >
            <FaChevronLeft />
          </button>
          
          <button 
            onClick={nextSlide}
            className="carousel-nav-btn carousel-nav-right"
            aria-label="Próximo slide"
          >
            <FaChevronRight />
          </button>

          {/* Dots Indicator */}
          <div className="flex justify-center space-x-3 mt-8">
            {products.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`carousel-dot ${index === currentSlide ? 'active' : ''}`}
                aria-label={`Ir para slide ${index + 1}`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
