import pickle


class Persistence_Exemplar:
    """class for serialization/deserialization"""

    @staticmethod
    def serialize(account):
        with open('example.pickle', 'wb') as f:
            pickle.dump(account, f)
        f.close()

    @staticmethod
    def deserialize():
        with open('example.pickle', 'rb') as f:
            account = pickle.load(f)
        f.close()
        return account
