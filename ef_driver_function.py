from ef_eval import Evaluate

evaluate = Evaluate("spritzer-self-test1.run", "spritzer.cbor.hierarchical.qrels")

evaluate.debug()
