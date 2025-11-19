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

  const menuItems = [
    { label: 'Início', href: '/' },
    { label: 'Produtos', href: '/produtos' },
    { label: 'Serviços', href: '/servicos' },
    { label: 'Sobre', href: '/sobre' },
    { label: 'Contato', href: '#contact' },
  ]

  return (
    <header
      className="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
      style={{
        backdropFilter: `blur(${isScrolled ? '20px' : '10px'})`,
        backgroundColor: isScrolled 
          ? 'rgba(15, 23, 42, 0.95)' 
          : 'rgba(15, 23, 42, 0.8)',
      }}
    >
      {/* Gradient Border */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50" />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between min-h-24 sm:h-20 py-3 sm:py-0">
          {/* Logo */}
          <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-3">
            {/* Mobile: Logo maior e mais larga, sem texto */}
            {/* Desktop: Logo maior, quase na altura do header */}
            <div className="relative w-48 h-32 sm:w-44 sm:h-28 md:w-52 md:h-30 lg:w-60 lg:h-32">
              <Image
                src="/images/genesys-logo.png"
                alt="Genesys Tecnologia Jurídica"
                fill
                className="object-contain"
                priority
              />
            </div>
            {/* Texto visível apenas em telas médias e grandes */}
            <div className="hidden sm:block text-left">
              <h1 className="text-xl sm:text-2xl md:text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                Genesys
              </h1>
              <p className="text-xs sm:text-sm text-gray-300">Tecnologia Jurídica</p>
            </div>
          </div>

          {/* Desktop Menu */}
          <nav className="hidden md:flex items-center space-x-8">
            {menuItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="relative text-gray-300 hover:text-white transition-colors group"
              >
                {item.label}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-500 to-cyan-500 group-hover:w-full transition-all duration-300" />
              </a>
            ))}
          </nav>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <button className="p-2 text-gray-400 hover:text-white transition-colors hover:scale-110">
              <FaSearch />
            </button>
            
            <button className="px-6 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-medium hover:shadow-lg hover:shadow-blue-500/50 transition-all hover:scale-105">
              Começar Agora
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 text-white hover:scale-110 transition-transform"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <div className={`md:hidden overflow-hidden transition-all duration-300 ${isMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}`}>
        <div className="px-4 py-6 space-y-4 bg-slate-900/95 backdrop-blur-xl border-t border-slate-800">
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
          
          <button className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-medium hover:scale-105 transition-transform">
            Começar Agora
          </button>
        </div>
      </div>
    </header>
  )
}