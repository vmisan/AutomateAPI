charactersCount = 15
phraseLength = len(input())
print(phraseLength)
print(type(phraseLength))
if charactersCount > phraseLength:
    assert charactersCount > phraseLength
    print(f"Allowed characters count which is entered by user = {charactersCount} ")
else:
    print(f"User typed not allowed count if characters = {charactersCount}")




