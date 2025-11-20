"""
Serviço de autenticação para usuários do bot Telegram
Permite login/logout e verificação de acesso ao Kermartin
"""

import sys
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime, timedelta
import hashlib
import secrets

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy.orm import Session
from shared.config.database import get_db
from shared.database.models import User
from shared.utils.logger import bot_telegram_logger as logger


class AuthService:
    """Serviço de autenticação"""
    
    # Dicionário para armazenar estados de login em dois passos
    _login_states: Dict[int, Dict] = {}
    
    # Dicionário para códigos de recuperação de senha
    _recovery_codes: Dict[str, Dict] = {}
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Gera hash da senha usando SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _check_session_timeout(self, user: User) -> bool:
        """
        Verifica se a sessão expirou (24h de inatividade)
        
        Returns:
            True se sessão expirada, False caso contrário
        """
        if not user.ultimo_login:
            return True
        
        timeout = timedelta(hours=24)
        tempo_inativo = datetime.utcnow() - user.ultimo_login
        
        if tempo_inativo > timeout:
            return True
        return False
    
    def iniciar_login(self, telegram_id: int) -> tuple[bool, str]:
        """
        Inicia processo de login em dois passos (passo 1: solicita email)
        
        Returns:
            (sucesso, mensagem)
        """
        self._login_states[telegram_id] = {'step': 1, 'email': None}
        return True, (
            "🔐 **Login - Passo 1/2**\n\n"
            "Por favor, informe seu **email** cadastrado:\n\n"
            "💡 Digite apenas o email (ex: `usuario@exemplo.com`)"
        )
    
    def processar_email_login(self, telegram_id: int, email: str) -> tuple[bool, str]:
        """
        Processa email no login em dois passos (passo 1)
        
        Returns:
            (sucesso, mensagem)
        """
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                if telegram_id in self._login_states:
                    del self._login_states[telegram_id]
                return False, "❌ Usuário não encontrado. Use /start primeiro."
            
            # Verificar se email confere
            if not user.email or user.email.lower() != email.lower():
                if telegram_id in self._login_states:
                    del self._login_states[telegram_id]
                return False, "❌ Email não confere com o cadastro."
            
            # Armazenar email no estado
            if telegram_id not in self._login_states:
                self._login_states[telegram_id] = {}
            
            self._login_states[telegram_id]['step'] = 2
            self._login_states[telegram_id]['email'] = email.lower()
            
            return True, (
                "🔐 **Login - Passo 2/2**\n\n"
                "Agora informe sua **senha**:\n\n"
                "🔒 Sua senha será processada de forma segura.\n"
                "💡 Digite apenas a senha (será oculta na mensagem)"
            )
            
        except Exception as e:
            logger.error(f"Erro ao processar email no login: {e}")
            if telegram_id in self._login_states:
                del self._login_states[telegram_id]
            return False, "❌ Erro ao processar email. Tente novamente."
        finally:
            db.close()
    
    def completar_login(self, telegram_id: int, password: str) -> tuple[bool, str]:
        """
        Completa login em dois passos (passo 2: valida senha)
        
        Returns:
            (sucesso, mensagem)
        """
        if telegram_id not in self._login_states or self._login_states[telegram_id]['step'] != 2:
            return False, "❌ Por favor, inicie o login com `/login` primeiro."
        
        email = self._login_states[telegram_id]['email']
        
        # Limpar estado
        del self._login_states[telegram_id]
        
        # Fazer login normalmente
        return self.login(telegram_id, email, password)
    
    def login(self, telegram_id: int, email: str, password: str) -> tuple[bool, str]:
        """
        Faz login do usuário
        
        Args:
            telegram_id: ID do Telegram do usuário
            email: Email do usuário
            password: Senha (texto plano)
            
        Returns:
            (sucesso, mensagem)
        """
        db: Session = next(get_db())
        
        try:
            # Buscar usuário pelo telegram_id
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False, "❌ Usuário não encontrado. Use /start primeiro."
            
            # Verificar se email está cadastrado
            if not user.email:
                return False, "❌ Email não cadastrado. Informe seu email no login."
            
            # Verificar se email confere
            if user.email.lower() != email.lower():
                return False, "❌ Email não confere com o cadastro."
            
            # Verificar senha
            if not user.senha_hash:
                # Primeiro login - definir senha
                user.senha_hash = self._hash_password(password)
                db.commit()
                logger.info(f"Senha definida para usuário {telegram_id}")
                return False, "✅ Senha definida com sucesso! Faça login novamente."
            
            # Verificar hash da senha
            password_hash = self._hash_password(password)
            if user.senha_hash != password_hash:
                return False, "❌ Senha incorreta."
            
            # Verificar timeout de sessão anterior
            if user.autenticado and self._check_session_timeout(user):
                logger.info(f"Sessão expirada para usuário {telegram_id}, reautenticando")
            
            # Login bem-sucedido
            user.autenticado = True
            user.ultimo_login = datetime.utcnow()
            db.commit()
            db.refresh(user)
            
            logger.info(f"Usuário {telegram_id} ({email}) fez login")
            return True, "✅ Login realizado com sucesso! Você agora tem acesso ao Kermartin."
            
        except Exception as e:
            logger.error(f"Erro ao fazer login: {e}")
            db.rollback()
            return False, "❌ Erro ao fazer login. Tente novamente."
        finally:
            db.close()
    
    def logout(self, telegram_id: int) -> tuple[bool, str]:
        """
        Faz logout do usuário
        
        Args:
            telegram_id: ID do Telegram do usuário
            
        Returns:
            (sucesso, mensagem)
        """
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False, "❌ Usuário não encontrado."
            
            user.autenticado = False
            db.commit()
            
            logger.info(f"Usuário {telegram_id} fez logout")
            return True, "✅ Logout realizado com sucesso."
            
        except Exception as e:
            logger.error(f"Erro ao fazer logout: {e}")
            db.rollback()
            return False, "❌ Erro ao fazer logout."
        finally:
            db.close()
    
    def is_authenticated(self, telegram_id: int, check_timeout: bool = True) -> bool:
        """
        Verifica se usuário está autenticado e se sessão não expirou
        
        Args:
            telegram_id: ID do Telegram do usuário
            check_timeout: Se deve verificar timeout de sessão
            
        Returns:
            True se autenticado e sessão válida, False caso contrário
        """
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False
            
            if not user.autenticado:
                return False
            
            # Verificar timeout de sessão
            if check_timeout and self._check_session_timeout(user):
                user.autenticado = False
                db.commit()
                logger.info(f"Sessão expirada para usuário {telegram_id}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar autenticação: {e}")
            return False
        finally:
            db.close()
    
    def gerar_codigo_recuperacao(self, email: str) -> tuple[bool, str, str]:
        """
        Gera código de recuperação de senha
        
        Returns:
            (sucesso, mensagem, codigo)
        """
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.email == email.lower()).first()
            
            if not user:
                return False, "❌ Email não encontrado no sistema.", ""
            
            # Gerar código de 6 dígitos
            codigo = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
            
            # Armazenar código (válido por 15 minutos)
            self._recovery_codes[codigo] = {
                'email': email.lower(),
                'telegram_id': user.telegram_id,
                'expires_at': datetime.utcnow() + timedelta(minutes=15)
            }
            
            logger.info(f"Código de recuperação gerado para {email}")
            return True, (
                f"✅ Código de recuperação gerado!\n\n"
                f"**Código:** `{codigo}`\n\n"
                f"⚠️ Este código é válido por 15 minutos.\n"
                f"Use o comando `/recuperar_senha {codigo} nova_senha` para redefinir sua senha."
            ), codigo
            
        except Exception as e:
            logger.error(f"Erro ao gerar código de recuperação: {e}")
            return False, "❌ Erro ao gerar código. Tente novamente.", ""
        finally:
            db.close()
    
    def recuperar_senha(self, codigo: str, nova_senha: str) -> tuple[bool, str]:
        """
        Recupera senha usando código
        
        Returns:
            (sucesso, mensagem)
        """
        if codigo not in self._recovery_codes:
            return False, "❌ Código inválido ou expirado."
        
        recovery_data = self._recovery_codes[codigo]
        
        # Verificar expiração
        if datetime.utcnow() > recovery_data['expires_at']:
            del self._recovery_codes[codigo]
            return False, "❌ Código expirado. Gere um novo código."
        
        telegram_id = recovery_data['telegram_id']
        
        # Remover código usado
        del self._recovery_codes[codigo]
        
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False, "❌ Usuário não encontrado."
            
            # Atualizar senha
            user.senha_hash = self._hash_password(nova_senha)
            user.autenticado = False  # Forçar novo login
            db.commit()
            
            logger.info(f"Senha recuperada para usuário {telegram_id}")
            return True, (
                "✅ Senha redefinida com sucesso!\n\n"
                "Faça login novamente com sua nova senha:\n"
                "`/login`"
            )
            
        except Exception as e:
            logger.error(f"Erro ao recuperar senha: {e}")
            db.rollback()
            return False, "❌ Erro ao redefinir senha. Tente novamente."
        finally:
            db.close()
    
    def trocar_senha(self, telegram_id: int, senha_atual: str, nova_senha: str) -> tuple[bool, str]:
        """
        Troca senha do usuário (requer senha atual)
        
        Returns:
            (sucesso, mensagem)
        """
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False, "❌ Usuário não encontrado."
            
            # Verificar senha atual
            if not user.senha_hash:
                return False, "❌ Você ainda não possui senha cadastrada. Use `/cadastrar` primeiro."
            
            senha_atual_hash = self._hash_password(senha_atual)
            if user.senha_hash != senha_atual_hash:
                return False, "❌ Senha atual incorreta."
            
            # Atualizar senha
            user.senha_hash = self._hash_password(nova_senha)
            db.commit()
            
            logger.info(f"Senha trocada para usuário {telegram_id}")
            return True, "✅ Senha alterada com sucesso!"
            
        except Exception as e:
            logger.error(f"Erro ao trocar senha: {e}")
            db.rollback()
            return False, "❌ Erro ao trocar senha. Tente novamente."
        finally:
            db.close()
    
    def require_auth_message(self) -> str:
        """Retorna mensagem pedindo login"""
        return (
            "🔒 **Acesso Restrito ao Kermartin**\n\n"
            "Para acessar informações do Kermartin, você precisa fazer login.\n\n"
            "**Como fazer login:**\n"
            "1. Use o comando `/login`\n"
            "2. Informe seu email e senha\n\n"
            "**Exemplo:**\n"
            "`/login email@exemplo.com senha123`\n\n"
            "💡 Se você ainda não tem cadastro, entre em contato com o administrador."
        )
    
    def register_user_email(self, telegram_id: int, email: str, password: str) -> tuple[bool, str]:
        """
        Registra email e senha para um usuário existente
        
        Args:
            telegram_id: ID do Telegram
            email: Email do usuário
            password: Senha
            
        Returns:
            (sucesso, mensagem)
        """
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False, "❌ Usuário não encontrado. Use /start primeiro."
            
            # Verificar se email já está em uso
            existing = db.query(User).filter(
                User.email == email.lower(),
                User.id != user.id
            ).first()
            
            if existing:
                return False, "❌ Este email já está cadastrado para outro usuário."
            
            # Registrar email e senha
            user.email = email.lower()
            user.senha_hash = self._hash_password(password)
            user.autenticado = False  # Precisa fazer login após cadastro
            db.commit()
            
            logger.info(f"Email registrado para usuário {telegram_id}: {email}")
            return True, (
                "✅ Cadastro realizado com sucesso!\n\n"
                "Agora faça login com:\n"
                f"`/login {email} {password}`"
            )
            
        except Exception as e:
            logger.error(f"Erro ao registrar email: {e}")
            db.rollback()
            return False, "❌ Erro ao registrar. Tente novamente."
        finally:
            db.close()


# Instância global
auth_service = AuthService()

