# 🖼️ Guia de Otimização de Imagens - Genesys Tecnologia

## 📊 Análise Atual

### Imagens Encontradas:
- **Total**: ~4.8 MB em `/public/images`
- **Formatos**: PNG (maioria), JPG, JPEG

### Imagens Grandes que Precisam de Otimização:

| Arquivo | Tamanho Atual | Tamanho Ideal | Economia |
|---------|---------------|---------------|----------|
| `clenio.png` | 1.4 MB | ~50-100 KB | **93%** |
| `firmino1.png` | 1.1 MB | ~50-100 KB | **91%** |
| `lilian1.png` | 955 KB | ~50-100 KB | **90%** |
| `firmino.png` | 842 KB | ~50-100 KB | **88%** |
| `kermartin-logo.png` | 178 KB | ~30-50 KB | **75%** |
| `equipe.jpg` | 170 KB | ~50-80 KB | **60%** |
| `lilian.png` | 150 KB | ~40-60 KB | **65%** |
| `genesys-logo.png` | 120 KB | ~30-50 KB | **60%** |

**Economia Total Estimada**: ~4.5 MB → ~500 KB = **90% de redução!**

---

## 🎯 Estratégia de Otimização

### 1. Converter para WebP
WebP oferece 25-35% melhor compressão que JPEG e PNG.

### 2. Redimensionar Imagens
Muitas imagens estão maiores que o necessário.

### 3. Comprimir com Qualidade Adequada
- Fotos: 80-85% de qualidade
- Logos: 90-95% de qualidade
- Ícones: PNG otimizado

---

## 🛠️ Ferramentas Recomendadas

### Opção 1: Sharp (Node.js) - RECOMENDADO
```bash
npm install --save-dev sharp
```

### Opção 2: Squoosh CLI
```bash
npx @squoosh/cli --webp auto public/images/*.{jpg,png}
```

### Opção 3: ImageMagick
```bash
sudo apt-get install imagemagick
```

### Opção 4: Online
- **TinyPNG**: https://tinypng.com/
- **Squoosh**: https://squoosh.app/
- **Compressor.io**: https://compressor.io/

---

## 📝 Script de Otimização Automática

Criei um script em `scripts/optimize-images.js` que:
1. Converte todas as imagens para WebP
2. Mantém os originais como fallback
3. Redimensiona para tamanhos adequados
4. Comprime com qualidade otimizada

### Como Usar:

```bash
# Instalar dependências
npm install --save-dev sharp

# Executar otimização
node scripts/optimize-images.js
```

---

## 🎨 Tamanhos Recomendados

### Fotos de Equipe:
- **Tamanho**: 400x400px (quadrado)
- **Formato**: WebP + JPG fallback
- **Qualidade**: 85%
- **Peso**: 30-50 KB

### Logos:
- **Tamanho**: 512x512px (máximo)
- **Formato**: WebP + PNG fallback
- **Qualidade**: 90%
- **Peso**: 20-40 KB

### Imagens de Hero/Banner:
- **Tamanho**: 1920x1080px (máximo)
- **Formato**: WebP + JPG fallback
- **Qualidade**: 80%
- **Peso**: 100-200 KB

---

## ✅ Checklist de Otimização

- [ ] Converter imagens para WebP
- [ ] Redimensionar para tamanhos adequados
- [ ] Comprimir com qualidade otimizada
- [ ] Adicionar fallbacks (PNG/JPG)
- [ ] Atualizar componentes para usar WebP
- [ ] Implementar lazy loading
- [ ] Adicionar placeholders blur
- [ ] Testar em diferentes dispositivos

---

## 🚀 Implementação no Next.js

O Next.js já otimiza imagens automaticamente com o componente `<Image>`.
Mas podemos melhorar ainda mais:

### 1. Usar WebP:
```typescript
<Image
  src="/images/foto.webp"
  alt="Descrição"
  width={400}
  height={400}
  quality={85}
  placeholder="blur"
  blurDataURL="data:image/..."
/>
```

### 2. Lazy Loading:
```typescript
<Image
  src="/images/foto.webp"
  alt="Descrição"
  loading="lazy"
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

### 3. Responsive Images:
```typescript
<Image
  src="/images/foto.webp"
  alt="Descrição"
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
/>
```

---

## 📈 Benefícios Esperados

### Performance:
- ⚡ **90% menor** tamanho de imagens
- ⚡ **3-5x mais rápido** carregamento de página
- ⚡ **Melhor score** no Google PageSpeed

### SEO:
- 📈 **Melhor ranking** no Google
- 📈 **Menor bounce rate**
- 📈 **Melhor Core Web Vitals**

### UX:
- 😊 **Carregamento instantâneo**
- 😊 **Menos dados móveis**
- 😊 **Melhor experiência**

---

## 🔄 Próximos Passos

1. **Executar script de otimização**
2. **Testar imagens otimizadas**
3. **Atualizar componentes**
4. **Medir performance**
5. **Deploy em produção**

---

## ⚠️ Importante

- **Sempre faça backup** das imagens originais
- **Teste em diferentes navegadores**
- **Verifique qualidade visual**
- **Monitore performance** após deploy
