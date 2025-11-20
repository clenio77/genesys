'use client'

import Image from 'next/image'
import Link from 'next/link'
import { FaRocket, FaUsers, FaAward, FaChartLine, FaLinkedin, FaGithub, FaInstagram } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

export default function SobrePage() {
  const equipe = [
    {
      nome: 'Clênio Moura',
      cargo: 'CEO & Fundador',
      foto: '/images/clenio.png',
      bio: 'CEO & Fundador da Genesys Tecnologia. Desenvolvedor Python especializado em Inteligência Artificial. Engenheiro de IA com foco em automação de processos e desenvolvimento de agentes inteligentes. Especialista em IA e Direito com 15+ anos de experiência.',
      linkedin: '#',
      github: '#',
      instagram: 'https://www.instagram.com/afonso.clenio?utm_source=qr&igsh=eXM1cWtvOWZ2dThq'
    },
    {
      nome: 'Lilian Santos',
      cargo: 'Advogada Trabalhista',
      foto: '/images/lilian1.png',
      bio: 'CEO & Fundadora da Genesys Tecnologia. Advogada trabalhista especializada em direito do trabalho com vasta experiência em relações trabalhistas. Conhecimento profundo em legislação trabalhista, processos e consultoria jurídica. Atuação dedicada à defesa dos direitos trabalhistas.',
      linkedin: '#',
      github: '#',
      instagram: 'https://www.instagram.com/adv.liliantrabalhista?igsh=ZmE3aG8ycHNubDgw'
    },
    {
      nome: 'Firmino Costa',
      cargo: 'Advogado Criminalista',
      foto: '/images/firmino1.png',
      bio: 'CEO & Fundador da Genesys Tecnologia. Advogado criminalista com mais de 15 anos de experiência em casos complexos. Especialista em direito penal, jurisprudência criminal e defesa estratégica. Atuação focada em resultados e excelência jurídica.',
      linkedin: '#',
      github: '#',
      instagram: 'https://www.instagram.com/firmino.adv?igsh=M2N3cGkxdGtoOWgw'
    }
  ]

  const valores = [
    {
      icon: FaRocket,
      titulo: 'Inovação',
      descricao: 'Buscamos constantemente novas tecnologias para revolucionar o setor jurídico'
    },
    {
      icon: FaUsers,
      titulo: 'Colaboração',
      descricao: 'Trabalhamos em parceria com nossos clientes para criar soluções personalizadas'
    },
    {
      icon: FaAward,
      titulo: 'Excelência',
      descricao: 'Comprometidos com a mais alta qualidade em tudo que fazemos'
    },
    {
      icon: FaChartLine,
      titulo: 'Resultados',
      descricao: 'Focados em entregar valor real e mensurável para nossos clientes'
    }
  ]

  const timeline = [
    { ano: '2020', evento: 'Fundação da Genesys Tecnologia' },
    { ano: '2021', evento: 'Lançamento do Kermartin IA v1.0' },
    { ano: '2022', evento: '100+ clientes ativos' },
    { ano: '2023', evento: 'Expansão nacional e novos módulos' },
    { ano: '2024', evento: '500+ clientes e reconhecimento internacional' }
  ]

  return (
    <>
      <SEOHead
        title="Sobre - Genesys Tecnologia | Inovação em IA Jurídica"
        description="Conheça a Genesys Tecnologia, empresa pioneira em soluções de Inteligência Artificial para o setor jurídico. Nossa história, valores e equipe."
        keywords="sobre genesys, empresa ia jurídica, tecnologia jurídica, inovação legal tech, equipe genesys"
        canonical="https://genesys-tecnologia.com.br/sobre"
      />
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <PremiumHeader />

        {/* Hero Section */}
        <section className="pt-32 pb-20 px-4">
          <div className="max-w-7xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Sobre a Genesys
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-12">
              Transformando o futuro da prática jurídica com inteligência artificial
            </p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="text-4xl font-bold text-blue-400 mb-2">500+</div>
                <div className="text-sm text-gray-400">Clientes Ativos</div>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="text-4xl font-bold text-cyan-400 mb-2">50K+</div>
                <div className="text-sm text-gray-400">Casos Analisados</div>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="text-4xl font-bold text-purple-400 mb-2">99%</div>
                <div className="text-sm text-gray-400">Satisfação</div>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="text-4xl font-bold text-green-400 mb-2">4 anos</div>
                <div className="text-sm text-gray-400">No Mercado</div>
              </div>
            </div>
          </div>
        </section>

        {/* Nossa História */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  Nossa História
                </h2>
                <div className="space-y-4 text-gray-300 text-lg leading-relaxed">
                  <p>
                    A Genesys Tecnologia nasceu em 2020 com uma missão clara: democratizar o acesso
                    à tecnologia de ponta para profissionais do direito.
                  </p>
                  <p>
                    Fundada por especialistas em IA e direito, combinamos expertise técnica com
                    profundo conhecimento jurídico para criar soluções que realmente fazem a diferença.
                  </p>
                  <p>
                    Hoje, somos referência em Legal Tech no Brasil, atendendo desde advogados
                    autônomos até grandes escritórios e departamentos jurídicos corporativos.
                  </p>
                  <p>
                    Nossa plataforma Kermartin IA já analisou mais de 50 mil casos, economizando
                    milhares de horas de trabalho e milhões de reais para nossos clientes.
                  </p>
                </div>
              </div>

              <div className="relative">
                <div className="aspect-square rounded-3xl overflow-hidden bg-gradient-to-br from-blue-600/20 to-cyan-600/20 backdrop-blur-sm border border-blue-500/30">
                  <Image
                    src="/images/genesys-sala.webp"
                    alt="Genesys Tecnologia - Nossa História"
                    width={1024}
                    height={1024}
                    className="object-cover w-full h-full"
                    priority
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Timeline */}
        <section className="py-20 px-4">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold mb-16 text-center bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Nossa Jornada
            </h2>

            <div className="relative">
              {/* Linha vertical */}
              <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-500 to-cyan-500 hidden md:block" />

              <div className="space-y-12">
                {timeline.map((item, index) => (
                  <div
                    key={index}
                    className={`flex items-center gap-8 ${index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'
                      }`}
                  >
                    <div className={`flex-1 ${index % 2 === 0 ? 'md:text-right' : 'md:text-left'}`}>
                      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700 hover:border-blue-500/50 transition-all">
                        <div className="text-3xl font-bold text-blue-400 mb-2">{item.ano}</div>
                        <div className="text-lg text-gray-300">{item.evento}</div>
                      </div>
                    </div>

                    <div className="hidden md:block w-4 h-4 bg-blue-500 rounded-full border-4 border-slate-900 relative z-10" />

                    <div className="flex-1" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Valores */}
        <section className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold mb-16 text-center bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Nossos Valores
            </h2>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {valores.map((valor, index) => {
                const Icon = valor.icon
                return (
                  <div
                    key={index}
                    className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-blue-500/50 transition-all text-center"
                  >
                    <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-xl flex items-center justify-center text-white text-2xl mx-auto mb-4">
                      <Icon />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-3">{valor.titulo}</h3>
                    <p className="text-gray-300">{valor.descricao}</p>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* Equipe */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-center bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Nossa Equipe
            </h2>
            <p className="text-xl text-gray-300 text-center mb-16 max-w-3xl mx-auto">
              Profissionais especializados unidos pela paixão em transformar o setor jurídico
            </p>

            <div className="grid md:grid-cols-3 gap-8">
              {equipe.map((membro, index) => (
                <div
                  key={index}
                  className="group bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-blue-500/50 transition-all text-center"
                >
                  <div className="relative w-32 h-32 mx-auto mb-6 rounded-full overflow-hidden border-4 border-blue-500/30 group-hover:border-blue-500 transition-all">
                    <Image
                      src={membro.foto}
                      alt={membro.nome}
                      fill
                      className="object-cover"
                    />
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-2">{membro.nome}</h3>
                  <p className="text-cyan-400 font-medium mb-4">{membro.cargo}</p>
                  <p className="text-gray-300 mb-6">{membro.bio}</p>
                  <div className="flex justify-center gap-4">
                    <a
                      href={membro.linkedin}
                      className="w-10 h-10 bg-slate-700 hover:bg-blue-600 rounded-full flex items-center justify-center text-white transition-all"
                    >
                      <FaLinkedin />
                    </a>
                    <a
                      href={membro.github}
                      className="w-10 h-10 bg-slate-700 hover:bg-blue-600 rounded-full flex items-center justify-center text-white transition-all"
                    >
                      <FaGithub />
                    </a>
                    {membro.instagram && (
                      <a
                        href={membro.instagram}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-full flex items-center justify-center text-white transition-all"
                      >
                        <FaInstagram />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl p-12">
            <h2 className="text-4xl font-bold text-white mb-4">
              Quer fazer parte dessa transformação?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Junte-se a centenas de profissionais que já revolucionaram sua prática jurídica
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                href="/produtos"
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
              >
                Conhecer Produtos
              </Link>
              <Link
                href="#contact"
                className="bg-blue-800 text-white px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
              >
                Falar Conosco
              </Link>
            </div>
          </div>
        </section>

        <Footer />
      </div>
    </>
  )
}

