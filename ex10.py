class Test:
    def test_check_number(self):
        charactersCount = 15
        phraseLength = len(input())
        print(phraseLength)
        print(type(phraseLength))
        assert charactersCount > phraseLength, f"Allowed characters count which is entered by user = {charactersCount}"




