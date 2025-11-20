# 🎨 Guia: Imagem de Fundo Sutil para Chat do Bot

## ✅ Imagens Criadas

Foram criadas **2 versões** de imagens de fundo sutis:

1. **`genesys_chat_background.jpg`** - Com logo Genesys muito sutil (5% opacidade)
2. **`genesys_chat_background_minimal.jpg`** - Versão minimalista (apenas gradiente)

**Localização:** `bot-telegram/backgrounds/`

---

## 📱 Como Aplicar no Telegram

### **No Telegram Desktop:**

1. Abra o chat com o bot **Genesys Legal Bot**
2. Clique nos **três pontos** (⋮) no canto superior direito
3. Selecione **"Change Background"** ou **"Alterar Papel de Parede"**
4. Clique em **"Choose from File"** ou **"Escolher Arquivo"**
5. Navegue até: `bot-telegram/backgrounds/`
6. Selecione `genesys_chat_background.jpg` ou `genesys_chat_background_minimal.jpg`
7. Ajuste a opacidade se desejar (recomendado: 15-25%)
8. Clique em **"Apply"** ou **"Aplicar"**

### **No Telegram Mobile (Android/iOS):**

1. Abra o chat com o bot
2. Toque nos **três pontos** (⋮) no topo
3. Selecione **"Change Background"** ou **"Alterar Papel de Parede"**
4. Toque em **"Choose from Gallery"** ou **"Escolher da Galeria"**
5. Selecione a imagem criada
6. Ajuste a opacidade (arraste o slider)
7. Toque em **"Apply"** ou **"Aplicar"**

---

## 🎨 Características das Imagens

### **Versão com Logo:**
- ✅ Fundo escuro elegante (gradiente suave)
- ✅ Logo Genesys no canto inferior direito
- ✅ Logo com apenas **5% de opacidade** (muito sutil)
- ✅ Padrão de pontos discretos para textura
- ✅ Dimensões: 1080x1920px (otimizado para mobile)
- ✅ Tamanho: ~36 KB (leve e rápido)

### **Versão Minimalista:**
- ✅ Apenas gradiente suave
- ✅ Sem logo (ainda mais discreto)
- ✅ Cor escura azulada profissional
- ✅ Ideal para quem quer máximo minimalismo

---

## 🔧 Recriar as Imagens

Se quiser ajustar a opacidade ou criar novas versões:

```bash
cd products/tier1/bot-telegram
python3 criar_background.py
```

**Ajustar opacidade da logo:**
Edite a linha 65 no arquivo `criar_background.py`:
```python
alpha = alpha.point(lambda p: int(p * 0.05))  # 5% - altere para 0.03 (3%) ou 0.08 (8%)
```

---

## 💡 Dicas

1. **Opacidade no Telegram:** Ajuste para 15-25% para ficar bem sutil
2. **Escolha a versão:** Use a com logo se quiser branding, a minimalista se quiser apenas elegância
3. **Compatibilidade:** Funciona em Desktop, Android e iOS
4. **Repetir processo:** Se trocar de dispositivo, repita o processo em cada um

---

## 🎯 Resultado Esperado

Após aplicar, o chat terá:
- ✅ Fundo escuro elegante e profissional
- ✅ Logo Genesys muito sutil (quase imperceptível, mas presente)
- ✅ Visual limpo que não interfere na leitura
- ✅ Identidade visual da marca discretamente presente

---

**Status:** ✅ **IMAGENS CRIADAS E PRONTAS PARA USO**

