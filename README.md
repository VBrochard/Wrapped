## How it works
 
1. **Watermarking** — overlays a stamp PDF onto every page of the target PDF
2. **Encryption** — encrypts the watermarked PDF using AES-256-GCM with a password-derived key (PBKDF2-HMAC-SHA256, 650 000 iterations)
 
The output is an encrypted binary file that can only be read by someone with the correct password.
 
## Requirements
 
```bash
pip install cryptography pypdf
```
 
## Usage
 
### Encrypt a PDF
 
```bash
python Ewrapped.py <input.pdf> <watermark.pdf> <output_file>
```
 
You will be prompted to enter and confirm an encryption password.
 
### Decrypt a PDF
 
```bash
python Dwrapped.py <encrypted_file> <output.pdf>
```
 
You will be prompted to enter the decryption password.
 
## File structure
 
```
Wrapped/
├── Ewrapped.py   # Encrypt: watermarks then encrypts a PDF
├── Dwrapped.py   # Decrypt: decrypts and restores the PDF
└── README.md
```
 
## Security details
 
| Parameter | Value |
|-----------|-------|
| Cipher | AES-256-GCM |
| KDF | PBKDF2-HMAC-SHA256 |
| Iterations | 650 000 |
| Salt | 16 bytes (random) |
| Nonce | 12 bytes (random) |
 
## Possible Roadmap
 
Graphical user interface
On-the-fly custom watermark generation (text input by user)
 
