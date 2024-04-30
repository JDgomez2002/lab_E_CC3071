from utils.yalexReader import *
from utils.yalpReader import *

myFile = "yals/slr-1.yal"
myYalepFile = "yalps/slr-1.yalp"
graphDirectDFA = False
graphMinDFA = False

def main():
  regexs = {
    "Comments": "\"(*\" (^*)* *\"*)\"",
    "Header": "{ *(^})*}",
    "Declaration": "let +['a'-'z']* +=",
    "Variables": "('['(^])*]|^[ \n]*)+",
    "Rules": "rule *tokens *=",
    "InitialToken": "['&'-'}']+",
    "Tokens": "'|' *['\"'-'}']*",
    "Returns": "{ *(^})*}",
    "Trailer": "{ *(_)*",
  }

  startTime = time.time()

  values, tokens, dictTokens, dict = readYalexFile(regexs, myFile)

  values = setValues(values)

  print("\n#########################################################################################")
  print("################################# Variables & Rules #####################################")
  print("#########################################################################################\n")

  # variables
  for lal in values:
    print(lal, ": ", values[lal])

  print()

  # write tokens into the py file
  with open('scan.py', 'w') as f:
    f.write(dict['Header'][1:-1])
    for value in dictTokens:
      fileValues, function = defString(value, dictTokens[value][2:-2])
      dictTokens[value] = f"{{ {function} }}"
      f.write(fileValues)
    f.write(dict['Trailer'][1:-2])

  i = 0
  while i < len(tokens):
    tok = tokens[i]
    if tok in values:
      tokens[i] = values[tokens[i]]
    if tok in dictTokens:
      tokens[i] += dictTokens[tok]
    i += 1

  mainString = ''.join(str(i) for i in tokens)
  mainAscii = asciiTransformer.ASCIITransformer(mainString)

  # rules & tokens
  for tok in dictTokens:
    print(tok, ": ", dictTokens[tok])

  print("\n#########################################################################################")
  print("################################# Postfix expression ####################################")
  print("#########################################################################################\n")

  mainPostfix = shuntingYard.exec(mainAscii)
  print(mainPostfix)
  stack, nodes, treeAlphabet = tree.exec(mainPostfix)

  print("\n#########################################################################################")
  print("############################## Direct & minimized DFA ###################################")
  print("#########################################################################################\n")

  # direct DFA
  states, alphabet, transitions, initialState, finalState = directDFA.exec(stack, nodes, treeAlphabet, graphDirectDFA)

  DFAStates = set()
  for i in states:
    DFAStates.add(str(i))

  DFAAlphabet = set()
  for i in alphabet:
    DFAAlphabet.add(str(i))

  DFATransitions = set()
  for tran in transitions:
    trans = ()
    for t in tran:
      trans = trans + (str(t),)
    DFATransitions.add(trans)

  initStateDFA = {str(initialState)}

  acceptedStatesDFA = set()
  for i in finalState:
    acceptedStatesDFA.add(str(i))

  # min DFA
  newStates, symbols, newTransitions, newInitStates, newFinalStates = minDFA.exec(DFAStates, DFAAlphabet, DFATransitions, initStateDFA, acceptedStatesDFA, graphMinDFA, True)

  tempDict = dictTokens.copy()
  for ret in tempDict:
    if ret[0] == '"' and ret[-1] == '"':
      newString = ret.replace('"', '')
      dictTokens[newString] = dictTokens.pop(ret)[2:-2]
    else:
      dictTokens.pop(ret)

  minimizedDFA = {
    "states": newStates,
    "transitions": newTransitions,
    "symbols": symbols,
    "start_states": newInitStates,
    "final_states": newFinalStates,
    "returns": dictTokens,
  }

  # DFA Minimizado en un archivo .pickle
  with open('result/minDFA.pickle', 'wb') as f:
    pickle.dump(minimizedDFA, f)

  if graphMinDFA:
    print("Min. DFA saved in: result/minDFA.pickle\n")

  execTime = time.time() - startTime

  print(f"Total time: {round(execTime, 3)}s")

if __name__ == "__main__":
  main()

  print("\n\n#########################################################################################")
  print("################################# Program.txt scan ######################################")
  print("#########################################################################################\n\n")

  # from scan import main as scanMain
  # scanMain()

  print("#########################################################################################")
  print("################################### Yalep Reader ########################################")
  print("#########################################################################################\n")

  yalp = Yalp(myYalepFile).getGrammar()
  for key in yalp:
    print("- ",key, ": ", yalp[key])

  print("\n#########################################################################################")
  print("################################## End of program #######################################")
  print("#########################################################################################\n")
