import jwt

class JWT_Manager:

    def __init__(self):

        with open("authorization/private.pem", "r") as f:
            self.private_key = f.read()

        with open("authorization/public.pem", "r") as f:
            self.public_key = f.read()

    def encode(self, data):

        try:

            encoded = jwt.encode(
                data,
                self.private_key,
                algorithm="RS256"
            )

            return encoded

        except Exception as e:

            print(e)

            return None

    def decode(self, token):

        try:

            decoded = jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"]
            )

            return decoded

        except Exception as e:

            print(e)

            return None