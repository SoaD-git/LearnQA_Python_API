def test_phrase_length():
    phrase = input("Input some phrase less 15 chars: ")
    assert len(phrase) < 15, f"{phrase} have over or equals 15 chars, it's length {len(phrase)}"
