'use client'

import Link from 'next/link'
import { FaInfoCircle, FaArrowRight } from 'react-icons/fa'

interface LegacyProdutoBannerProps {
  titulo: string
  descricao: string
  linkServico: string
  labelServico: string
}

export default function LegacyProdutoBanner({
  titulo,
  descricao,
  linkServico,
  labelServico,
}: LegacyProdutoBannerProps) {
  return (
    <div className="bg-gradient-to-r from-indigo-900/40 to-blue-900/40 border-b border-indigo-500/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="flex items-start gap-3">
            <FaInfoCircle className="text-indigo-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm font-semibold text-indigo-200">{titulo}</p>
              <p className="text-sm text-gray-400">{descricao}</p>
            </div>
          </div>
          <Link
            href={linkServico}
            className="inline-flex items-center gap-2 text-sm font-semibold text-cyan-400 hover:text-cyan-300 transition-colors whitespace-nowrap"
          >
            {labelServico}
            <FaArrowRight className="text-xs" />
          </Link>
        </div>
      </div>
    </div>
  )
}
