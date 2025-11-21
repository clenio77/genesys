'use client'

import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

export default function PoliticaPrivacidadePage() {
    return (
        <>
            <SEOHead
                title="Política de Privacidade - Genesys Tecnologia"
                description="Política de Privacidade da Genesys Tecnologia. Saiba como coletamos, usamos e protegemos seus dados pessoais em conformidade com a LGPD."
                keywords="política de privacidade, LGPD, proteção de dados, segurança da informação, termos de uso"
                canonical="https://genesys-tecnologia.com.br/politica-privacidade"
            />
            <div className="min-h-screen bg-slate-950 text-gray-300">
                <PremiumHeader />

                <main className="pt-32 pb-20 px-4">
                    <div className="max-w-4xl mx-auto">
                        <h1 className="text-4xl md:text-5xl font-bold text-white mb-8">
                            Política de Privacidade
                        </h1>

                        <div className="prose prose-invert prose-lg max-w-none">
                            <p className="lead text-xl text-gray-400 mb-8">
                                A Genesys Tecnologia (&quot;nós&quot;, &quot;nosso&quot;) está comprometida em proteger a sua privacidade.
                                Esta Política de Privacidade explica como coletamos, usamos, divulgamos e protegemos suas informações
                                quando você visita nosso site ou utiliza nossos serviços.
                            </p>

                            <div className="bg-slate-900/50 p-8 rounded-2xl border border-slate-800 mb-12">
                                <h3 className="text-white mt-0">Destaques da Política</h3>
                                <ul className="grid md:grid-cols-2 gap-4 mt-4 mb-0">
                                    <li className="flex items-start gap-2">
                                        <span className="text-green-400">✓</span>
                                        Conformidade total com a LGPD
                                    </li>
                                    <li className="flex items-start gap-2">
                                        <span className="text-green-400">✓</span>
                                        Criptografia de ponta a ponta
                                    </li>
                                    <li className="flex items-start gap-2">
                                        <span className="text-green-400">✓</span>
                                        Transparência no uso de dados
                                    </li>
                                    <li className="flex items-start gap-2">
                                        <span className="text-green-400">✓</span>
                                        Controle total sobre suas informações
                                    </li>
                                </ul>
                            </div>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">1. Coleta de Informações</h2>
                            <p>
                                Coletamos informações que você nos fornece diretamente, como quando você cria uma conta,
                                solicita uma demonstração, assina nossa newsletter ou entra em contato conosco.
                                As informações podem incluir:
                            </p>
                            <ul>
                                <li>Nome completo e informações de contato profissional</li>
                                <li>Endereço de e-mail e número de telefone</li>
                                <li>Informações da empresa e cargo</li>
                                <li>Dados de pagamento (processados de forma segura por terceiros)</li>
                            </ul>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">2. Uso das Informações</h2>
                            <p>
                                Utilizamos as informações coletadas para:
                            </p>
                            <ul>
                                <li>Fornecer, manter e melhorar nossos serviços</li>
                                <li>Processar transações e enviar avisos relacionados</li>
                                <li>Enviar comunicações técnicas, atualizações de segurança e suporte</li>
                                <li>Responder aos seus comentários, perguntas e solicitações</li>
                                <li>Monitorar e analisar tendências, uso e atividades</li>
                            </ul>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">3. Proteção de Dados</h2>
                            <p>
                                Implementamos medidas de segurança técnicas e organizacionais apropriadas para proteger
                                seus dados pessoais contra acesso não autorizado, alteração, divulgação ou destruição.
                                Nossos protocolos incluem:
                            </p>
                            <ul>
                                <li>Criptografia SSL/TLS em todas as comunicações</li>
                                <li>Armazenamento seguro em servidores certificados</li>
                                <li>Controles de acesso rigorosos e autenticação multifator</li>
                                <li>Auditorias de segurança regulares</li>
                            </ul>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">4. Compartilhamento de Dados</h2>
                            <p>
                                Não vendemos seus dados pessoais. Compartilhamos informações apenas nas seguintes circunstâncias:
                            </p>
                            <ul>
                                <li>Com fornecedores de serviços que nos auxiliam em nossas operações</li>
                                <li>Para cumprir obrigações legais ou regulatórias</li>
                                <li>Para proteger direitos, propriedade ou segurança da Genesys ou de terceiros</li>
                            </ul>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">5. Seus Direitos (LGPD)</h2>
                            <p>
                                De acordo com a Lei Geral de Proteção de Dados (LGPD), você tem direito a:
                            </p>
                            <ul>
                                <li>Confirmar a existência de tratamento de dados</li>
                                <li>Acessar seus dados pessoais</li>
                                <li>Corrigir dados incompletos, inexatos ou desatualizados</li>
                                <li>Solicitar a anonimização, bloqueio ou eliminação de dados desnecessários</li>
                                <li>Portabilidade dos dados a outro fornecedor de serviço</li>
                                <li>Revogar o consentimento a qualquer momento</li>
                            </ul>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">6. Cookies e Tecnologias Similares</h2>
                            <p>
                                Utilizamos cookies para melhorar sua experiência de navegação, analisar o tráfego do site
                                e personalizar conteúdo. Você pode controlar o uso de cookies através das configurações do seu navegador.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">7. Contato</h2>
                            <p>
                                Se você tiver dúvidas sobre esta Política de Privacidade ou sobre o tratamento de seus dados,
                                entre em contato com nosso Encarregado de Proteção de Dados (DPO) através do e-mail:
                                <a href="mailto:dpo@genesys-tecnologia.com.br" className="text-blue-400 hover:text-blue-300 ml-1">
                                    dpo@genesys-tecnologia.com.br
                                </a>
                            </p>

                            <div className="border-t border-slate-800 mt-12 pt-8 text-sm text-gray-500">
                                Última atualização: 20 de Novembro de 2025
                            </div>
                        </div>
                    </div>
                </main>

                <Footer />
            </div>
        </>
    )
}
