'use client'

import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { FaCalculator, FaFileAlt, FaCheckCircle, FaArrowRight } from 'react-icons/fa'

export default function FerramentasPage() {
    const tools = [
        {
            title: 'Calculadora de Prazos',
            description: 'Calcule prazos processuais em dias úteis ou corridos de forma rápida e precisa.',
            icon: FaCalculator,
            link: '/ferramentas/calculadora-prazos',
            gradient: 'from-blue-600 to-cyan-600',
            badge: 'Novo CPC'
        },
        {
            title: 'Gerador de Documentos',
            description: 'Crie procurações, declarações e recibos prontos para imprimir em segundos.',
            icon: FaFileAlt,
            link: '/ferramentas/gerador-documentos',
            gradient: 'from-purple-600 to-pink-600',
            badge: 'PDF Instantâneo'
        },
        {
            title: 'Validador de CNJ',
            description: 'Verifique a validade de numerações processuais e identifique o tribunal de origem.',
            icon: FaCheckCircle,
            link: '/ferramentas/validador-cnj',
            gradient: 'from-emerald-600 to-teal-600',
            badge: 'Algoritmo Oficial'
        }
    ]

    return (
        <>
            <SEOHead
                title="Ferramentas Jurídicas Gratuitas - Genesys Tecnologia"
                description="Acesse nossas ferramentas gratuitas para advogados: Calculadora de Prazos, Gerador de Documentos e Validador de Processos CNJ."
                keywords="calculadora prazos processuais, gerador procuração, validador cnj, ferramentas jurídicas grátis"
                canonical="https://genesys-tecnologia.com.br/ferramentas"
            />
            <div className="min-h-screen bg-slate-950 text-gray-300">
                <PremiumHeader />

                <main className="pt-32 pb-20 px-4">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center mb-16">
                            <h1 className="text-4xl md:text-5xl font-bold text-white mb-6">
                                Ferramentas Jurídicas <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">Gratuitas</span>
                            </h1>
                            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                                Utilitários essenciais para agilizar o dia a dia do seu escritório.
                                Sem cadastro, sem custo, direto ao ponto.
                            </p>
                        </div>

                        <div className="grid md:grid-cols-3 gap-8">
                            {tools.map((tool, idx) => (
                                <Link key={idx} href={tool.link}>
                                    <motion.div
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: idx * 0.1 }}
                                        className="h-full bg-slate-900/50 border border-slate-800 rounded-2xl p-8 hover:border-blue-500/50 hover:bg-slate-800/50 transition-all group cursor-pointer relative overflow-hidden"
                                    >
                                        {/* Hover Glow */}
                                        <div className={`absolute inset-0 bg-gradient-to-br ${tool.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`} />

                                        <div className="flex justify-between items-start mb-6">
                                            <div className={`p-4 rounded-xl bg-gradient-to-br ${tool.gradient} bg-opacity-10`}>
                                                <tool.icon className="text-3xl text-white" />
                                            </div>
                                            <span className="px-3 py-1 bg-slate-800 rounded-full text-xs font-medium text-gray-300 border border-slate-700">
                                                {tool.badge}
                                            </span>
                                        </div>

                                        <h3 className="text-2xl font-bold text-white mb-3 group-hover:text-blue-400 transition-colors">
                                            {tool.title}
                                        </h3>
                                        <p className="text-gray-400 mb-6">
                                            {tool.description}
                                        </p>

                                        <div className="flex items-center text-blue-400 font-semibold group-hover:translate-x-2 transition-transform">
                                            Acessar Ferramenta
                                            <FaArrowRight className="ml-2" />
                                        </div>
                                    </motion.div>
                                </Link>
                            ))}
                        </div>
                    </div>
                </main>

                <Footer />
            </div>
        </>
    )
}
