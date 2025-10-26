'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'
import { FaQuoteLeft, FaStar, FaChevronLeft, FaChevronRight } from 'react-icons/fa'
import Image from 'next/image'

export default function TestimonialsSection() {
  const [currentIndex, setCurrentIndex] = useState(0)

  const testimonials = [
    {
      name: 'Dr. Carlos Silva',
      role: 'Sócio - Silva & Associados',
      company: 'Escritório de Advocacia',
      image: '/images/clenio.png',
      rating: 5,
      text: 'A Genesys revolucionou nossa forma de trabalhar. A análise de contratos que levava dias agora é feita em minutos com precisão impressionante.',
    },
    {
      name: 'Dra. Ana Paula Costa',
      role: 'Diretora Jurídica',
      company: 'TechCorp Brasil',
      image: '/images/lilian1.png',
      rating: 5,
      text: 'Implementamos a solução de IA da Genesys e os resultados foram além das expectativas. Reduzimos custos em 60% e aumentamos a produtividade significativamente.',
    },
    {
      name: 'Dr. Roberto Firmino',
      role: 'Advogado Especialista',
      company: 'Firmino Advocacia',
      image: '/images/firmino.png',
      rating: 5,
      text: 'A pesquisa jurisprudencial com IA é simplesmente fantástica. Encontro precedentes relevantes em segundos e as predições são surpreendentemente precisas.',
    },
  ]

  const nextTestimonial = () => {
    setCurrentIndex((prev) => (prev + 1) % testimonials.length)
  }

  const prevTestimonial = () => {
    setCurrentIndex((prev) => (prev - 1 + testimonials.length) % testimonials.length)
  }

  const currentTestimonial = testimonials[currentIndex]

  return (
    <section className="py-24 bg-gradient-to-b from-slate-800 to-slate-900 relative overflow-hidden">
      {/* Background Decoration */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
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
            Depoimentos
          </span>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            O que nossos
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent"> Clientes Dizem</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Histórias reais de transformação digital no setor jurídico
          </p>
        </motion.div>

        {/* Testimonial Carousel */}
        <div className="max-w-4xl mx-auto">
          <div className="relative">
            {/* Navigation Buttons */}
            <div className="absolute top-1/2 -translate-y-1/2 left-0 right-0 flex justify-between pointer-events-none z-10">
              <motion.button
                className="p-3 bg-slate-800/80 backdrop-blur-sm border border-slate-700 rounded-full text-white hover:bg-slate-700 transition-all pointer-events-auto"
                onClick={prevTestimonial}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <FaChevronLeft />
              </motion.button>
              
              <motion.button
                className="p-3 bg-slate-800/80 backdrop-blur-sm border border-slate-700 rounded-full text-white hover:bg-slate-700 transition-all pointer-events-auto"
                onClick={nextTestimonial}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <FaChevronRight />
              </motion.button>
            </div>

            {/* Testimonial Card */}
            <AnimatePresence mode="wait">
              <motion.div
                key={currentIndex}
                className="p-8 md:p-12 bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl"
                initial={{ opacity: 0, x: 100 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -100 }}
                transition={{ duration: 0.5 }}
              >
                {/* Quote Icon */}
                <motion.div
                  className="mb-6"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
                >
                  <FaQuoteLeft className="text-5xl text-blue-500/30" />
                </motion.div>

                {/* Rating */}
                <motion.div
                  className="flex space-x-1 mb-6"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  {[...Array(currentTestimonial.rating)].map((_, i) => (
                    <motion.div
                      key={i}
                      initial={{ scale: 0, rotate: -180 }}
                      animate={{ scale: 1, rotate: 0 }}
                      transition={{ delay: 0.4 + i * 0.1, type: 'spring' }}
                    >
                      <FaStar className="text-2xl text-amber-400" />
                    </motion.div>
                  ))}
                </motion.div>

                {/* Testimonial Text */}
                <motion.p
                  className="text-xl text-gray-300 mb-8 leading-relaxed"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                >
                  &ldquo;{currentTestimonial.text}&rdquo;
                </motion.p>

                {/* Author Info */}
                <motion.div
                  className="flex items-center space-x-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                >
                  <div className="relative w-16 h-16 rounded-full overflow-hidden border-2 border-blue-500">
                    <Image
                      src={currentTestimonial.image}
                      alt={currentTestimonial.name}
                      fill
                      className="object-cover"
                    />
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-white">
                      {currentTestimonial.name}
                    </h4>
                    <p className="text-sm text-gray-400">
                      {currentTestimonial.role}
                    </p>
                    <p className="text-sm text-blue-400">
                      {currentTestimonial.company}
                    </p>
                  </div>
                </motion.div>
              </motion.div>
            </AnimatePresence>

            {/* Dots Indicator */}
            <div className="flex justify-center space-x-2 mt-8">
              {testimonials.map((_, index) => (
                <motion.button
                  key={index}
                  className={`w-3 h-3 rounded-full transition-all ${
                    index === currentIndex
                      ? 'bg-blue-500 w-8'
                      : 'bg-slate-600 hover:bg-slate-500'
                  }`}
                  onClick={() => setCurrentIndex(index)}
                  whileHover={{ scale: 1.2 }}
                  whileTap={{ scale: 0.9 }}
                />
              ))}
            </div>
          </div>

          {/* Stats */}
          <motion.div
            className="grid grid-cols-3 gap-6 mt-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            {[
              { value: '500+', label: 'Clientes Satisfeitos' },
              { value: '4.9/5', label: 'Avaliação Média' },
              { value: '98%', label: 'Taxa de Retenção' },
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                className="text-center p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/30 rounded-xl"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
                whileHover={{ y: -5, scale: 1.05 }}
              >
                <div className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}

