'use client'

import { FaBalanceScale, FaShieldAlt, FaLock, FaBrain } from 'react-icons/fa'

export default function FloatingCertifications() {
  const certifications = [
    {
      icon: FaBalanceScale,
      tooltip: 'OAB Certificado',
      className: 'certification-oab'
    },
    {
      icon: FaShieldAlt,
      tooltip: 'LGPD Compliant',
      className: 'certification-lgpd'
    },
    {
      icon: FaLock,
      tooltip: 'ISO 27001',
      className: 'certification-iso'
    },
    {
      icon: FaBrain,
      tooltip: 'IA Certificada',
      className: 'certification-ia'
    }
  ]

  return (
    <div className="fixed top-1/2 right-5 transform -translate-y-1/2 z-50 flex flex-col gap-4">
      {certifications.map((cert, index) => (
        <div
          key={index}
          className={`certification-float ${cert.className} group`}
          data-tooltip={cert.tooltip}
        >
          <cert.icon className="text-white text-lg" />
          
          {/* Tooltip */}
          <div className="absolute right-full mr-3 top-1/2 transform -translate-y-1/2 bg-genesys-dark text-white text-sm px-3 py-2 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap pointer-events-none">
            {cert.tooltip}
            <div className="absolute left-full top-1/2 transform -translate-y-1/2 w-0 h-0 border-l-4 border-l-genesys-dark border-t-4 border-t-transparent border-b-4 border-b-transparent"></div>
          </div>
        </div>
      ))}
    </div>
  )
}
