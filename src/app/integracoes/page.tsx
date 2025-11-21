'use client'

import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'
import { FaWhatsapp, FaSlack, FaTrello, FaGoogle, FaMicrosoft, FaBalanceScale, FaCloud, FaRobot, FaDatabase } from 'react-icons/fa'
import { SiAsana, SiNotion, SiSalesforce, SiHubspot, SiZendesk } from 'react-icons/si'

export default function IntegracoesPage() {
    const categories = [
        {
            title: 'Tribunais e Sistemas Judiciais',
            description: 'Conecte-se automaticamente aos principais sistemas da justiça brasileira.',
            icon: FaBalanceScale,
            gradient: 'from-blue-600 to-cyan-600',
            integrations: [
                { name: 'PJe', status: 'Nativo', description: 'Processo Judicial Eletrônico' },
                { name: 'e-SAJ', status: 'Nativo', description: 'Sistema de Automação da Justiça' },
                { name: 'Projudi', status: 'Nativo', description: 'Processo Judicial Digital' },
                { name: 'Eproc', status: 'Beta', description: 'Sistema de Processo Eletrônico' },
                { name: 'Tucujuris', status: 'Em Breve', description: 'Gestão Processual' }
            ]
        },
        {
            title: 'Comunicação e Atendimento',
            description: 'Centralize o atendimento ao cliente e notificações.',
            icon: FaWhatsapp,
            gradient: 'from-green-600 to-emerald-600',
            integrations: [
                { name: 'WhatsApp Business', status: 'Nativo', icon: FaWhatsapp, description: 'API Oficial e Web' },
                { name: 'Slack', status: 'Nativo', icon: FaSlack, description: 'Notificações de equipe' },
                { name: 'Microsoft Teams', status: 'Nativo', icon: FaMicrosoft, description: 'Colaboração corporativa' },
                { name: 'Zendesk', status: 'Beta', icon: SiZendesk, description: 'Suporte ao cliente' }
            ]
        },
        {
            title: 'Produtividade e Gestão',
            description: 'Sincronize prazos, tarefas e documentos.',
            icon: FaCloud,
            gradient: 'from-purple-600 to-pink-600',
            integrations: [
                { name: 'Google Workspace', status: 'Nativo', icon: FaGoogle, description: 'Calendar, Drive e Gmail' },
                { name: 'Trello', status: 'Nativo', icon: FaTrello, description: 'Gestão de quadros' },
                { name: 'Asana', status: 'Nativo', icon: SiAsana, description: 'Gestão de projetos' },
                { name: 'Notion', status: 'Beta', icon: SiNotion, description: 'Base de conhecimento' }
            ]
        },
        {
            title: 'CRM e Vendas',
            description: 'Gerencie leads e oportunidades jurídicas.',
            icon: FaDatabase,
            gradient: 'from-orange-600 to-red-600',
            integrations: [
                { name: 'Salesforce', status: 'Enterprise', icon: SiSalesforce, description: 'CRM líder mundial' },
                { name: 'HubSpot', status: 'Nativo', icon: SiHubspot, description: 'Inbound Marketing' },
                { name: 'RD Station', status: 'Nativo', description: 'Automação de Marketing' }
            ]
        }
    ]

    return (
        <>
            <SEOHead
                title="Integrações - Genesys Tecnologia"
                description="Conecte a Genesys aos seus softwares favoritos: PJe, WhatsApp, Google, Trello e muito mais."
                keywords="integrações jurídicas, api pje, api esaj, automação whatsapp, legaltech integrations"
                canonical="https://genesys-tecnologia.com.br/integracoes"
            />
            <div className="min-h-screen bg-slate-950 text-gray-300">
                <PremiumHeader />

                <main className="pt-32 pb-20 px-4">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center mb-20">
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 rounded-full border border-slate-700 mb-6"
                            >
                                <FaRobot className="text-blue-400" />
                                <span className="text-sm font-medium text-blue-300">Ecossistema Conectado</span>
                            </motion.div>

                            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
                                Conecte a Genesys ao <br />
                                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">seu fluxo de trabalho</span>
                            </h1>
                            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                                Não mude a forma como você trabalha. Apenas torne-a mais inteligente.
                                Nossa plataforma se integra nativamente às ferramentas que você já usa.
                            </p>
                        </div>

                        <div className="grid gap-12">
                            {categories.map((category, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, y: 40 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    viewport={{ once: true }}
                                    transition={{ delay: idx * 0.1 }}
                                >
                                    <div className="flex items-center gap-4 mb-8">
                                        <div className={`p-3 rounded-xl bg-gradient-to-br ${category.gradient} bg-opacity-10`}>
                                            <category.icon className="text-2xl text-white" />
                                        </div>
                                        <div>
                                            <h2 className="text-2xl font-bold text-white">{category.title}</h2>
                                            <p className="text-gray-400">{category.description}</p>
                                        </div>
                                    </div>

                                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                                        {category.integrations.map((integration, i) => (
                                            <div
                                                key={i}
                                                className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 hover:border-blue-500/30 hover:bg-slate-800 transition-all group"
                                            >
                                                <div className="flex justify-between items-start mb-4">
                                                    {integration.icon ? (
                                                        <integration.icon className="text-3xl text-gray-400 group-hover:text-white transition-colors" />
                                                    ) : (
                                                        <div className="w-8 h-8 rounded bg-slate-800 flex items-center justify-center font-bold text-gray-400 group-hover:text-white">
                                                            {integration.name[0]}
                                                        </div>
                                                    )}
                                                    <span className={`text-xs font-bold px-2 py-1 rounded-full ${integration.status === 'Nativo' ? 'bg-green-500/10 text-green-400' :
                                                            integration.status === 'Beta' ? 'bg-blue-500/10 text-blue-400' :
                                                                integration.status === 'Enterprise' ? 'bg-purple-500/10 text-purple-400' :
                                                                    'bg-slate-700 text-gray-400'
                                                        }`}>
                                                        {integration.status}
                                                    </span>
                                                </div>
                                                <h3 className="text-lg font-bold text-white mb-1">{integration.name}</h3>
                                                <p className="text-sm text-gray-500">{integration.description}</p>
                                            </div>
                                        ))}
                                    </div>
                                </motion.div>
                            ))}
                        </div>

                        {/* CTA API */}
                        <div className="mt-20 p-8 md:p-12 bg-gradient-to-r from-slate-900 to-slate-800 rounded-3xl border border-slate-700 text-center">
                            <h2 className="text-3xl font-bold text-white mb-4">Desenvolvedor?</h2>
                            <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
                                Construa suas próprias integrações com nossa API RESTful robusta e bem documentada.
                                Webhooks, autenticação OAuth2 e suporte dedicado.
                            </p>
                            <div className="flex justify-center gap-4">
                                <button className="px-6 py-3 bg-white text-slate-900 font-bold rounded-lg hover:bg-gray-100 transition-colors">
                                    Ler Documentação da API
                                </button>
                                <button className="px-6 py-3 bg-transparent border border-slate-600 text-white font-bold rounded-lg hover:border-white transition-colors">
                                    Solicitar Chave de Acesso
                                </button>
                            </div>
                        </div>
                    </div>
                </main>

                <Footer />
            </div>
        </>
    )
}
