# 🔑 Configuração da API Key CNJ

## ⚠️ Importante

A **API Pública do CNJ (DataJud)** requer uma **chave pública (API Key)** para autenticação.

---

## 📋 Como Obter a Chave

### **1. Acesse o Portal:**

🔗 **https://datajud-wiki.cnj.jus.br/api-publica/acesso/**

### **2. Siga as Instruções:**

1. Cadastre-se ou faça login
2. Solicite a chave pública
3. Aceite os termos de uso
4. Receba a chave

### **3. Formato da Chave:**

A chave vem no formato:
```
Authorization: APIKey SUA_CHAVE_AQUI
```

---

## 🔧 Como Configurar

### **Opção 1: Variável de Ambiente (Recomendado)**

```bash
export CNJ_API_KEY="sua_chave_aqui"
python3 extrair_processos_cnj_fila.py processos.txt
```

### **Opção 2: Arquivo .env**

Crie um arquivo `.env`:
```bash
CNJ_API_KEY=sua_chave_aqui
```

E carregue antes de executar:
```bash
source .env
python3 extrair_processos_cnj_fila.py processos.txt
```

### **Opção 3: Modificar Código (Não Recomendado)**

Edite `extrair_processos_cnj_fila.py`:
```python
extrator = CNJExtractor(
    delay_segundos=1.0,
    api_key="sua_chave_aqui"
)
```

---

## ✅ Testar se Funciona

```bash
# Com chave configurada
export CNJ_API_KEY="sua_chave"
python3 extrair_processos_cnj_fila.py "0001234-56.2024.8.26.0100"
```

Se funcionar, você verá:
```
✅ Sucesso! Movimentações: X
```

Se não funcionar:
```
❌ Erro: Não autorizado - API key necessária
```

---

## 📚 Documentação Oficial

- **Wiki CNJ:** https://datajud-wiki.cnj.jus.br/api-publica/
- **Acesso/Autenticação:** https://datajud-wiki.cnj.jus.br/api-publica/acesso/
- **Termos de Uso:** https://formularios.cnj.jus.br/wp-content/uploads/2023/05/Termos-de-uso-api-publica-V1.1.pdf

---

## ⚠️ Importante

- ⚠️ **Não compartilhe sua chave** publicamente
- ⚠️ **Não faça commit** da chave no Git
- ⚠️ **Use variáveis de ambiente** sempre que possível
- ⚠️ **Respeite os termos de uso** do CNJ

---

**Configure a chave antes de usar o script! 🔑**

