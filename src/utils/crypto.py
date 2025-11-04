import base64


def encrypt_password(password: str) -> str:
    """简单编码密码（注意：这不是真正的加密）"""
    return base64.b64encode(password.encode()).decode()


def decrypt_password(encrypted: str) -> str:
    """解码密码"""
    return base64.b64decode(encrypted.encode()).decode()
