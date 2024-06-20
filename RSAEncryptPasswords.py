from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


# 生成RSA密钥对并保存到文件
def generate_rsa_key_pair(private_key_path='private_key.pem', public_key_path='public_key.pem'):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 序列化并保存私钥
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(private_key_path, 'wb') as f:
        f.write(private_pem)

    # 序列化并保存公钥
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(public_key_path, 'wb') as f:
        f.write(public_pem)

    print("RSA密钥对已生成并保存到文件。")


# 加密数据
def encrypt_data(public_key_path, data):
    with open(public_key_path, 'rb') as f:
        public_pem = f.read()

    public_key = serialization.load_pem_public_key(public_pem)

    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted


# 解密数据
def decrypt_data(private_key_path, encrypted_data):
    with open(private_key_path, 'rb') as f:
        private_pem = f.read()

    private_key = serialization.load_pem_private_key(private_pem, password=None)

    decrypted = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted


# 测试生成密钥对、加密和解密
if __name__ == '__main__':
    # 生成RSA密钥对
    generate_rsa_key_pair()

    # 要加密的数据
    message = b'Hello, this is a secret message!'

    # 加密数据
    encrypted_message = encrypt_data('public_key.pem', message)
    print("加密后的数据：", encrypted_message)

    # 解密数据
    decrypted_message = decrypt_data('private_key.pem', encrypted_message)
    print("解密后的数据：", decrypted_message.decode())
