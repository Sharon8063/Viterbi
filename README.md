# Viterbi
An implementation of HMM( HIDDEN MARKOV MODELS)-Viterbi Algorithm

Dataset description:
State File:

The State_File is a plain text file, where each line carries the information specified below:

    The first line is an integer 𝑁

, which is the number of states.
The next 𝑁
lines are the descriptive names of the states with 𝐼𝐷 𝑖(0≤𝑖≤𝑁−1). Note that the name of a state is mainly for better readability, as the algorithm distinguishes states by their 𝐼𝐷𝑠
(except the two special states).
The next lines are the frequency of transitions between two states. Each line contains three fields (denoted as 𝑓1,𝑓2,𝑓3
), separated by white spaces, meaning that we have seen 𝑓3 number of times where state 𝑓1 transit to state 𝑓2. Note that 𝑓3 could be any non-negative integer (𝑖.𝑒., including 0). Also note that if some state transitions are not specified in this file, we assume the frequency is 0

    .

Symbol File:

The Symbol_File is a plain text file, where each line carries the information specified below:

    The first line is an integer 𝑀

, which is the number of symbols.
The next 𝑀
lines are the descriptive names of the symbols with 𝐼𝐷 𝑖(0≤𝑖≤𝑀−1). Note that the name of a symbol is important and needed when parsing the addresses, however, only the 𝐼𝐷
is used in the rest of the program. All symbol names are case-sensitive.
The next lines are the frequency of emissions between a state and a symbol. Each line contains three fields (denoted as 𝑓1,𝑓2,𝑓3
), separated by white spaces, meaning that we have seen 𝑓3 number of times where state 𝑓1 emits the symbol 𝑓2. Note that 𝑓3 could be any non-negative integer (𝑖.𝑒.,

    including 0). Also note that if some state-symbol emissions are not specified in this file, we assume the frequency is 0.

Query File:

The Query_File consists of one or more lines, where each line is an address to be parsed.

    Parsing. To parse each query line, you first need to decompose the line into a sequence of tokens with the following rules:

    Whenever there is one or more white spaces, you can break there and discard the white spaces.
    We take the following punctuations as a state, so you need to correctly extract them.
    *, ( ) / - & *

For example, the following line:

8/23-35 Barker St., Kingsford, NSW 2032

will be parsed into the following tokens (one token a line)

8
/
23
-
35
Barker
St.
,
Kingsford
,
NSW
2032

Then you can convert each token into the symbol 𝐼𝐷𝑠
, with the possibility that some symbols are never seen in the Symbol_File, and you need to treat it as a special UNK symbol.
