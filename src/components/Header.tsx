'use client'

import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { FaBars, FaTimes } from 'react-icons/fa'

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  return (
    <>
      <nav className="header-glass-modern" style={{ top: '0px' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="genesys-logo logo-container relative w-40 h-24 sm:w-36 sm:h-20 md:w-44 md:h-22 lg:w-52 lg:h-24">
                <Image
                  src="/images/genesys-logo.png"
                  alt="Genesys Tecnologia"
                  fill
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                  className="object-contain hover:scale-105 transition-transform duration-300"
                  style={{
                    background: 'transparent !important',
                    border: 'none !important',
                    outline: 'none !important',
                    boxShadow: 'none !important',
                    objectPosition: 'center !important'
                  }}
                  priority
                />
              </div>
              <span className="text-2xl font-bold gradient-text hidden lg:block font-playfair">
                Genesys Tecnologia
              </span>
            </div>
            
            {/* Desktop Navigation */}
            <div className="nav-links hidden md:flex space-x-8">
              <Link href="#home" className="nav-link text-lg">
                Início
              </Link>
              <Link href="#about" className="nav-link text-lg">
                Sobre
              </Link>
              <Link href="#team" className="nav-link text-lg">
                Equipe
              </Link>
              <Link href="#solutions" className="nav-link text-lg">
                Soluções
              </Link>
              <Link href="#products" className="nav-link text-lg">
                Produtos
              </Link>
              <Link href="#contact" className="nav-link text-lg">
                Contato
              </Link>
            </div>
            
            {/* Mobile Menu Button */}
            <button
              onClick={toggleMenu}
              className="mobile-menu-button md:hidden text-white text-2xl z-50"
              aria-label="Toggle menu"
            >
              {isMenuOpen ? <FaTimes /> : <FaBars />}
            </button>
          </div>
        </div>
      </nav>
      
      {/* Mobile Menu */}
      <div className={`fixed inset-0 z-30 bg-genesys-dark/95 backdrop-blur-md transition-all duration-300 ${
        isMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible'
      }`}>
        <div className="flex flex-col items-center justify-center h-full space-y-8">
          <Link 
            href="#home" 
            className="nav-link text-2xl font-playfair"
            onClick={() => setIsMenuOpen(false)}
          >
            Início
          </Link>
          <Link 
            href="#about" 
            className="nav-link text-2xl font-playfair"
            onClick={() => setIsMenuOpen(false)}
          >
            Sobre
          </Link>
          <Link 
            href="#team" 
            className="nav-link text-2xl font-playfair"
            onClick={() => setIsMenuOpen(false)}
          >
            Equipe
          </Link>
          <Link 
            href="#solutions" 
            className="nav-link text-2xl font-playfair"
            onClick={() => setIsMenuOpen(false)}
          >
            Soluções
          </Link>
          <Link 
            href="#products" 
            className="nav-link text-2xl font-playfair"
            onClick={() => setIsMenuOpen(false)}
          >
            Produtos
          </Link>
          <Link 
            href="#contact" 
            className="nav-link text-2xl font-playfair"
            onClick={() => setIsMenuOpen(false)}
          >
            Contato
          </Link>
        </div>
      </div>
      
      {/* Header Spacer */}
      <div className="header-spacer h-40"></div>
    </>
  )
}
