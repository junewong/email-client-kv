#!/usr/bin/env python3
"""测试所有模块是否可以正常导入"""

print("测试模块导入...")

try:
    from src.utils.crypto import encrypt_password, decrypt_password
    print("✓ crypto模块")
    
    from src.core.account import AccountManager
    print("✓ account模块")
    
    from src.core.imap_client import IMAPClient
    print("✓ imap_client模块")
    
    from src.core.smtp_client import SMTPClient
    print("✓ smtp_client模块")
    
    from src.core.storage import EmailStorage
    print("✓ storage模块")
    
    from src.utils.config import MAIL_PROVIDERS
    print("✓ config模块")
    
    print("\n所有模块导入成功！")
    
    # 测试加密解密
    print("\n测试密码加密...")
    password = "test123"
    encrypted = encrypt_password(password)
    decrypted = decrypt_password(encrypted)
    assert password == decrypted
    print(f"✓ 加密解密测试通过")
    
    print("\n✅ 所有测试通过！")
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
