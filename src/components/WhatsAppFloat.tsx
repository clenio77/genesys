'use client'

import { FaWhatsapp } from 'react-icons/fa'

export default function WhatsAppFloat() {
  const handleWhatsAppClick = () => {
    window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre os serviços da Genesys Tecnologia.', '_blank')
  }

  return (
    <button
      onClick={handleWhatsAppClick}
      className="whatsapp-float group"
      aria-label="Contato via WhatsApp"
    >
      <FaWhatsapp />
      
      {/* Tooltip */}
      <div className="absolute right-full mr-3 top-1/2 transform -translate-y-1/2 bg-green-600 text-white text-sm px-3 py-2 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap pointer-events-none">
        Fale conosco no WhatsApp
        <div className="absolute left-full top-1/2 transform -translate-y-1/2 w-0 h-0 border-l-4 border-l-green-600 border-t-4 border-t-transparent border-b-4 border-b-transparent"></div>
      </div>
    </button>
  )
}
