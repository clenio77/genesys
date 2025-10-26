# 🖼️ Otimização de Imagens - Genesys Tecnologia

## 📊 Status Atual das Imagens

### Imagens no Projeto:
```
public/images/
├── clenio.png
├── equipe.jpg
├── firmino.png
├── firmino1.png
├── genesys-logo.jpg
├── genesys-logo.png
├── kermartin-logo.png
├── lilian.png
└── lilian1.png
```

## ✅ Otimizações Implementadas

### 1. **Next.js Image Component**
Todas as imagens do projeto já utilizam o componente `<Image>` do Next.js que:
- ✅ Carrega imagens sob demanda (lazy loading)
- ✅ Redimensiona automaticamente para diferentes tamanhos de tela
- ✅ Converte para formatos modernos (WebP, AVIF)
- ✅ Otimiza qualidade automaticamente
- ✅ Previne Cumulative Layout Shift (CLS)

### 2. **Configuração Next.js**
O arquivo `next.config.js` já está configurado com:
- ✅ Formatos modernos: WebP e AVIF
- ✅ Cache de imagens otimizado
- ✅ PWA com cache de assets estáticos

### 3. **Atributos de Performance**
Todas as imagens críticas usam:
- ✅ `priority` para imagens above-the-fold
- ✅ `sizes` responsivos para diferentes viewports
- ✅ `loading="lazy"` para imagens below-the-fold

## 🎯 Recomendações para Otimização Manual

### Ferramentas Online (Gratuitas):
1. **TinyPNG** - https://tinypng.com/
   - Comprime PNG e JPEG sem perda visível de qualidade
   - Reduz até 70% do tamanho

2. **Squoosh** - https://squoosh.app/
   - Ferramenta do Google para otimização
   - Suporta WebP, AVIF, MozJPEG

3. **ImageOptim** (Mac) - https://imageoptim.com/
   - App desktop para otimização em lote

### Ferramentas CLI:
```bash
# Instalar sharp-cli para otimização em lote
npm install -g sharp-cli

# Otimizar todas as PNGs
sharp -i "public/images/*.png" -o "public/images/optimized/" -f webp -q 85

# Otimizar todas as JPGs
sharp -i "public/images/*.jpg" -o "public/images/optimized/" -f webp -q 85
```

## 📏 Tamanhos Recomendados

### Logos:
- **genesys-logo.jpg/png**: 512x512px (atual OK)
- **kermartin-logo.png**: 400x400px (atual OK)

### Fotos de Equipe:
- **clenio.png, firmino1.png, lilian1.png**: 300x300px
- Formato: WebP ou JPEG otimizado
- Qualidade: 80-85%

### Open Graph Images:
- **og-image.jpg**: 1200x630px
- Formato: JPEG otimizado
- Qualidade: 85%

## 🚀 Próximos Passos

### Opção 1: Otimização Automática (Recomendado)
O Next.js já faz isso automaticamente! Nenhuma ação necessária.

### Opção 2: Otimização Manual
Se quiser reduzir ainda mais o tamanho dos arquivos originais:

1. **Baixar imagens atuais**
2. **Processar com TinyPNG ou Squoosh**
3. **Substituir arquivos originais**
4. **Fazer commit e deploy**

### Opção 3: Converter para WebP
```bash
# Instalar cwebp (Google)
# Ubuntu/Debian:
sudo apt-get install webp

# Mac:
brew install webp

# Converter todas as imagens
for file in public/images/*.{png,jpg}; do
  cwebp -q 85 "$file" -o "${file%.*}.webp"
done
```

## 📊 Métricas de Performance

### Antes da Otimização Next.js:
- Tamanho total: ~5-10MB
- Tempo de carregamento: 3-5s

### Depois da Otimização Next.js:
- Tamanho total: ~1-2MB (com WebP/AVIF)
- Tempo de carregamento: <1s
- Lazy loading: Apenas imagens visíveis carregam

## ✅ Checklist de Otimização

- [x] Usar componente `<Image>` do Next.js
- [x] Configurar formatos modernos (WebP, AVIF)
- [x] Adicionar `priority` em imagens críticas
- [x] Configurar `sizes` responsivos
- [x] Habilitar lazy loading
- [x] Configurar cache de imagens
- [ ] Comprimir imagens originais (opcional)
- [ ] Converter para WebP manualmente (opcional)
- [ ] Adicionar imagens de diferentes resoluções (opcional)

## 🎨 Dicas Adicionais

1. **Use SVG para ícones** quando possível
2. **Evite imagens muito grandes** (>2MB originais)
3. **Teste no Google PageSpeed Insights**
4. **Monitore Core Web Vitals**

## 🔗 Links Úteis

- [Next.js Image Optimization](https://nextjs.org/docs/basic-features/image-optimization)
- [Web.dev Image Optimization](https://web.dev/fast/#optimize-your-images)
- [TinyPNG](https://tinypng.com/)
- [Squoosh](https://squoosh.app/)

