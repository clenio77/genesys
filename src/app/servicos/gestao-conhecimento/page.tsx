'use client'

import Link from 'next/link'
import { FaDatabase, FaSearch, FaBrain, FaArrowRight, FaCheck } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'

export default function GestaoConhecimentoPage() {
  const capabilities = [
    'Base de conhecimento privada por cliente',
    'Busca semântica em documentos internos',
    'RAG com controle de citações e fontes',
    'Organização por área, cliente ou caso',
    'Guardrails contra fontes inventadas',
    'Exportação de relatórios fundamentados',
  ]

  return (
    <>
      <SEOHead
        title="Base de Conhecimento — Capacidade do Kermartin | Genesys"
        description="Pesquisa, bases privadas e gestão de conhecimento são capacidades nativas do Kermartin IA. A Genesys configura tudo na implantação."
        keywords="base de conhecimento kermartin, rag jurídico, busca semântica, gestão documental ia"
        canonical="https://genesys-tecnologia.com.br/servicos/gestao-conhecimento"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

        <section className="pt-32 pb-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-500/10 border border-indigo-500/30 rounded-full mb-6">
              <FaDatabase className="text-indigo-400" />
              <span className="text-indigo-300 text-sm font-medium">Capacidade do Kermartin</span>
            </div>

            <h1 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-indigo-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Base de Conhecimento e Pesquisa
            </h1>

            <p className="text-xl text-gray-300 mb-8 leading-relaxed">
              Gestão de conhecimento e pesquisa jurisprudencial não são serviços avulsos da Genesys —
              são módulos integrados ao <strong className="text-white">Kermartin IA</strong>.
              Configuramos bases privadas, conectores e fluxos de pesquisa durante a implantação.
            </p>

            <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700 text-left mb-10">
              <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <FaBrain className="text-purple-400" />
                O que o Kermartin oferece nativamente
              </h2>
              <div className="grid sm:grid-cols-2 gap-3">
                {capabilities.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-gray-300 text-sm">
                    <FaCheck className="text-green-400 mt-0.5 flex-shrink-0" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex flex-wrap justify-center gap-4">
              <Link
                href="/produtos/kermartin-ia"
                className="px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg font-semibold hover:shadow-xl transition-all hover:scale-105 inline-flex items-center gap-2"
              >
                Conhecer o Kermartin
                <FaArrowRight />
              </Link>
              <Link
                href="/servicos"
                className="px-8 py-4 bg-slate-800 text-white rounded-lg font-semibold border border-slate-700 hover:border-indigo-500/50 transition-all inline-flex items-center gap-2"
              >
                <FaSearch />
                Ver Implantação
              </Link>
            </div>
          </div>
        </section>

        <section className="py-16 px-4 bg-slate-900/50">
          <div className="max-w-3xl mx-auto text-center">
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-gray-400"
            >
              Precisa estruturar a base documental do escritório? Isso entra no escopo de{' '}
              <Link href="/servicos" className="text-cyan-400 hover:underline">Implantação do Kermartin</Link>
              {' '}— fale com nossa equipe para mapear fontes, permissões e fluxos de pesquisa.
            </motion.p>
          </div>
        </section>

        <Footer />
      </div>
    </>
  )
}
