
Files
electrum-4.7.2-x86-64.appimage
iancoleman-bip39-standalone-0.5.6.html
python-3.14.4.tar.xz : python source to guarantee identical output forever
readme.txt
rolls.py : dice to seed https://github.com/Coldcard/firmware/raw/master/docs/rolls.py
seedgen-openssl.py : passphrase to dice with openssl
seedgen-pure.py : passphrase to dice without openssl

SHA256 - Verify before running - sha256sum
cf775fb74a182ca53041b513b49b5ffb414610057c2b6d43037f1c4e77e5065a  electrum-4.7.2-x86-64.appimage
129b03505824879b8a4429576e3de6951c8599644c1afcaae80840f79237695a  iancoleman-bip39-standalone-0.5.6.html
d923c51303e38e249136fc1bdf3568d56ecb03214efdef48516176d3d7faaef8  python-3.14.4.tar.xz
4348a520e57df665e0ab57baa369a95ace0f9b5fba355b3f22b0b9b2c2e6cd30  rolls.py
0fa2c90cd71913ce462d167e0a64c928637fc0f781260ffc164b87961ada457a  seedgen-openssl.py
73d3900689f074b8ca0b8d7a92c6fab1c65f4f404fd1d4d9c564410a1fed9020  seedgen-pure.py

Build python from source without openssl
sudo apt-get install build-essential pkg-config xz-utils
tar -xf python.tar.xz
cd Python
./configure
make
./python seedgen-pure.py | ./python rolls.py

Build python from source with openssl
sudo apt-get install build-essential libssl-dev pkg-config xz-utils
tar -xf python.tar.xz
cd Python
./configure --with-openssl=/usr
make
./python seedgen-openssl.py | ./python rolls.py

Passphrase constraint
ASCII characters only
Non-ASCII characters (accented, non-Latin) will encode inconsistently across systems and keyboards
This would silently produce different dice rolls on recovery

Determinism guarantee
Same passphrase always produces identical dice rolls
pbkdf2_hmac behaviour is fixed in CPython source
BIAS_LIMIT = 252 (42 x 6) eliminates modulo bias
ITERATIONS = 600_000 (OWASP recommendation at time of writing)

Constants
Must never change or output changes for every passphrase
SEPARATOR = b"seedgen:v1:dice:pbkdf2-sha256"
BIAS_LIMIT = 252 (42 x 6 — eliminates modulo bias)
ITERATIONS = 600_000

Wallet configuration
Script type : Native Segwit (p2wpkh)
Derivation : m/84h/0h/0h
Address prefix : bc1q

Security notes
Run on airgapped diskless machine
Shut down immediately after use
Passphrase entropy is the only real security variable

Recovery procedure
Boot airgapped machine
Verify SHA256
Run
Enter passphrase when prompted
Feed output into Electrum
Select Native Segwit (p2wpkh), path m/84h/0h/0h
Verify first 3 receiving addresses
Shut down immediately

