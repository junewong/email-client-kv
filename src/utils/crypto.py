import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def get_device_key():
    """获取设备唯一标识作为加密密钥"""
    import platform
    device_id = platform.node() + platform.machine()
    return hashlib.sha256(device_id.encode()).digest()


def encrypt_password(password: str) -> str:
    """加密密码"""
    key = get_device_key()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(password.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return f"{iv}:{ct}"


def decrypt_password(encrypted: str) -> str:
    """解密密码"""
    key = get_device_key()
    iv, ct = encrypted.split(':')
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')
