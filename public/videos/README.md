# 📹 Pasta de Vídeos de Depoimentos

Esta pasta contém os vídeos de depoimentos de clientes para o site Genesys Tecnologia.

## 🎥 Como Adicionar Vídeos

### Opção 1: Vídeos Locais (Recomendado para vídeos curtos)

1. **Grave o vídeo do depoimento** (recomendado: 30-60 segundos)
2. **Converta para MP4** (formato mais compatível)
3. **Otimize o vídeo** para web:
   ```bash
   # Usando FFmpeg para otimizar
   ffmpeg -i video-original.mov -vcodec h264 -acodec aac -strict -2 -b:v 1M -b:a 128k depoimento-1.mp4
   ```
4. **Coloque o arquivo** nesta pasta (`public/videos/`)
5. **Atualize o componente** em `src/components/TestimonialsWithVideo.tsx`:
   ```typescript
   videoUrl: '/videos/depoimento-1.mp4'
   ```

### Opção 2: YouTube (Recomendado para vídeos longos)

1. **Faça upload do vídeo** no YouTube
2. **Obtenha o ID do vídeo** (exemplo: `dQw4w9WgXcQ` de `youtube.com/watch?v=dQw4w9WgXcQ`)
3. **Atualize o componente**:
   ```typescript
   videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ'
   ```

### Opção 3: Vimeo

1. **Faça upload do vídeo** no Vimeo
2. **Obtenha o ID do vídeo** (exemplo: `123456789`)
3. **Atualize o componente**:
   ```typescript
   videoUrl: 'https://player.vimeo.com/video/123456789'
   ```

## 📐 Especificações Recomendadas

### Vídeos Locais:
- **Formato**: MP4 (H.264)
- **Resolução**: 1920x1080 (Full HD) ou 1280x720 (HD)
- **Aspect Ratio**: 16:9
- **Duração**: 30-60 segundos
- **Bitrate**: ~1 Mbps (vídeo) + 128 kbps (áudio)
- **Tamanho máximo**: 10-20 MB por vídeo

### Thumbnails:
- **Formato**: JPG ou PNG
- **Resolução**: 1920x1080
- **Localização**: `public/images/`

## 🎬 Dicas para Gravação

1. **Iluminação**: Use luz natural ou softbox
2. **Áudio**: Use microfone externo (lapela ou direcional)
3. **Enquadramento**: Plano médio (busto até cabeça)
4. **Fundo**: Neutro ou ambiente profissional
5. **Roteiro**: Prepare pontos-chave antes de gravar
6. **Duração**: Mantenha entre 30-60 segundos

## 📝 Estrutura do Depoimento

Um bom depoimento deve incluir:
1. **Nome e cargo** do depoente
2. **Problema** que tinha antes
3. **Solução** que a Genesys ofereceu
4. **Resultados** obtidos (números, se possível)
5. **Recomendação** final

## 🔧 Ferramentas Úteis

### Gravação:
- **OBS Studio** (gratuito, Windows/Mac/Linux)
- **Zoom** (para gravações remotas)
- **Smartphone** (para gravações rápidas)

### Edição:
- **DaVinci Resolve** (gratuito, profissional)
- **iMovie** (Mac, gratuito)
- **Shotcut** (gratuito, multiplataforma)

### Compressão:
- **HandBrake** (gratuito, multiplataforma)
- **FFmpeg** (linha de comando)
- **CloudConvert** (online)

## 📊 Arquivos Atuais

- `depoimento-1.mp4` - Dr. Carlos Silva (Silva & Associados)
- `depoimento-2.mp4` - Dr. Roberto Mendes (Mendes Advocacia)
- `depoimento-3.mp4` - Dr. Fernando Alves (Alves & Partners)

## ⚠️ Importante

- **Não commite vídeos grandes** no Git (use Git LFS ou hospedagem externa)
- **Otimize sempre** os vídeos antes de adicionar
- **Teste em diferentes dispositivos** (mobile, tablet, desktop)
- **Verifique permissões** de uso de imagem dos depoentes

## 🚀 Deploy

Para produção, considere usar:
- **Cloudinary** (CDN de vídeos)
- **Vimeo Pro** (player customizável)
- **AWS S3 + CloudFront** (escalável)
- **YouTube** (gratuito, mas com branding)
