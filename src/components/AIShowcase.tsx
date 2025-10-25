'use client'

import { motion } from 'framer-motion'
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
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
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
        </motion.div>

        {/* Neural Network Visualization */}
        <div className="mb-20">
          <motion.div
            className="relative max-w-4xl mx-auto h-64 flex items-center justify-center"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1 }}
          >
            {/* Central Node */}
            <motion.div
              className="absolute z-10 w-20 h-20 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center shadow-lg shadow-blue-500/50"
              animate={{
                scale: [1, 1.1, 1],
                boxShadow: [
                  '0 0 20px rgba(59, 130, 246, 0.5)',
                  '0 0 40px rgba(59, 130, 246, 0.8)',
                  '0 0 20px rgba(59, 130, 246, 0.5)',
                ],
              }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <FaBrain className="text-3xl text-white" />
            </motion.div>

            {/* Orbiting Nodes */}
            {technologies.map((tech, index) => {
              const angle = (index * 360) / technologies.length
              const radius = 150
              const x = Math.cos((angle * Math.PI) / 180) * radius
              const y = Math.sin((angle * Math.PI) / 180) * radius

              return (
                <motion.div
                  key={tech.name}
                  className="absolute"
                  style={{
                    left: `calc(50% + ${x}px)`,
                    top: `calc(50% + ${y}px)`,
                  }}
                  initial={{ opacity: 0, scale: 0 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <motion.div
                    className={`w-16 h-16 bg-gradient-to-br ${tech.color} rounded-full flex items-center justify-center shadow-lg cursor-pointer`}
                    whileHover={{ scale: 1.2, rotate: 360 }}
                    transition={{ type: 'spring', stiffness: 300 }}
                  >
                    <tech.icon className="text-2xl text-white" />
                  </motion.div>
                  <p className="text-xs text-gray-400 text-center mt-2 whitespace-nowrap">
                    {tech.name}
                  </p>

                  {/* Connection Line */}
                  <svg
                    className="absolute top-1/2 left-1/2 -z-10"
                    style={{
                      width: Math.abs(x) * 2,
                      height: Math.abs(y) * 2,
                    }}
                  >
                    <motion.line
                      x1={x > 0 ? 0 : Math.abs(x) * 2}
                      y1={y > 0 ? 0 : Math.abs(y) * 2}
                      x2={x > 0 ? Math.abs(x) * 2 : 0}
                      y2={y > 0 ? Math.abs(y) * 2 : 0}
                      stroke="rgba(59, 130, 246, 0.3)"
                      strokeWidth="2"
                      initial={{ pathLength: 0 }}
                      whileInView={{ pathLength: 1 }}
                      viewport={{ once: true }}
                      transition={{ duration: 1, delay: index * 0.1 }}
                    />
                  </svg>
                </motion.div>
              )
            })}
          </motion.div>
        </div>

        {/* Performance Metrics */}
        <motion.div
          className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-5xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          {metrics.map((metric, index) => (
            <motion.div
              key={metric.label}
              className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl text-center hover:bg-white/10 transition-all"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
              whileHover={{ y: -5, scale: 1.05 }}
            >
              <div className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
                {metric.value}
              </div>
              <div className="text-sm font-semibold text-white mb-1">
                {metric.label}
              </div>
              <div className="text-xs text-gray-400">
                {metric.description}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Data Flow Animation */}
        <motion.div
          className="mt-16 max-w-4xl mx-auto"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 1 }}
        >
          <div className="relative h-2 bg-slate-700 rounded-full overflow-hidden">
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-blue-500 via-cyan-500 to-blue-500"
              animate={{
                x: ['-100%', '100%'],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'linear',
              }}
            />
          </div>
          <div className="flex justify-between mt-4 text-sm text-gray-400">
            <span>Entrada de Dados</span>
            <span>Processamento IA</span>
            <span>Resultados</span>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

