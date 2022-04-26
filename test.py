from src.convert import ConvertService

convert = ConvertService()
print(convert.encode_responses(["Hi", "how?", "wow"]))