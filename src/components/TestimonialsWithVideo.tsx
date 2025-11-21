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
      nome: 'Dr. Eduardo Martins',
      cargo: 'Advogado Tributarista',
      empresa: 'Martins & Advogados Associados',
      foto: '/images/avatar-fernando.webp',
      rating: 5,
      texto: 'A Genesys revolucionou nossa forma de trabalhar. Com a IA jurídica, conseguimos analisar processos tributários complexos em minutos. Nossa produtividade aumentou 300% e a precisão nas análises melhorou significativamente.',
      videoUrl: '/videos/depoimento-advogado.mp4',
      videoThumbnail: '/images/avatar-fernando.webp',
      tipo: 'video'
    },
    {
      id: 4,
      nome: 'Dra. Beatriz',
      cargo: 'Advogada Empresarial',
      empresa: 'Silva & Advogados',
      foto: '/images/depoimento1-thumb.webp',
      rating: 5,
      texto: 'A Genesys transformou completamente nossa forma de trabalhar. A inteligência artificial nos ajuda a analisar contratos complexos em minutos, identificando cláusulas críticas e riscos que antes levávamos horas para encontrar. Nossa produtividade aumentou significativamente!',
      videoUrl: '/videos/depoimento1.mp4',
      videoThumbnail: '/images/depoimento1-thumb.webp',
      tipo: 'video'
    },
    {
      id: 2,
      nome: 'Dra. Ana Paula Oliveira',
      cargo: 'Diretora Jurídica',
      empresa: 'TechCorp Brasil',
      foto: '/images/avatar-ana.webp',
      rating: 5,
      texto: 'A consultoria em IA da Genesys foi fundamental para nossa transformação digital. A equipe é extremamente competente e o suporte é excepcional. Reduzimos 70% do tempo em análise de contratos.',
      videoUrl: '/videos/depoimento-ana.mp4',
      videoThumbnail: '/images/avatar-ana.webp',
      tipo: 'video'
    },
    {
      id: 3,
      nome: 'Dr. Roberto Mendes',
      cargo: 'Sócio-Fundador',
      empresa: 'Mendes & Associados',
      foto: '/images/avatar-roberto.webp',
      rating: 5,
      texto: 'Os serviços da Genesys transformaram completamente nossa operação. A pesquisa jurídica inteligente nos permite encontrar precedentes relevantes em segundos, a análise automatizada de contratos identifica riscos que antes passavam despercebidos, e o sistema de compliance garante que estamos sempre em conformidade com a LGPD. O ROI foi alcançado em apenas 4 meses e nossa equipe agora pode focar em atividades estratégicas ao invés de tarefas repetitivas. Recomendo fortemente!',
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
              <div className="relative h-full min-h-[300px] md:min-h-[400px] flex items-center justify-center bg-slate-900/50 rounded-2xl overflow-hidden">
                {currentTestimonial.tipo === 'video' && currentTestimonial.videoUrl ? (
                  <div className="relative w-full h-full flex items-center justify-center">
                    {playingVideo === currentTestimonial.id ? (
                      // Detecta se é vídeo local (MP4, WebM, MOV) ou embed (YouTube, Vimeo)
                      currentTestimonial.videoUrl.match(/\.(mp4|webm|mov)$/i) ? (
                        <video
                          src={currentTestimonial.videoUrl}
                          className="w-full h-full max-h-[500px] object-contain"
                          controls
                          autoPlay
                          preload="metadata"
                        >
                          Seu navegador não suporta vídeo HTML5.
                        </video>
                      ) : (
                        <iframe
                          src={currentTestimonial.videoUrl}
                          className="w-full h-full aspect-video"
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                          allowFullScreen
                        />
                      )
                    ) : (
                      <div
                        className="relative w-full h-full min-h-[300px] cursor-pointer group flex items-center justify-center"
                        onClick={() => setPlayingVideo(currentTestimonial.id)}
                      >
                        <Image
                          src={currentTestimonial.videoThumbnail || currentTestimonial.foto}
                          alt={currentTestimonial.nome}
                          fill
                          className="object-contain"
                        />
                        <div className="absolute inset-0 bg-black/40 group-hover:bg-black/30 transition-all flex items-center justify-center">
                          <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform shadow-2xl z-10">
                            <FaPlay className="text-white text-2xl ml-1" />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="relative w-full aspect-square rounded-2xl overflow-hidden">
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
                  className={`w-3 h-3 rounded-full transition-all ${index === currentIndex
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

