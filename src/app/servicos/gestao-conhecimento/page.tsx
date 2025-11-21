'use client'

import { FaDatabase, FaSearch, FaShareAlt, FaBrain, FaCloudUploadAlt, FaArrowRight } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'

export default function GestaoConhecimentoPage() {
    const features = [
        {
            icon: FaDatabase,
            title: 'Base Centralizada',
            description: 'Todo o conhecimento do seu escritório em um único lugar seguro e acessível',
            gradient: 'from-indigo-600 to-blue-600'
        },
        {
            icon: FaSearch,
            title: 'Busca Semântica',
            description: 'Encontre documentos pelo sentido e contexto, não apenas por palavras-chave',
            gradient: 'from-blue-600 to-cyan-600'
        },
        {
            icon: FaShareAlt,
            title: 'Colaboração Real',
            description: 'Compartilhe conhecimento e trabalhe em equipe de forma eficiente',
            gradient: 'from-cyan-600 to-teal-600'
        },
        {
            icon: FaBrain,
            title: 'IA Generativa',
            description: 'Gere novos documentos baseados no conhecimento acumulado da sua equipe',
            gradient: 'from-teal-600 to-emerald-600'
        }
    ]

    const benefits = [
        'Acesso instantâneo ao conhecimento',
        'Redução de 90% no tempo de busca',
        'Colaboração eficiente entre equipes',
        'Preservação do capital intelectual',
        'Onboarding acelerado de novos advogados',
        'Padronização de peças jurídicas',
        'Versionamento automático',
        'Controle de acesso granular'
    ]

    const solutions = [
        {
            title: 'Wiki Jurídica',
            description: 'Crie uma enciclopédia interna com seus modelos e teses',
            icon: '📚',
            status: 'Colaborativo'
        },
        {
            title: 'Smart Search',
            description: 'Busca tipo Google para seus documentos internos',
            icon: '🔍',
            status: 'IA Powered'
        },
        {
            title: 'Gestão de Versões',
            description: 'Nunca mais perca uma alteração importante',
            icon: 'history', // Using text icon for consistency with previous file if needed, or replace with component
            status: 'Automático'
        },
        {
            title: 'Hub de Modelos',
            description: 'Templates sempre atualizados e prontos para uso',
            icon: '📝',
            status: 'Organizado'
        }
    ]

    // Fix icon for solution 3
    solutions[2].icon = '⏱️'

    const stats = [
        { value: '-90%', label: 'Tempo de Busca', icon: '⚡' },
        { value: '100%', label: 'Retenção', icon: '🧠' },
        { value: 'Total', label: 'Organização', icon: '🗂️' },
        { value: '24/7', label: 'Disponibilidade', icon: '🌐' }
    ]

    return (
        <>
            <SEOHead
                title="Gestão de Conhecimento - Genesys Tecnologia"
                description="Centralize e organize todo o conhecimento jurídico do seu escritório. Busca inteligente, colaboração e preservação do capital intelectual."
                keywords="gestão de conhecimento jurídico, knowledge management, busca semântica, base de conhecimento, wiki jurídica"
                canonical="https://genesys-tecnologia.com.br/servicos/gestao-conhecimento"
            />
            <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
                <PremiumHeader />

                {/* Hero Section */}
                <section className="pt-32 pb-20 px-4">
                    <div className="max-w-7xl mx-auto">
                        <div className="grid lg:grid-cols-2 gap-12 items-center">
                            <motion.div
                                initial={{ opacity: 0, x: -50 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.6 }}
                            >
                                <div className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-500/10 border border-indigo-500/30 rounded-full mb-6">
                                    <FaDatabase className="text-indigo-400" />
                                    <span className="text-indigo-300 text-sm font-medium">Knowledge Management</span>
                                </div>

                                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-indigo-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
                                    Gestão de Conhecimento
                                </h1>

                                <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                                    Transforme a informação do seu escritório em inteligência competitiva.
                                    Centralize, organize e encontre tudo em segundos com nossa IA.
                                </p>

                                <div className="grid grid-cols-2 gap-4 mb-8">
                                    {stats.map((stat, idx) => (
                                        <div key={idx} className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                                            <div className="text-2xl mb-1">{stat.icon}</div>
                                            <div className="text-2xl font-bold text-indigo-400">{stat.value}</div>
                                            <div className="text-xs text-gray-400 mt-1">{stat.label}</div>
                                        </div>
                                    ))}
                                </div>

                                <div className="flex flex-wrap gap-4">
                                    <button
                                        onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de conhecer a solução de Gestão de Conhecimento.', '_blank')}
                                        className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg font-semibold hover:shadow-xl hover:shadow-indigo-500/50 transition-all hover:scale-105 flex items-center gap-2"
                                    >
                                        Ver Demonstração
                                        <FaArrowRight />
                                    </button>
                                    <button
                                        onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre preços de Gestão de Conhecimento.', '_blank')}
                                        className="px-8 py-4 bg-slate-800 text-white rounded-lg font-semibold border border-slate-700 hover:border-indigo-500/50 transition-all hover:scale-105"
                                    >
                                        Consultar Preços
                                    </button>
                                </div>
                            </motion.div>

                            <motion.div
                                initial={{ opacity: 0, x: 50 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.6, delay: 0.2 }}
                                className="relative"
                            >
                                <div className="bg-gradient-to-br from-indigo-600/20 to-blue-600/20 rounded-3xl p-8 border border-indigo-500/30 backdrop-blur-sm">
                                    <div className="space-y-4">
                                        {benefits.slice(0, 6).map((benefit, idx) => (
                                            <motion.div
                                                key={idx}
                                                initial={{ opacity: 0, x: 20 }}
                                                animate={{ opacity: 1, x: 0 }}
                                                transition={{ delay: 0.3 + idx * 0.1 }}
                                                className="flex items-center gap-3 text-gray-200"
                                            >
                                                <FaCloudUploadAlt className="text-green-400 flex-shrink-0" />
                                                <span>{benefit}</span>
                                            </motion.div>
                                        ))}
                                    </div>
                                </div>
                            </motion.div>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section className="py-20 px-4 bg-slate-900/50">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center mb-16">
                            <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                                Inteligência Coletiva
                            </h2>
                            <p className="text-xl text-gray-400">
                                Potencialize o conhecimento da sua equipe
                            </p>
                        </div>

                        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                            {features.map((feature, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, y: 20 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    viewport={{ once: true }}
                                    transition={{ delay: idx * 0.1 }}
                                    className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 hover:border-indigo-500/50 transition-all hover:shadow-xl hover:shadow-indigo-500/20"
                                >
                                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4`}>
                                        <feature.icon className="text-2xl text-white" />
                                    </div>
                                    <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                                    <p className="text-gray-400">{feature.description}</p>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Solutions Section */}
                <section className="py-20 px-4">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center mb-16">
                            <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                                Ferramentas Poderosas
                            </h2>
                            <p className="text-xl text-gray-400">
                                Tudo que você precisa para organizar seu escritório
                            </p>
                        </div>

                        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                            {solutions.map((solution, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    whileInView={{ opacity: 1, scale: 1 }}
                                    viewport={{ once: true }}
                                    transition={{ delay: idx * 0.1 }}
                                    className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-indigo-500/50 transition-all"
                                >
                                    <div className="text-5xl mb-4 text-center">{solution.icon}</div>
                                    <h3 className="text-lg font-bold text-white mb-2 text-center">{solution.title}</h3>
                                    <p className="text-sm text-gray-400 mb-4 text-center">{solution.description}</p>
                                    <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-2 text-center">
                                        <span className="text-indigo-400 font-semibold text-sm">{solution.status}</span>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="py-20 px-4">
                    <div className="max-w-4xl mx-auto">
                        <div className="bg-gradient-to-r from-indigo-600 to-blue-600 rounded-3xl p-12 text-center">
                            <h2 className="text-4xl font-bold text-white mb-4">
                                Pare de perder tempo procurando arquivos
                            </h2>
                            <p className="text-xl text-indigo-100 mb-8">
                                Organize seu escritório hoje mesmo com nossa IA
                            </p>
                            <button
                                onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de organizar a gestão de conhecimento do meu escritório.', '_blank')}
                                className="bg-white text-indigo-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105 inline-flex items-center gap-2"
                            >
                                Começar Agora
                                <FaArrowRight />
                            </button>
                        </div>
                    </div>
                </section>

                <Footer />
            </div>
        </>
    )
}
