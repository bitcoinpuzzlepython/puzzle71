import random
import time
import os
from datetime import datetime

# Configurações do Puzzle 71
TARGET_ADDRESS = "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU"
INTERVAL_START = 0x400000000000000000  # Início do intervalo (270 bits - 0%)
INTERVAL_END = 0x7FFFFFFFFFFFFFFFFF    # Fim do intervalo (271 bits - 100%)
CONTROL_FILE = "puzzle71_controle.txt"
SOLUTION_FILE = "puzzle71_solucao.txt"

# Calcular intervalo de busca (75% a 90%)
interval_size = INTERVAL_END - INTERVAL_START
SEARCH_START = INTERVAL_START + int(interval_size * 0.75)  # 75% do intervalo
SEARCH_END = INTERVAL_START + int(interval_size * 0.90)    # 90% do intervalo

# Função para gerar endereço Bitcoin from private key
def generate_address(private_key_hex):
    import hashlib
    import base58
    import ecdsa
    
    private_key_bytes = bytes.fromhex(private_key_hex)
    
    # Gerar chave pública
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key_bytes = b'\x04' + vk.to_string()
    
    # SHA-256 + RIPEMD-160
    sha256 = hashlib.sha256(public_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    ripemd160_bytes = ripemd160.digest()
    
    # Add network byte + checksum
    network_bytes = b'\x00' + ripemd160_bytes
    checksum = hashlib.sha256(hashlib.sha256(network_bytes).digest()).digest()[:4]
    address_bytes = network_bytes + checksum
    
    return base58.b58encode(address_bytes).decode('utf-8')

# Verificar se solução já existe
def check_existing_solution():
    if os.path.exists(SOLUTION_FILE):
        with open(SOLUTION_FILE, 'r') as f:
            solution = f.read().splitlines()
            print("🎉 SOLUÇÃO JÁ ENCONTRADA ANTERIORMENTE!")
            print(f"🔑 Chave Privada: {solution[0]}")
            print(f"📫 Endereço: {solution[1]}")
            print(f"💾 Salvo em: {SOLUTION_FILE}")
        return True
    return False

# Carregar chaves já testadas
def load_tested_keys():
    tested = set()
    if os.path.exists(CONTROL_FILE):
        with open(CONTROL_FILE, 'r') as f:
            for line in f:
                tested.add(line.strip())
    return tested

# Salvar chave testada
def save_tested_key(key_hex):
    with open(CONTROL_FILE, 'a') as f:
        f.write(f"{key_hex}\n")

# Salvar solução encontrada
def save_solution(private_key_hex, address):
    with open(SOLUTION_FILE, 'w') as f:
        f.write(f"{private_key_hex}\n")
        f.write(f"{address}\n")
    print(f"💾 Solução salva em {SOLUTION_FILE}")

# Função principal de pesquisa
def search_puzzle71():
    # Verificar se já foi resolvido
    if check_existing_solution():
        return
    
    # Carregar histórico
    tested_keys = load_tested_keys()
    print(f"📊 Chaves já testadas anteriormente: {len(tested_keys)}")
    
    print("🔍 INICIANDO BUSCA NO BITCOIN PUZZLE #71")
    print("=" * 60)
    print(f"🎯 ENDEREÇO ALVO: {TARGET_ADDRESS}")
    print(f"📊 INTERVALO TOTAL: {hex(INTERVAL_START)} a {hex(INTERVAL_END)}")
    print(f"🎯 FOCO DE BUSCA: 75% a 90% do intervalo")
    print(f"   → INÍCIO: {hex(SEARCH_START)}")
    print(f"   → FIM: {hex(SEARCH_END)}")
    print(f"   → TAMANHO: {SEARCH_END - SEARCH_START + 1:,} chaves")
    print(f"⏰ INÍCIO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("⏸️  Pressione Ctrl+C para pausar a qualquer momento")
    print("=" * 60)
    
    keys_tested = 0
    start_time = time.time()
    
    try:
        while True:
            # Gerar chave aleatória no intervalo 75%-90%
            private_key_int = random.randint(SEARCH_START, SEARCH_END)
            private_key_hex = hex(private_key_int)[2:].zfill(64)
            
            # Pular se já testada
            if private_key_hex in tested_keys:
                continue
                
            # Gerar endereço e verificar
            address = generate_address(private_key_hex)
            keys_tested += 1
            tested_keys.add(private_key_hex)
            save_tested_key(private_key_hex)
            
            # Verificar a cada 1000 chaves
            if keys_tested % 1000 == 0:
                elapsed = time.time() - start_time
                speed = keys_tested / elapsed if elapsed > 0 else 0
                print(f"✅ Testadas: {keys_tested:,} chaves | "
                      f"Velocidade: {speed:.2f} chaves/seg | "
                      f"Última: {private_key_hex[:12]}...")
            
            # Verificar se encontrou
            if address == TARGET_ADDRESS:
                print("\n" + "🎉" * 30)
                print("🎊 CHAVE PRIVADA DO PUZZLE #71 ENCONTRADA! 🎊")
                print("🎉" * 30)
                print(f"🔑 CHAVE PRIVADA: {private_key_hex}")
                print(f"📫 ENDEREÇO GERADO: {address}")
                print(f"🎯 ENDEREÇO ALVO: {TARGET_ADDRESS}")
                print(f"⏱️  TEMPO TOTAL: {time.time() - start_time:.2f} segundos")
                print(f"🔍 CHAVES TESTADAS: {keys_tested:,}")
                print(f"📍 POSIÇÃO NO INTERVALO: {private_key_int/interval_size*100:.2f}%")
                
                save_solution(private_key_hex, address)
                break
                
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        speed = keys_tested / elapsed if elapsed > 0 else 0
        print(f"\n⏸️  BUSCA INTERROMPIDA")
        print(f"📊 Total de chaves testadas: {keys_tested:,}")
        print(f"🚀 Velocidade média: {speed:.2f} chaves/segundo")
        print(f"💾 Progresso salvo em {CONTROL_FILE}")

# Execução principal
if __name__ == "__main__":
    print("=" * 60)
    print("           BITCOIN PUZZLE #71 SOLVER")
    print("=" * 60)
    print(f"📍 Pesquisa focada nos 75% a 90% do intervalo")
    print("=" * 60)
    
    search_puzzle71()
    
    print("\n" + "=" * 60)
    print("🚀 Execução concluída!")
    print(f"🕒 Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)