'use client'

import Image from 'next/image'
import { FaGavel, FaBriefcase, FaCode, FaLinkedin, FaTwitter } from 'react-icons/fa'

export default function TeamSection() {
  const teamMembers = [
    {
      name: 'Firmino',
      role: 'Advogado Criminalista',
      description: 'Especialista em direito penal com mais de 15 anos de experiência em casos complexos. Expertise em jurisprudência criminal e defesa estratégica.',
      image: '/images/firmino1.png',
      icon: FaGavel,
      tags: ['Direito Penal', 'Jurisprudência', 'Defesa Criminal'],
      social: {
        linkedin: '#',
        twitter: '#'
      }
    },
    {
      name: 'Lilian',
      role: 'Advogada Trabalhista',
      description: 'Especialista em direito do trabalho com vasta experiência em relações trabalhistas. Conhecimento profundo em legislação trabalhista e processos.',
      image: '/images/lilian1.png',
      icon: FaBriefcase,
      tags: ['Direito do Trabalho', 'Relações Trabalhistas', 'Legislação'],
      social: {
        linkedin: '#',
        twitter: '#'
      }
    },
    {
      name: 'Clenio',
      role: 'Desenvolvedor & Engenheiro de IA',
      description: 'Desenvolvedor Python especializado em Inteligência Artificial. Engenheiro de IA com foco em automação de processos e desenvolvimento de agentes inteligentes.',
      image: '/images/clenio.png',
      icon: FaCode,
      tags: ['Python', 'Inteligência Artificial', 'Automação', 'Agentes IA'],
      social: {
        linkedin: '#',
        twitter: '#'
      }
    }
  ]

  return (
    <section id="team" className="py-20 bg-gradient-to-b from-genesys-navy to-genesys-dark">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold font-playfair mb-6">
            <span className="gradient-text">Nossa Equipe</span>
          </h2>
          <p className="text-xl text-genesys-slate max-w-3xl mx-auto">
            Profissionais especializados unindo expertise jurídica e tecnológica
          </p>
        </div>
        
        {/* Team Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {teamMembers.map((member, index) => (
            <div key={index} className="team-card group">
              {/* Profile Image */}
              <div className="relative mb-6">
                <div className="w-32 h-32 mx-auto relative overflow-hidden rounded-full border-4 border-genesys-gold/20 group-hover:border-genesys-gold transition-colors duration-300">
                  <Image
                    src={member.image}
                    alt={member.name}
                    fill
                    sizes="(max-width: 768px) 50vw, 25vw"
                    className="object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-genesys-dark/50 to-transparent"></div>
                </div>
                
                {/* Icon */}
                <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <member.icon className="text-white text-xl" />
                </div>
              </div>
              
              {/* Content */}
              <div className="text-center">
                <h3 className="text-2xl font-bold font-playfair mb-2 gradient-text">
                  {member.name}
                </h3>
                <p className="text-genesys-gold font-semibold mb-4">
                  {member.role}
                </p>
                <p className="text-genesys-slate text-sm leading-relaxed mb-6">
                  {member.description}
                </p>
                
                {/* Tags */}
                <div className="flex flex-wrap justify-center gap-2 mb-6">
                  {member.tags.map((tag, tagIndex) => (
                    <span
                      key={tagIndex}
                      className="px-3 py-1 bg-white/10 rounded-full text-xs text-genesys-cream border border-white/20"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                
                {/* Social Links */}
                <div className="flex justify-center space-x-4">
                  <a
                    href={member.social.linkedin}
                    className="w-10 h-10 bg-blue-600 hover:bg-blue-700 rounded-full flex items-center justify-center text-white transition-colors duration-300"
                    aria-label={`LinkedIn de ${member.name}`}
                  >
                    <FaLinkedin className="text-sm" />
                  </a>
                  <a
                    href={member.social.twitter}
                    className="w-10 h-10 bg-cyan-500 hover:bg-cyan-600 rounded-full flex items-center justify-center text-white transition-colors duration-300"
                    aria-label={`Twitter de ${member.name}`}
                  >
                    <FaTwitter className="text-sm" />
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Team Stats */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text font-playfair">15+</div>
            <div className="text-genesys-slate text-sm">Anos de Experiência</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text font-playfair">1000+</div>
            <div className="text-genesys-slate text-sm">Casos Analisados</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text font-playfair">50+</div>
            <div className="text-genesys-slate text-sm">Projetos de IA</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text font-playfair">98%</div>
            <div className="text-genesys-slate text-sm">Taxa de Sucesso</div>
          </div>
        </div>
      </div>
    </section>
  )
}
