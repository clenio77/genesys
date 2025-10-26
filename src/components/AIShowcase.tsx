'use client'

import { FaBrain, FaRobot, FaChartLine, FaDatabase, FaNetworkWired, FaCog } from 'react-icons/fa'

export default function AIShowcase() {
  const technologies = [
    { name: 'Machine Learning', icon: FaBrain, color: 'from-blue-500 to-cyan-500' },
    { name: 'NLP', icon: FaRobot, color: 'from-purple-500 to-pink-500' },
    { name: 'Analytics', icon: FaChartLine, color: 'from-emerald-500 to-teal-500' },
    { name: 'Big Data', icon: FaDatabase, color: 'from-amber-500 to-orange-500' },
    { name: 'Neural Networks', icon: FaNetworkWired, color: 'from-indigo-500 to-blue-500' },
    { name: 'Automation', icon: FaCog, color: 'from-rose-500 to-red-500' },
  ]

  const metrics = [
    { label: 'Precisão', value: '95%', description: 'Taxa de acurácia' },
    { label: 'Velocidade', value: '10x', description: 'Mais rápido' },
    { label: 'Economia', value: '60%', description: 'Redução de custos' },
    { label: 'Satisfação', value: '4.9/5', description: 'Avaliação média' },
  ]

  return (
    <section className="py-24 bg-gradient-to-b from-slate-900 to-slate-800 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `linear-gradient(to right, rgba(59, 130, 246, 0.1) 1px, transparent 1px),
                           linear-gradient(to bottom, rgba(59, 130, 246, 0.1) 1px, transparent 1px)`,
          backgroundSize: '40px 40px',
        }} />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Section Header */}
        <div className="text-center mb-16">
          <span className="inline-block px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-full text-blue-400 text-sm font-medium mb-4">
            Tecnologia de Ponta
          </span>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Inteligência Artificial
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent"> Avançada</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Nossa plataforma utiliza as mais recentes tecnologias de IA para entregar resultados excepcionais
          </p>
        </div>

        {/* Technologies Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-16">
          {technologies.map((tech) => (
            <div
              key={tech.name}
              className="group p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition-all duration-300"
            >
              <div className="text-center">
                <tech.icon className={`text-4xl mb-3 mx-auto bg-gradient-to-r ${tech.color} bg-clip-text text-transparent`} />
                <p className="text-sm text-gray-300 font-medium">{tech.name}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
          {metrics.map((metric) => (
            <div
              key={metric.label}
              className="text-center p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:bg-white/10 transition-all duration-300"
            >
              <div className="text-4xl font-bold text-white mb-2">{metric.value}</div>
              <div className="text-lg text-gray-300 font-medium mb-1">{metric.label}</div>
              <div className="text-sm text-gray-400">{metric.description}</div>
            </div>
          ))}
        </div>

        {/* Process Flow */}
        <div className="text-center">
          <h3 className="text-2xl font-bold text-white mb-8">Como Funciona</h3>
          <div className="flex flex-col md:flex-row items-center justify-center gap-8">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">1</span>
              </div>
              <span className="text-gray-300">Entrada de Dados</span>
            </div>
            <div className="hidden md:block w-8 h-0.5 bg-gray-600"></div>
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">2</span>
              </div>
              <span className="text-gray-300">Processamento IA</span>
            </div>
            <div className="hidden md:block w-8 h-0.5 bg-gray-600"></div>
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">3</span>
              </div>
              <span className="text-gray-300">Resultados</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}