'use client'

import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { FaChartLine, FaSearch, FaFileContract, FaRobot, FaArrowRight, FaChevronLeft, FaChevronRight } from 'react-icons/fa'
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
    subtitle: 'Assistente Jurídico Inteligente',
    description: 'Seu assistente jurídico pessoal 24/7. Análise instantânea de documentos, respostas precisas e insights estratégicos com IA de última geração.',
    logo: '/images/kermartin-logo.png',
    gradient: 'from-blue-600 via-cyan-600 to-blue-500',
    stats: [
      { label: 'Precisão', value: '95%' },
      { label: 'Disponibilidade', value: '24/7' },
      { label: 'Respostas', value: '<3s' },
    ],
    cta: 'Conhecer Kermartin',
    ctaLink: '/produtos/kermartin-ia',
    bgPattern: 'radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.15) 0%, transparent 50%)',
  },
  {
    id: 2,
    title: 'Analytics Jurídico',
    subtitle: 'Inteligência de Dados',
    description: 'Transforme dados jurídicos em decisões estratégicas. Dashboards interativos, métricas em tempo real e previsões baseadas em IA.',
    icon: FaChartLine,
    gradient: 'from-purple-600 via-pink-600 to-purple-500',
    stats: [
      { label: 'Métricas', value: '50+' },
      { label: 'Tempo Real', value: '100%' },
      { label: 'Insights', value: 'IA' },
    ],
    cta: 'Ver Analytics',
    ctaLink: '/tecnologias/analytics-juridico',
    bgPattern: 'radial-gradient(circle at 80% 50%, rgba(168, 85, 247, 0.15) 0%, transparent 50%)',
  },
  {
    id: 3,
    title: 'Pesquisa Jurisprudencial',
    subtitle: 'Busca Inteligente',
    description: 'Encontre jurisprudências relevantes em segundos. Busca semântica avançada em mais de 90 milhões de decisões judiciais.',
    icon: FaSearch,
    gradient: 'from-emerald-600 via-teal-600 to-emerald-500',
    stats: [
      { label: 'Decisões', value: '90M+' },
      { label: 'Tribunais', value: 'Todos' },
      { label: 'Busca', value: 'IA' },
    ],
    cta: 'Explorar Pesquisa',
    ctaLink: '/produtos/pesquisa-juridica',
    bgPattern: 'radial-gradient(circle at 50% 20%, rgba(16, 185, 129, 0.15) 0%, transparent 50%)',
  },
  {
    id: 4,
    title: 'Análise de Contratos',
    subtitle: 'Revisão Automatizada',
    description: 'Análise completa de contratos em minutos. Identificação de riscos, cláusulas críticas e sugestões de melhorias com IA.',
    icon: FaFileContract,
    gradient: 'from-amber-600 via-orange-600 to-amber-500',
    stats: [
      { label: 'Velocidade', value: '90%+' },
      { label: 'Precisão', value: '98%' },
      { label: 'Economia', value: '10x' },
    ],
    cta: 'Ver Análise',
    ctaLink: '/produtos/analise-contratos',
    bgPattern: 'radial-gradient(circle at 50% 80%, rgba(245, 158, 11, 0.15) 0%, transparent 50%)',
  },
  {
    id: 5,
    title: 'Automação Processual',
    subtitle: 'Workflow Inteligente',
    description: 'Automatize tarefas repetitivas e ganhe produtividade. Gestão de prazos, petições automáticas e acompanhamento processual.',
    icon: FaRobot,
    gradient: 'from-rose-600 via-red-600 to-rose-500',
    stats: [
      { label: 'Produtividade', value: '+300%' },
      { label: 'Automação', value: '100%' },
      { label: 'Erros', value: '-95%' },
    ],
    cta: 'Automatizar Agora',
    ctaLink: '/produtos/automacao-processos',
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
      className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950"
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
          className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-3xl"
          style={{ background: currentProduct.gradient }}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.3, 0.2],
          }}
          transition={{ duration: 4, repeat: Infinity }}
        />
        <motion.div
          className="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-3xl"
          style={{ background: currentProduct.gradient }}
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.3, 0.2, 0.3],
          }}
          transition={{ duration: 4, repeat: Infinity, delay: 2 }}
        />
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
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
              className="grid lg:grid-cols-2 gap-12 items-center"
            >
              {/* Left Column - Content */}
              <div className="space-y-8">
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
                    className="text-cyan-400 text-sm font-semibold mb-2 tracking-wider uppercase"
                  >
                    {currentProduct.subtitle}
                  </motion.p>
                  <motion.h2
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className={`text-5xl md:text-6xl font-bold bg-gradient-to-r ${currentProduct.gradient} bg-clip-text text-transparent mb-4`}
                  >
                    {currentProduct.title}
                  </motion.h2>
                  <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="text-xl text-gray-300 leading-relaxed"
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
                <div className="relative p-8 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl">
                  {/* Background Pattern */}
                  <div className="absolute inset-0 rounded-3xl opacity-30" style={{ background: currentProduct.bgPattern }} />

                  {/* Stats Grid */}
                  <div className="relative grid grid-cols-3 gap-6">
                    {currentProduct.stats.map((stat, index) => (
                      <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.8 + index * 0.1 }}
                        className="text-center p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 hover:bg-white/10 transition-all"
                      >
                        <div className={`text-4xl font-bold bg-gradient-to-r ${currentProduct.gradient} bg-clip-text text-transparent mb-2 leading-tight py-1`}>
                          {stat.value}
                        </div>
                        <div className="text-sm text-gray-400 font-medium">
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
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-3 z-20">
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
            <div className={`w-12 h-2 rounded-full transition-all ${
              index === currentIndex
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
