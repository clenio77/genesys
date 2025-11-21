'use client'

import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

export default function CookiesPage() {
    return (
        <>
            <SEOHead
                title="Política de Cookies - Genesys Tecnologia"
                description="Política de Cookies da Genesys Tecnologia. Entenda como utilizamos cookies para melhorar sua experiência e como você pode gerenciá-los."
                keywords="política de cookies, cookies, privacidade, rastreamento, LGPD"
                canonical="https://genesys-tecnologia.com.br/cookies"
            />
            <div className="min-h-screen bg-slate-950 text-gray-300">
                <PremiumHeader />

                <main className="pt-32 pb-20 px-4">
                    <div className="max-w-4xl mx-auto">
                        <h1 className="text-4xl md:text-5xl font-bold text-white mb-8">
                            Política de Cookies
                        </h1>

                        <div className="prose prose-invert prose-lg max-w-none">
                            <p className="lead text-xl text-gray-400 mb-8">
                                Esta Política de Cookies explica o que são cookies, como a Genesys Tecnologia os utiliza
                                e como você pode gerenciar suas preferências.
                            </p>

                            <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-800 mb-12">
                                <h3 className="text-white mt-0">O que são Cookies?</h3>
                                <p className="mb-0">
                                    Cookies são pequenos arquivos de texto armazenados no seu dispositivo (computador, tablet ou celular)
                                    quando você visita um site. Eles permitem que o site "lembre" suas ações e preferências
                                    (como login, idioma, tamanho da fonte) por um determinado período.
                                </p>
                            </div>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">1. Como Utilizamos Cookies</h2>
                            <p>
                                Utilizamos cookies para diversos fins, incluindo:
                            </p>
                            <ul>
                                <li>Garantir o funcionamento correto do nosso site</li>
                                <li>Melhorar a segurança e prevenir atividades fraudulentas</li>
                                <li>Entender como os visitantes interagem com nosso site</li>
                                <li>Personalizar sua experiência e lembrar suas preferências</li>
                                <li>Fornecer conteúdo e publicidade relevantes</li>
                            </ul>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">2. Tipos de Cookies que Utilizamos</h2>

                            <div className="space-y-6 mt-6">
                                <div className="bg-slate-900/30 p-6 rounded-lg border-l-4 border-green-500">
                                    <h4 className="text-white font-bold mt-0 mb-2">Cookies Essenciais</h4>
                                    <p className="mb-0 text-sm">
                                        Necessários para o funcionamento básico do site. Sem eles, recursos como login e
                                        navegação segura não funcionariam. Não podem ser desativados.
                                    </p>
                                </div>

                                <div className="bg-slate-900/30 p-6 rounded-lg border-l-4 border-blue-500">
                                    <h4 className="text-white font-bold mt-0 mb-2">Cookies de Desempenho e Análise</h4>
                                    <p className="mb-0 text-sm">
                                        Coletam informações anônimas sobre como os visitantes usam o site (ex: páginas mais visitadas,
                                        tempo de permanência). Nos ajudam a melhorar a performance e usabilidade.
                                    </p>
                                </div>

                                <div className="bg-slate-900/30 p-6 rounded-lg border-l-4 border-purple-500">
                                    <h4 className="text-white font-bold mt-0 mb-2">Cookies de Funcionalidade</h4>
                                    <p className="mb-0 text-sm">
                                        Permitem que o site lembre suas escolhas (como nome de usuário, idioma ou região)
                                        para oferecer uma experiência mais personalizada.
                                    </p>
                                </div>

                                <div className="bg-slate-900/30 p-6 rounded-lg border-l-4 border-orange-500">
                                    <h4 className="text-white font-bold mt-0 mb-2">Cookies de Publicidade</h4>
                                    <p className="mb-0 text-sm">
                                        Utilizados para exibir anúncios relevantes aos seus interesses. Também limitam o número
                                        de vezes que você vê um anúncio e ajudam a medir a eficácia das campanhas.
                                    </p>
                                </div>
                            </div>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">3. Gerenciamento de Cookies</h2>
                            <p>
                                Você tem o direito de aceitar ou recusar cookies. A maioria dos navegadores aceita cookies automaticamente,
                                mas você pode modificar as configurações do seu navegador para recusá-los, se preferir.
                            </p>
                            <p>
                                Para gerenciar cookies nos navegadores mais populares:
                            </p>
                            <ul>
                                <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">Google Chrome</a></li>
                                <li><a href="https://support.mozilla.org/pt-BR/kb/protecao-contra-rastreamento-aprimorada-firefox-desktop" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">Mozilla Firefox</a></li>
                                <li><a href="https://support.apple.com/pt-br/guide/safari/sfri11471/mac" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">Safari</a></li>
                                <li><a href="https://support.microsoft.com/pt-br/microsoft-edge/excluir-cookies-no-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">Microsoft Edge</a></li>
                            </ul>
                            <p className="text-sm text-gray-500 mt-4">
                                Nota: A desativação de cookies pode limitar a funcionalidade de algumas partes do nosso site.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">4. Atualizações desta Política</h2>
                            <p>
                                Podemos atualizar esta Política de Cookies periodicamente para refletir mudanças em nossas práticas
                                ou por razões operacionais, legais ou regulatórias. Recomendamos que você reveja esta página regularmente.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">5. Contato</h2>
                            <p>
                                Se você tiver dúvidas sobre nossa utilização de cookies, entre em contato conosco através do e-mail:
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
