import uhashlib

def basicHash(data_bytes):
    if isinstance(data_bytes, str):
        data_bytes = data_bytes.encode("utf-8")
    
    return uhashlib.sha256(data_bytes).digest()    

def keyedHash(key_bytes, data_bytes):
    block_size = 64  # HMAC block size (in bytes)

    if isinstance(key_bytes, str):
        key_bytes = key_bytes.encode("utf-8")
        
    if isinstance(data_bytes, str):
        data_bytes = data_bytes.encode("utf-8")

    # Key padding: If the key is longer than block_size, hash it; otherwise, pad with zeros
    if len(key_bytes) > block_size:
        key_bytes = uhashlib.sha256(key_bytes).digest()
    key_bytes = key_bytes.ljust(block_size, b'\x00')

    # Inner and outer paddings for the key
    inner_key_pad = bytes([x ^ 0x36 for x in key_bytes])
    outer_key_pad = bytes([x ^ 0x5C for x in key_bytes])

    # Calculate inner and outer hash digests
    inner_digest = uhashlib.sha256(inner_key_pad + data_bytes).digest()
    outer_digest = uhashlib.sha256(outer_key_pad + inner_digest).digest()

    # Return the HMAC digest as a hexadecimal string
    
    return outer_digest


content = "ReceiptHandle=AQEBNcvkQFA%2FHbek4vgSaumj5NWhAgkcZ4Id11J2gsqsBU4HeANDi6lykCgKfg7SwmEr08NZ8rMh3DoRwtftbVRRUbXE3fgPwnB%2FNx1dd7ceDWBh3gwzeQ3TCXp7TxacDa4BUliRNuBa%2F3DeDR8vRix3tKXvrczqQq59%2B2CwFSO8FdcBaNsoHLvuV3lIkPIpVbPEiggyjPBNUH1bs1xUJ1bXasQRnkG9Dh%2BU%2B978TFVcqJsy%2B%2FK4BQJYQ0uhLu%2FyLfKWO00obYty3GV6zLIVNbUUfAXAQ5RSyaZx4SDBLAqI%2FDhkZZa6LGx7bpcTZBfYN5uGHBEOZiLSb50JEw%2BtRIEu%2BJ67g3bycGHTujqSQUyB%2BFtWjZElCwJrVJLKIdj7lkQSg5l2ZJmtuZpN%2BAgYhjrC1A%3D%3D"
data_bytes = content.encode("utf-8")
print(uhashlib.sha256(data_bytes).digest().hex())