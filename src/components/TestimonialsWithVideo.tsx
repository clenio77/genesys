'use client'

import { useState } from 'react'
import { FaPlay, FaQuoteLeft, FaStar, FaChevronLeft, FaChevronRight } from 'react-icons/fa'
import Image from 'next/image'

interface Testimonial {
  id: number
  nome: string
  cargo: string
  empresa: string
  foto: string
  rating: number
  texto: string
  videoUrl?: string
  videoThumbnail?: string
  tipo: 'texto' | 'video'
}

export default function TestimonialsWithVideo() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [playingVideo, setPlayingVideo] = useState<number | null>(null)

  const depoimentos: Testimonial[] = [
    {
      id: 1,
      nome: 'Dr. Carlos Silva',
      cargo: 'Sócio Fundador',
      empresa: 'Silva & Associados',
      foto: '/images/clenio.png',
      rating: 5,
      texto: 'A Genesys transformou completamente nossa prática jurídica. Com o Kermartin IA, reduzimos em 70% o tempo de análise de contratos e aumentamos nossa produtividade em 3x. O ROI foi alcançado em apenas 4 meses!',
      videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      videoThumbnail: '/images/clenio.png',
      tipo: 'video'
    },
    {
      id: 2,
      nome: 'Dra. Ana Paula Oliveira',
      cargo: 'Diretora Jurídica',
      empresa: 'TechCorp Brasil',
      foto: '/images/lilian1.png',
      rating: 5,
      texto: 'A consultoria em IA da Genesys foi fundamental para nossa transformação digital. A equipe é extremamente competente e o suporte é excepcional. Recomendo fortemente!',
      tipo: 'texto'
    },
    {
      id: 3,
      nome: 'Dr. Roberto Mendes',
      cargo: 'Advogado Especialista',
      empresa: 'Mendes Advocacia',
      foto: '/images/firmino1.png',
      rating: 5,
      texto: 'O sistema de pesquisa jurídica com IA é simplesmente incrível. Encontro precedentes relevantes em minutos, algo que antes levava horas. A precisão é impressionante!',
      videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      videoThumbnail: '/images/firmino1.png',
      tipo: 'video'
    },
    {
      id: 4,
      nome: 'Dra. Mariana Costa',
      cargo: 'Coordenadora de Compliance',
      empresa: 'FinanceGroup',
      foto: '/images/lilian1.png',
      rating: 5,
      texto: 'O módulo de Compliance IA nos ajudou a alcançar 100% de conformidade com a LGPD. Os alertas em tempo real são essenciais para nossa operação. Excelente investimento!',
      tipo: 'texto'
    },
    {
      id: 5,
      nome: 'Dr. Fernando Alves',
      cargo: 'Sócio',
      empresa: 'Alves & Partners',
      foto: '/images/clenio.png',
      rating: 5,
      texto: 'A automação de processos liberou nossa equipe para focar em atividades estratégicas. Economizamos mais de 15 horas por semana em tarefas repetitivas. Simplesmente fantástico!',
      videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      videoThumbnail: '/images/clenio.png',
      tipo: 'video'
    },
    {
      id: 6,
      nome: 'Dra. Juliana Santos',
      cargo: 'Advogada Associada',
      empresa: 'Santos Advocacia',
      foto: '/images/lilian.png',
      rating: 5,
      texto: 'A interface é intuitiva e a curva de aprendizado é muito rápida. Em uma semana já estávamos usando todas as funcionalidades. O suporte técnico é sempre muito atencioso.',
      tipo: 'texto'
    }
  ]

  const nextTestimonial = () => {
    setCurrentIndex((prev) => (prev + 1) % depoimentos.length)
    setPlayingVideo(null)
  }

  const prevTestimonial = () => {
    setCurrentIndex((prev) => (prev - 1 + depoimentos.length) % depoimentos.length)
    setPlayingVideo(null)
  }

  const currentTestimonial = depoimentos[currentIndex]

  return (
    <section className="py-24 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
      {/* Background Decoration */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
          backgroundSize: '40px 40px',
        }} />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              O Que Nossos Clientes Dizem
            </span>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Histórias reais de transformação com nossas soluções de IA
          </p>
        </div>

        {/* Main Testimonial Card */}
        <div className="max-w-5xl mx-auto">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-3xl p-8 md:p-12 border border-slate-700 shadow-2xl">
            <div className="grid md:grid-cols-2 gap-8 items-center">
              {/* Left Side - Video or Image */}
              <div className="relative">
                {currentTestimonial.tipo === 'video' && currentTestimonial.videoUrl ? (
                  <div className="relative aspect-video rounded-2xl overflow-hidden bg-slate-900">
                    {playingVideo === currentTestimonial.id ? (
                      <iframe
                        src={currentTestimonial.videoUrl}
                        className="w-full h-full"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                      />
                    ) : (
                      <div 
                        className="relative w-full h-full cursor-pointer group"
                        onClick={() => setPlayingVideo(currentTestimonial.id)}
                      >
                        <Image
                          src={currentTestimonial.videoThumbnail || currentTestimonial.foto}
                          alt={currentTestimonial.nome}
                          fill
                          className="object-cover"
                        />
                        <div className="absolute inset-0 bg-black/40 group-hover:bg-black/30 transition-all flex items-center justify-center">
                          <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                            <FaPlay className="text-white text-2xl ml-1" />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="relative aspect-square rounded-2xl overflow-hidden">
                    <Image
                      src={currentTestimonial.foto}
                      alt={currentTestimonial.nome}
                      fill
                      className="object-cover"
                    />
                  </div>
                )}
              </div>

              {/* Right Side - Content */}
              <div>
                {/* Quote Icon */}
                <FaQuoteLeft className="text-4xl text-blue-400 mb-6 opacity-50" />

                {/* Rating */}
                <div className="flex gap-1 mb-4">
                  {[...Array(currentTestimonial.rating)].map((_, i) => (
                    <FaStar key={i} className="text-yellow-400 text-xl" />
                  ))}
                </div>

                {/* Testimonial Text */}
                <p className="text-lg text-gray-300 mb-6 leading-relaxed">
                  &ldquo;{currentTestimonial.texto}&rdquo;
                </p>

                {/* Author Info */}
                <div className="border-t border-slate-700 pt-6">
                  <h4 className="text-xl font-bold text-white mb-1">
                    {currentTestimonial.nome}
                  </h4>
                  <p className="text-cyan-400 font-medium mb-1">
                    {currentTestimonial.cargo}
                  </p>
                  <p className="text-gray-400 text-sm">
                    {currentTestimonial.empresa}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-center gap-4 mt-8">
            <button
              onClick={prevTestimonial}
              className="w-12 h-12 bg-slate-800 hover:bg-slate-700 rounded-full flex items-center justify-center text-white transition-all hover:scale-110"
              aria-label="Depoimento anterior"
            >
              <FaChevronLeft />
            </button>

            {/* Dots */}
            <div className="flex gap-2">
              {depoimentos.map((_, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setCurrentIndex(index)
                    setPlayingVideo(null)
                  }}
                  className={`w-3 h-3 rounded-full transition-all ${
                    index === currentIndex
                      ? 'bg-blue-500 w-8'
                      : 'bg-slate-600 hover:bg-slate-500'
                  }`}
                  aria-label={`Ir para depoimento ${index + 1}`}
                />
              ))}
            </div>

            <button
              onClick={nextTestimonial}
              className="w-12 h-12 bg-slate-800 hover:bg-slate-700 rounded-full flex items-center justify-center text-white transition-all hover:scale-110"
              aria-label="Próximo depoimento"
            >
              <FaChevronRight />
            </button>
          </div>

          {/* Counter */}
          <div className="text-center mt-4 text-gray-400 text-sm">
            {currentIndex + 1} / {depoimentos.length}
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto mt-16">
          <div className="text-center">
            <div className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
              500+
            </div>
            <div className="text-gray-400 text-sm">Clientes Satisfeitos</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
              99%
            </div>
            <div className="text-gray-400 text-sm">Satisfação</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
              4.9/5
            </div>
            <div className="text-gray-400 text-sm">Avaliação Média</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
              10x
            </div>
            <div className="text-gray-400 text-sm">ROI Médio</div>
          </div>
        </div>
      </div>
    </section>
  )
}

