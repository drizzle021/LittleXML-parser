from token_ import Token

# <?xml version=12.3?><ab:><ef:>N@C#</ab:></ab:> # valid input
tokens = [
    Token("<?xml", "<?xml"),
    Token("version=", "version="),
    Token("NUMBER", "12"),
    Token(".", "."),
    Token("NUMBER", "3"),
    Token("?>", "?>"),

    Token("<", "<"),
    Token("LETTER", "a"),      
    Token("LETTER", "b"),      
    Token(":", ":"),
    Token(">", ">"),

    Token("<", "<"),
    Token("LETTER", "e"),      
    Token("LETTER", "f"),      
    Token(":", ":"),
    Token(">", ">"),

    Token("LETTER", "N"),      
    Token("@", "@"),
    Token("LETTER", "C"),      
    Token("#", "#"),

    Token("</", "</"),
    Token("LETTER", "a"),      
    Token("LETTER", "b"),      
    Token(":", ":"),
    Token(">", ">"),

    Token("</", "</"),
    Token("LETTER", "a"),      
    Token("LETTER", "b"),      
    Token(":", ":"),
    Token(">", ">"),

    Token("$", "$")
]

# <?xml version=12.3?><a/> # valid input
tokens_2 = [
    Token("<?xml", "<?xml"),
    Token("version=", "version="),
    Token("NUMBER", "1"),
    Token("NUMBER", "2"),
    Token(".", "."),
    Token("NUMBER", "3"),
    Token("?>", "?>"),
    Token("<", "<"),
    Token("LETTER", "a"),
    Token("/>", "/>"),
    
    Token("$", "$")
]

# <a><b/><c/></a> # invalid input only one emptyelemtag is allowed
invalid_tokens = [
    Token("<", "<"),
    Token("LETTER", "a"),
    Token(">", ">"),
    Token("<", "<"),
    Token("LETTER", "b"),
    Token("/>", "/>"),
    Token("<", "<"),
    Token("LETTER", "c"),
    Token("/>", "/>"),
    Token("</", "</"),
    Token("LETTER", "a"),
    Token(">", ">"),

    Token("$", "$")
]

# <a>Hello<b/>World</a> # invalid input emptyelemtag cant be nested between words
invalid_tokens_2 = [
    Token("<", "<"),
    Token("LETTER", "a"),
    Token(">", ">"),
    Token("LETTER", "H"),
    Token("LETTER", "e"),
    Token("LETTER", "l"),
    Token("LETTER", "l"),
    Token("LETTER", "o"),
    Token("<", "<"),
    Token("LETTER", "b"),
    Token("/>", "/>"),
    Token("LETTER", "W"),
    Token("LETTER", "o"),
    Token("LETTER", "r"),
    Token("LETTER", "l"),
    Token("LETTER", "d"),
    Token("</", "</"),
    Token("LETTER", "a"),
    Token(">", ">"),

    Token("$", "$")
]

# <a>Hello&</a> ->  <a>Hello</a> 
recovery_test_tokens = [
    Token("<", "<"),
    Token("LETTER", "a"),
    Token(">", ">"),
    Token("LETTER", "H"),
    Token("LETTER", "e"),
    Token("LETTER", "l"),
    Token("LETTER", "l"),
    Token("LETTER", "o"),
    Token("&", "&"),  # invalid token to test recovery
    Token("</", "</"),
    Token("LETTER", "a"),
    Token(">", ">"),

    Token("$", "$")
]

src = '<?xml version=12.3?><ab:><ef:>N@C#</ab:></ab:>'
src_2 = '<?xml version=12.3?><a/>'
invalid_src = '<a><b/><c/></a>'
invalid_src_2 = '<a>Hello<b/>World</a>'
recovery_test_src = '<a>Hello&</a>'