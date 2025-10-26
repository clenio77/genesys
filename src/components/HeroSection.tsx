'use client'

import { FaRocket, FaBrain, FaChartLine, FaArrowDown } from 'react-icons/fa'
import { useEffect, useState } from 'react'

export default function HeroSection() {
  const [typedText, setTypedText] = useState('')
  const fullText = 'Inteligência Artificial Jurídica'
  
  useEffect(() => {
    let index = 0
    const timer = setInterval(() => {
      if (index <= fullText.length) {
        setTypedText(fullText.slice(0, index))
        index++
      } else {
        clearInterval(timer)
      }
    }, 100)
    
    return () => clearInterval(timer)
  }, [])

  const stats = [
    { value: '10k+', label: 'Documentos Analisados', icon: FaBrain },
    { value: '95%', label: 'Precisão IA', icon: FaChartLine },
    { value: '24/7', label: 'Disponibilidade', icon: FaRocket },
  ]

  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 pt-20">
      {/* Neural Network Background */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, rgba(59, 130, 246, 0.3) 1px, transparent 0)`,
          backgroundSize: '50px 50px',
        }} />
      </div>

      {/* Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/30 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/30 rounded-full blur-3xl animate-pulse" />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="max-w-5xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-full mb-8">
            <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
            <span className="text-blue-300 text-sm font-medium">
              Tecnologia de Ponta em IA Jurídica
            </span>
          </div>

          {/* Main Title */}
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-white via-blue-100 to-cyan-100 bg-clip-text text-transparent">
              Genesys Tecnologia
            </span>
          </h1>

          {/* Typing Effect Subtitle */}
          <div className="h-16 mb-8">
            <h2 className="text-2xl md:text-4xl text-blue-300 font-light">
              {typedText}
              <span className="animate-pulse">|</span>
            </h2>
          </div>

          {/* Description */}
          <p className="text-lg md:text-xl text-gray-300 mb-12 max-w-3xl mx-auto">
            Transforme sua prática jurídica com soluções de IA de última geração. 
            Análise inteligente, automação avançada e insights precisos para decisões estratégicas.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-semibold text-lg shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 transition-all hover:scale-105">
              Começar Gratuitamente
            </button>
            
            <button className="px-8 py-4 bg-white/10 backdrop-blur-sm border border-white/20 text-white rounded-lg font-semibold text-lg hover:bg-white/20 transition-all hover:scale-105">
              Ver Demonstração
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {stats.map((stat) => (
              <div
                key={stat.label}
                className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition-all hover:-translate-y-1"
              >
                <stat.icon className="text-4xl text-blue-400 mb-3 mx-auto" />
                <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
          <div className="flex flex-col items-center text-gray-400">
            <span className="text-sm mb-2">Role para explorar</span>
            <FaArrowDown className="text-xl animate-bounce" />
          </div>
        </div>
      </div>
    </section>
  )
}