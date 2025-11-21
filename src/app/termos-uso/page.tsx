'use client'

import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

export default function TermosUsoPage() {
    return (
        <>
            <SEOHead
                title="Termos de Uso - Genesys Tecnologia"
                description="Termos de Uso e Condições de Serviço da Genesys Tecnologia. Regras e diretrizes para utilização de nossos softwares e serviços jurídicos."
                keywords="termos de uso, contrato de licença, SLA, condições de serviço, software jurídico"
                canonical="https://genesys-tecnologia.com.br/termos-uso"
            />
            <div className="min-h-screen bg-slate-950 text-gray-300">
                <PremiumHeader />

                <main className="pt-32 pb-20 px-4">
                    <div className="max-w-4xl mx-auto">
                        <h1 className="text-4xl md:text-5xl font-bold text-white mb-8">
                            Termos de Uso
                        </h1>

                        <div className="prose prose-invert prose-lg max-w-none">
                            <p className="lead text-xl text-gray-400 mb-8">
                                Bem-vindo à Genesys Tecnologia. Ao acessar nosso site ou utilizar nossos serviços,
                                você concorda em cumprir e estar vinculado aos seguintes termos e condições de uso.
                            </p>

                            <div className="bg-slate-900/50 p-6 rounded-xl border-l-4 border-blue-500 mb-12">
                                <p className="mb-0 text-gray-300">
                                    <strong>Nota Importante:</strong> O uso de nossos serviços de IA jurídica é destinado a auxiliar,
                                    e não substituir, o julgamento profissional de advogados e profissionais do direito.
                                </p>
                            </div>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">1. Aceitação dos Termos</h2>
                            <p>
                                Ao utilizar os serviços da Genesys Tecnologia (&quot;Serviços&quot;), você concorda com estes Termos de Uso.
                                Se você não concordar com qualquer parte destes termos, não deverá utilizar nossos Serviços.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">2. Licença de Uso</h2>
                            <p>
                                Concedemos a você uma licença limitada, não exclusiva, intransferível e revogável para acessar
                                e utilizar nossos Serviços para fins profissionais internos, sujeito a estes Termos.
                            </p>
                            <p>Você concorda em não:</p>
                            <ul>
                                <li>Modificar, copiar, distribuir ou criar trabalhos derivados de nossos Serviços</li>
                                <li>Realizar engenharia reversa ou tentar extrair o código-fonte de nosso software</li>
                                <li>Utilizar os Serviços para qualquer finalidade ilegal ou não autorizada</li>
                                <li>Compartilhar suas credenciais de acesso com terceiros</li>
                            </ul>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">3. Propriedade Intelectual</h2>
                            <p>
                                Todos os direitos, títulos e interesses relativos aos Serviços, incluindo software, design,
                                textos, gráficos e logotipos, são de propriedade exclusiva da Genesys Tecnologia ou de seus licenciadores.
                                Nossos Serviços são protegidos por leis de direitos autorais e propriedade intelectual.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">4. Responsabilidades e Limitações</h2>
                            <p>
                                Embora nos esforcemos para fornecer informações precisas e atualizadas, nossos Serviços baseados em IA
                                podem conter erros ou imprecisões. A Genesys Tecnologia não garante a precisão, integridade ou
                                adequação das informações geradas.
                            </p>
                            <p>
                                Em nenhuma circunstância a Genesys Tecnologia será responsável por quaisquer danos indiretos,
                                incidentais, especiais ou consequentes decorrentes do uso ou incapacidade de uso dos Serviços.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">5. Disponibilidade e SLA</h2>
                            <p>
                                Empregamos nossos melhores esforços para manter os Serviços disponíveis 24 horas por dia, 7 dias por semana.
                                No entanto, interrupções podem ocorrer para manutenção, atualizações ou devido a falhas fora de nosso controle.
                                Para clientes Enterprise, os níveis de serviço (SLA) são regidos por contrato específico.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">6. Cancelamento e Rescisão</h2>
                            <p>
                                Podemos suspender ou encerrar seu acesso aos Serviços imediatamente, sem aviso prévio ou responsabilidade,
                                por qualquer motivo, incluindo, sem limitação, a violação destes Termos.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">7. Alterações nos Termos</h2>
                            <p>
                                Reservamo-nos o direito de modificar estes Termos a qualquer momento. As alterações entrarão em vigor
                                imediatamente após a publicação no site. O uso continuado dos Serviços após as alterações constitui
                                sua aceitação dos novos Termos.
                            </p>

                            <h2 className="text-2xl font-bold text-white mt-12 mb-6">8. Lei Aplicável</h2>
                            <p>
                                Estes Termos serão regidos e interpretados de acordo com as leis da República Federativa do Brasil.
                                Qualquer disputa decorrente destes Termos será submetida à jurisdição exclusiva dos tribunais da
                                comarca de Uberlândia, MG.
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
