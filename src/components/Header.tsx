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
          <div className="flex justify-between items-center h-20 md:h-24">
            <div className="flex items-center h-full py-2">
              <Link href="#home" className="flex items-center h-full">
                <div className="relative w-[180px] h-[40px] sm:w-[220px] sm:h-[50px] md:w-[260px] md:h-[60px] transition-all duration-300">
                  <Image
                    src="/images/genesys-logo.png"
                    alt="Genesys Tecnologia - Inteligência Artificial Jurídica"
                    fill
                    sizes="(max-width: 640px) 180px, (max-width: 768px) 220px, 260px"
                    className="object-contain hover:scale-105 transition-transform duration-300"
                    style={{
                      objectFit: 'contain',
                      objectPosition: 'left center'
                    }}
                    priority
                  />
                </div>
              </Link>
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
      <div className={`fixed inset-0 z-30 bg-genesys-dark/95 backdrop-blur-md transition-all duration-300 ${isMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible'
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
      <div className="header-spacer"></div>
    </>
  )
}
