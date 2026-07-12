'use client'

import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { FaChartLine, FaGavel, FaFileContract, FaRobot, FaArrowRight, FaChevronLeft, FaChevronRight } from 'react-icons/fa'
import Image from 'next/image'

interface Product {
  id: number
  title: string
  subtitle: string
  description: string
  icon?: React.ComponentType<{ className?: string }>
  logo?: string
  gradient: string
  stats: { label: string; value: string }[]
  cta: string
  ctaLink: string
  bgPattern: string
}

const products: Product[] = [
  {
    id: 1,
    title: 'Kermartin IA',
    subtitle: 'Plataforma de análise jurídica com IA',
    description: 'Motor jurídico BMAD para analisar documentos, processos e estratégias em blocos especializados: penal, civil, trânsito, tributário, auditoria pública e perfis estratégicos.',
    logo: '/images/kermartin-logo.png',
    gradient: 'from-blue-600 via-cyan-600 to-blue-500',
    stats: [
      { label: 'Blocos', value: '6+' },
      { label: 'Áreas', value: '5' },
      { label: 'Arquitetura', value: 'BMAD' },
    ],
    cta: 'Conhecer Kermartin',
    ctaLink: '/produtos/kermartin-ia',
    bgPattern: 'radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.15) 0%, transparent 50%)',
  },
  {
    id: 2,
    title: 'Implementação Assistida',
    subtitle: 'Serviço Genesys',
    description: 'Diagnóstico, parametrização, treinamento e implantação do Kermartin para escritórios, departamentos jurídicos e operações especializadas.',
    icon: FaRobot,
    gradient: 'from-purple-600 via-pink-600 to-purple-500',
    stats: [
      { label: 'Onboarding', value: 'Guiado' },
      { label: 'Treinamento', value: 'Equipe' },
      { label: 'Suporte', value: 'Contínuo' },
    ],
    cta: 'Ver Serviços',
    ctaLink: '/servicos',
    bgPattern: 'radial-gradient(circle at 80% 50%, rgba(168, 85, 247, 0.15) 0%, transparent 50%)',
  },
  {
    id: 3,
    title: 'Análise Penal e Júri',
    subtitle: 'Blocos estratégicos',
    description: 'Fluxos para inquérito, denúncia, prova, teses defensivas, debates em plenário e análise de perfis de acusação, defesa e testemunhas.',
    icon: FaGavel,
    gradient: 'from-emerald-600 via-teal-600 to-emerald-500',
    stats: [
      { label: 'Fluxo', value: 'Júri' },
      { label: 'Perfis', value: '3' },
      { label: 'Saída', value: 'Teses' },
    ],
    cta: 'Ver Kermartin',
    ctaLink: '/produtos/kermartin-ia',
    bgPattern: 'radial-gradient(circle at 50% 20%, rgba(16, 185, 129, 0.15) 0%, transparent 50%)',
  },
  {
    id: 4,
    title: 'Civil, Trânsito e Tributário',
    subtitle: 'Módulos jurídicos especializados',
    description: 'Análise civil com foco em prova e execução, defesa administrativa de trânsito e revisão de processos fiscais com regras anti-contaminação por área.',
    icon: FaFileContract,
    gradient: 'from-amber-600 via-orange-600 to-amber-500',
    stats: [
      { label: 'Civil', value: 'CPC' },
      { label: 'Trânsito', value: 'CTB' },
      { label: 'Tributário', value: 'CTN' },
    ],
    cta: 'Explorar Produto',
    ctaLink: '/produtos/kermartin-ia',
    bgPattern: 'radial-gradient(circle at 50% 80%, rgba(245, 158, 11, 0.15) 0%, transparent 50%)',
  },
  {
    id: 5,
    title: 'Auditoria Pública e Analytics',
    subtitle: 'Risco, licitações e evidências',
    description: 'Módulo para auditoria de licitações, detecção de irregularidades, análise de padrões e dashboards executivos para decisões baseadas em evidências.',
    icon: FaChartLine,
    gradient: 'from-rose-600 via-red-600 to-rose-500',
    stats: [
      { label: 'Risco', value: 'Score' },
      { label: 'Evidências', value: 'Mapa' },
      { label: 'Relatórios', value: 'BI' },
    ],
    cta: 'Ver Casos de Uso',
    ctaLink: '/produtos/kermartin-ia',
    bgPattern: 'radial-gradient(circle at 20% 80%, rgba(244, 63, 94, 0.15) 0%, transparent 50%)',
  },
]

export default function ProductCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [direction, setDirection] = useState(0)
  const [isPaused, setIsPaused] = useState(false)
  const [progress, setProgress] = useState(0)

  const slideVariants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 1000 : -1000,
      opacity: 0,
      scale: 0.8,
    }),
    center: {
      zIndex: 1,
      x: 0,
      opacity: 1,
      scale: 1,
    },
    exit: (direction: number) => ({
      zIndex: 0,
      x: direction < 0 ? 1000 : -1000,
      opacity: 0,
      scale: 0.8,
    }),
  }

  const swipeConfidenceThreshold = 10000
  const swipePower = (offset: number, velocity: number) => {
    return Math.abs(offset) * velocity
  }

  const paginate = useCallback((newDirection: number) => {
    setDirection(newDirection)
    setCurrentIndex((prevIndex) => {
      let nextIndex = prevIndex + newDirection
      if (nextIndex < 0) nextIndex = products.length - 1
      if (nextIndex >= products.length) nextIndex = 0
      return nextIndex
    })
    setProgress(0)
  }, [])

  // Auto-play
  useEffect(() => {
    if (isPaused) return

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          paginate(1)
          return 0
        }
        return prev + 2
      })
    }, 100)

    return () => clearInterval(interval)
  }, [isPaused, paginate])

  const currentProduct = products[currentIndex]

  return (
    <section
      className="relative w-full min-h-[600px] pt-28 pb-12 md:pt-32 md:pb-20 flex items-center justify-center overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950"
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      {/* Animated Background */}
      <div className="absolute inset-0">
        {/* Grid Pattern */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute inset-0" style={{
            backgroundImage: `radial-gradient(circle at 2px 2px, rgba(59, 130, 246, 0.3) 1px, transparent 0)`,
            backgroundSize: '50px 50px',
          }} />
        </div>

        {/* Gradient Orbs */}
        <motion.div
          className="absolute top-1/4 left-1/4 w-64 h-64 md:w-96 md:h-96 rounded-full blur-3xl"
          style={{ background: currentProduct.gradient }}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.3, 0.2],
          }}
          transition={{ duration: 4, repeat: Infinity }}
        />
        <motion.div
          className="absolute bottom-1/4 right-1/4 w-64 h-64 md:w-96 md:h-96 rounded-full blur-3xl"
          style={{ background: currentProduct.gradient }}
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.3, 0.2, 0.3],
          }}
          transition={{ duration: 4, repeat: Infinity, delay: 2 }}
        />
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
        <div className="max-w-7xl mx-auto">
          <AnimatePresence initial={false} custom={direction} mode="wait">
            <motion.div
              key={currentIndex}
              custom={direction}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{
                x: { type: "spring", stiffness: 300, damping: 30 },
                opacity: { duration: 0.2 },
                scale: { duration: 0.4 },
              }}
              drag="x"
              dragConstraints={{ left: 0, right: 0 }}
              dragElastic={1}
              onDragEnd={(_e, { offset, velocity }) => {
                const swipe = swipePower(offset.x, velocity.x)
                if (swipe < -swipeConfidenceThreshold) {
                  paginate(1)
                } else if (swipe > swipeConfidenceThreshold) {
                  paginate(-1)
                }
              }}
              className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center w-full"
            >
              {/* Left Column - Content */}
              <div className="space-y-6 sm:space-y-8">
                {/* Icon or Logo */}
                <motion.div
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
                  className={`inline-flex p-6 rounded-2xl bg-gradient-to-r ${currentProduct.gradient} shadow-2xl`}
                >
                  {currentProduct.logo ? (
                    <Image
                      src={currentProduct.logo}
                      alt={currentProduct.title}
                      width={80}
                      height={80}
                      className="object-contain"
                    />
                  ) : currentProduct.icon ? (
                    <currentProduct.icon className="text-5xl text-white" />
                  ) : null}
                </motion.div>

                {/* Title */}
                <div>
                  <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="text-cyan-400 text-xs sm:text-sm font-semibold mb-2 tracking-wider uppercase"
                  >
                    {currentProduct.subtitle}
                  </motion.p>
                  <motion.h2
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className={`text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold bg-gradient-to-r ${currentProduct.gradient} bg-clip-text text-transparent mb-4 break-words`}
                  >
                    {currentProduct.title}
                  </motion.h2>
                  <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="text-sm sm:text-base lg:text-lg xl:text-xl text-gray-300 leading-relaxed max-w-xl"
                  >
                    {currentProduct.description}
                  </motion.p>
                </div>

                {/* CTA Button */}
                <motion.a
                  href={currentProduct.ctaLink}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  className={`inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r ${currentProduct.gradient} text-white rounded-xl font-semibold text-lg shadow-2xl hover:shadow-3xl transition-all group`}
                >
                  {currentProduct.cta}
                  <FaArrowRight className="group-hover:translate-x-1 transition-transform" />
                </motion.a>
              </div>

              {/* Right Column - Stats */}
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.7 }}
                className="relative"
              >
                <div className="relative p-6 sm:p-8 md:p-10 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl">
                  {/* Background Pattern */}
                  <div className="absolute inset-0 rounded-3xl opacity-30" style={{ background: currentProduct.bgPattern }} />

                  {/* Stats Grid */}
                  <div className="relative grid grid-cols-3 gap-2 sm:gap-4 md:gap-6">
                    {currentProduct.stats.map((stat, index) => (
                      <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.8 + index * 0.1 }}
                        className="text-center p-2 sm:p-3 md:p-4 bg-white/5 backdrop-blur-sm rounded-xl md:rounded-2xl border border-white/10 hover:bg-white/10 transition-all flex flex-col justify-center items-center h-full"
                      >
                        <div className={`text-lg sm:text-xl lg:text-2xl xl:text-3xl font-bold bg-gradient-to-r ${currentProduct.gradient} bg-clip-text text-transparent mb-1 sm:mb-2 leading-tight`}>
                          {stat.value}
                        </div>
                        <div className="text-[10px] sm:text-xs text-gray-400 font-medium break-words leading-tight w-full">
                          {stat.label}
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* Navigation Arrows */}
      <button
        onClick={() => paginate(-1)}
        className="absolute left-4 top-1/2 -translate-y-1/2 p-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full text-white hover:bg-white/20 transition-all z-20 group"
        aria-label="Produto anterior"
      >
        <FaChevronLeft className="text-2xl group-hover:-translate-x-1 transition-transform" />
      </button>
      <button
        onClick={() => paginate(1)}
        className="absolute right-4 top-1/2 -translate-y-1/2 p-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full text-white hover:bg-white/20 transition-all z-20 group"
        aria-label="Próximo produto"
      >
        <FaChevronRight className="text-2xl group-hover:translate-x-1 transition-transform" />
      </button>

      {/* Dots Indicator */}
      <div className="absolute bottom-6 sm:bottom-8 left-1/2 -translate-x-1/2 flex gap-2 sm:gap-3 z-20">
        {products.map((_, index) => (
          <button
            key={index}
            onClick={() => {
              setDirection(index > currentIndex ? 1 : -1)
              setCurrentIndex(index)
              setProgress(0)
            }}
            className="group relative"
            aria-label={`Ir para produto ${index + 1}`}
          >
            <div className={`w-8 sm:w-10 md:w-12 h-1.5 sm:h-2 rounded-full transition-all ${index === currentIndex
              ? 'bg-white'
              : 'bg-white/30 hover:bg-white/50'
              }`}>
              {index === currentIndex && (
                <motion.div
                  className={`h-full rounded-full bg-gradient-to-r ${currentProduct.gradient}`}
                  initial={{ width: '0%' }}
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 0.1 }}
                />
              )}
            </div>
          </button>
        ))}
      </div>
    </section>
  )
}
