'use client'

import { useState, useEffect } from 'react'
import { FaBars, FaTimes, FaSearch } from 'react-icons/fa'
import Image from 'next/image'

export default function PremiumHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const primaryMenuItems = [
    { label: 'Início', href: '/' },
    { label: 'Produtos', href: '/produtos' },
    { label: 'Serviços', href: '/servicos' },
    { label: 'Planos', href: '/pricing' },
    { label: 'Contato', href: '/#contact' },
  ]

  const secondaryMenuItems = [
    { label: 'Ferramentas', href: '/ferramentas' },
    { label: 'Integrações', href: '/integracoes' },
    { label: 'Área do Cliente', href: '/portal-cliente' },
    { label: 'Sobre', href: '/sobre' },
  ]

  const menuItems = [...primaryMenuItems, ...secondaryMenuItems]

  return (
    <header
      className="fixed top-0 left-0 right-0 z-50 transition-all duration-300 overflow-x-clip"
      style={{
        backdropFilter: `blur(${isScrolled ? '20px' : '10px'})`,
        backgroundColor: isScrolled
          ? 'rgba(15, 23, 42, 0.95)'
          : 'rgba(15, 23, 42, 0.8)',
      }}
    >
      {/* Gradient Border */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50" />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-full">
        <div className="flex items-center justify-between gap-2 sm:gap-3 xl:gap-4 min-h-[70px] sm:min-h-[85px] lg:min-h-[95px] py-2 sm:py-2.5 lg:py-3 w-full min-w-0">
          {/* Logo */}
          <div className="flex items-center h-full flex-shrink-0 min-w-0">
            <a href="/" className="flex items-center h-full">
              <div className="relative w-[160px] h-full sm:w-[200px] xl:w-[220px] 2xl:w-[280px] min-h-[55px] sm:min-h-[75px] lg:min-h-[85px] overflow-hidden">
                <Image
                  src="/images/genesys-logo.png"
                  alt="Genesys Tecnologia Jurídica"
                  fill
                  sizes="(max-width: 640px) 180px, (max-width: 768px) 220px, 280px"
                  className="object-contain hover:scale-105 transition-transform duration-300 logo-scale"
                  style={{
                    objectFit: 'contain',
                    objectPosition: 'left center',
                    transformOrigin: 'left center'
                  }}
                  priority
                />
              </div>
            </a>
          </div>

          {/* Compact nav: primary links only (xl–2xl) */}
          <nav className="hidden xl:flex 2xl:hidden items-center min-w-0 flex-1 justify-center gap-0.5 xl:gap-1 overflow-hidden">
            {primaryMenuItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="relative px-1.5 py-1 text-xs xl:text-sm font-medium text-gray-300 hover:text-white transition-colors group whitespace-nowrap shrink-0"
              >
                {item.label}
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-500 to-cyan-500 group-hover:w-full transition-all duration-300" />
              </a>
            ))}
          </nav>

          {/* Full desktop nav (2xl+) */}
          <nav className="hidden 2xl:flex items-center min-w-0 flex-1 justify-center gap-1 2xl:gap-4 overflow-hidden">
            {menuItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="relative px-2 py-1 text-sm font-medium text-gray-300 hover:text-white transition-colors group whitespace-nowrap shrink-0"
              >
                {item.label}
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-500 to-cyan-500 group-hover:w-full transition-all duration-300" />
              </a>
            ))}
          </nav>

          {/* CTA Buttons */}
          <div className="hidden xl:flex items-center gap-2 flex-shrink-0">
            <button className="p-2 text-gray-400 hover:text-white transition-colors hover:scale-110 flex-shrink-0" aria-label="Buscar">
              <FaSearch />
            </button>

            <a
              href="/pricing"
              className="px-3 xl:px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg text-xs xl:text-sm font-medium hover:shadow-lg hover:shadow-blue-500/50 transition-all hover:scale-105 whitespace-nowrap inline-block flex-shrink-0"
            >
              Começar Agora
            </a>
          </div>

          {/* Mobile / compact menu button */}
          <button
            className="2xl:hidden p-2 text-white hover:scale-110 transition-transform relative z-10 flex-shrink-0"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile / compact menu */}
      <div className={`2xl:hidden overflow-hidden transition-all duration-300 relative z-20 ${isMenuOpen ? 'max-h-[600px] opacity-100' : 'max-h-0 opacity-0'}`}>
        <div className="px-4 py-6 space-y-4 bg-slate-900/95 backdrop-blur-xl border-t border-slate-800 overflow-y-auto max-h-[calc(100vh-100px)]">
          {menuItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="block text-gray-300 hover:text-white transition-colors py-2"
              onClick={() => setIsMenuOpen(false)}
            >
              {item.label}
            </a>
          ))}

          <a
            href="/pricing"
            className="block w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-medium hover:scale-105 transition-transform text-center"
          >
            Começar Agora
          </a>
        </div>
      </div>
    </header>
  )
}