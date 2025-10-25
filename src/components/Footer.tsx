'use client'

import Image from 'next/image'
import Link from 'next/link'
import { FaWhatsapp, FaLinkedin, FaTwitter, FaEnvelope, FaMapMarkerAlt, FaPhone } from 'react-icons/fa'

export default function Footer() {
  return (
    <footer className="bg-genesys-dark border-t border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-32 h-20 flex items-center justify-center genesys-logo logo-container relative">
                <Image
                  src="/images/genesys-logo.jpg"
                  alt="Genesys Tecnologia"
                  fill
                  sizes="(max-width: 768px) 50vw, 25vw"
                  className="object-contain hover:scale-105 transition-transform duration-300"
                  style={{ 
                    background: 'transparent', 
                    border: 'none'
                  }}
                />
              </div>
              <span className="text-2xl font-bold gradient-text hidden lg:block font-playfair">
                Genesys Tecnologia
              </span>
            </div>
            <p className="text-genesys-gray mb-6">
              Revolucionando a prática jurídica através da Inteligência Artificial.
              Transformamos dados jurídicos em insights poderosos.
            </p>
            
            {/* Social Links */}
            <div className="flex space-x-4">
              <a
                href="https://linkedin.com/company/genesys-tecnologia"
                className="w-10 h-10 bg-blue-600 hover:bg-blue-700 rounded-full flex items-center justify-center text-white transition-colors duration-300"
                aria-label="LinkedIn"
              >
                <FaLinkedin />
              </a>
              <a
                href="https://twitter.com/genesys_tech"
                className="w-10 h-10 bg-cyan-500 hover:bg-cyan-600 rounded-full flex items-center justify-center text-white transition-colors duration-300"
                aria-label="Twitter"
              >
                <FaTwitter />
              </a>
              <a
                href="mailto:contato@genesys-tecnologia.com.br"
                className="w-10 h-10 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center text-white transition-colors duration-300"
                aria-label="Email"
              >
                <FaEnvelope />
              </a>
            </div>
          </div>
          
          {/* Quick Links */}
          <div>
            <h3 className="text-xl font-semibold font-playfair mb-6 gradient-text">
              Links Rápidos
            </h3>
            <ul className="space-y-3">
              <li>
                <Link href="#home" className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300">
                  Início
                </Link>
              </li>
              <li>
                <Link href="#about" className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300">
                  Sobre Nós
                </Link>
              </li>
              <li>
                <Link href="#team" className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300">
                  Equipe
                </Link>
              </li>
              <li>
                <Link href="#products" className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300">
                  Produtos
                </Link>
              </li>
              <li>
                <Link href="#contact" className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300">
                  Contato
                </Link>
              </li>
            </ul>
          </div>
          
          {/* Services */}
          <div>
            <h3 className="text-xl font-semibold font-playfair mb-6 gradient-text">
              Serviços
            </h3>
            <ul className="space-y-3">
              <li className="text-genesys-gray">Kermartin IA</li>
              <li className="text-genesys-gray">Análise Jurídica</li>
              <li className="text-genesys-gray">Pesquisa Inteligente</li>
              <li className="text-genesys-gray">Compliance</li>
              <li className="text-genesys-gray">Consultoria IA</li>
            </ul>
          </div>
          
          {/* Contact Info */}
          <div>
            <h3 className="text-xl font-semibold font-playfair mb-6 gradient-text">
              Contato
            </h3>
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <FaMapMarkerAlt className="text-genesys-gold" />
                <span className="text-genesys-gray text-sm">
                  Brasil
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <FaPhone className="text-genesys-gold" />
                <span className="text-genesys-gray text-sm">
                  +55 34 99826-4603
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <FaEnvelope className="text-genesys-gold" />
                <span className="text-genesys-gray text-sm">
                  contato@genesys-tecnologia.com.br
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <FaWhatsapp className="text-genesys-gold" />
                <a
                  href="https://wa.me/5534998264603"
                  className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300 text-sm"
                >
                  WhatsApp
                </a>
              </div>
            </div>
          </div>
        </div>
        
        {/* Bottom Bar */}
        <div className="border-t border-white/10 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-genesys-gray text-sm mb-4 md:mb-0">
              © 2024 Genesys Tecnologia. Todos os direitos reservados.
            </div>
            <div className="flex space-x-6 text-sm">
              <Link href="/privacy" className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300">
                Política de Privacidade
              </Link>
              <Link href="/terms" className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300">
                Termos de Uso
              </Link>
              <Link href="/cookies" className="text-genesys-gray hover:text-genesys-gold transition-colors duration-300">
                Cookies
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
