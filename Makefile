generate-private-key:
	@echo "generating private key"
	openssl genrsa -out jwt-private.pem 2048
extract-public-key:
	@echo "extracting public key from the key pair"
	openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
